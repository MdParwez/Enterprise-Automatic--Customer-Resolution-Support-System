import json
from typing import Any

from openai import OpenAI

from src.config import get_settings


class LLMResolutionAdvisor:
    def __init__(self) -> None:
        self.settings = get_settings()

    @property
    def provider_name(self) -> str:
        if self.settings.groq_api_key and self.settings.ai_provider.lower() == "groq":
            return f"groq:{self.settings.groq_model}"
        return "local_rules"

    def refine_resolution(
        self,
        issue_message: str,
        issue_type: str,
        case_context: dict[str, Any],
        evidence: list[dict[str, Any]],
        playbook: dict[str, Any],
    ) -> dict[str, Any]:
        if not self.settings.groq_api_key or self.settings.ai_provider.lower() != "groq":
            return {
                "ai_provider": "local_rules",
                "ai_summary": "Local policy rules were used because no Groq API key is configured.",
            }

        prompt = {
            "customer_issue": issue_message,
            "detected_issue_type": issue_type,
            "case_context": case_context,
            "policy_and_case_evidence": evidence[:5],
            "baseline_playbook": playbook,
        }
        try:
            client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=self.settings.groq_api_key)
            response = client.chat.completions.create(
                model=self.settings.groq_model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an enterprise customer support resolution advisor. "
                            "Return compact JSON only. Do not execute actions. "
                            "Respect policy evidence and preserve human approval for risky financial or identity actions. "
                            "Schema: recommended_action, rationale, risk_level, confidence_score, sla_target, "
                            "approval_reason, risk_flags, next_best_actions, ai_summary."
                        ),
                    },
                    {"role": "user", "content": json.dumps(prompt, default=str)},
                ],
                temperature=0.2,
            )
            content = response.choices[0].message.content or "{}"
        except Exception as exc:
            return {
                "ai_provider": "local_rules",
                "ai_summary": f"Groq was configured but unavailable, so local policy rules were used. Reason: {type(exc).__name__}.",
            }
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            data = {"ai_summary": content[:600]}

        allowed = {
            "recommended_action",
            "rationale",
            "risk_level",
            "confidence_score",
            "sla_target",
            "approval_reason",
            "risk_flags",
            "next_best_actions",
            "ai_summary",
        }
        refined = {key: value for key, value in data.items() if key in allowed}
        if refined.get("risk_level") not in {"low", "medium", "high"}:
            refined.pop("risk_level", None)
        if "confidence_score" in refined:
            try:
                refined["confidence_score"] = max(0.0, min(1.0, float(refined["confidence_score"])))
            except (TypeError, ValueError):
                refined.pop("confidence_score", None)
        for key in ("risk_flags", "next_best_actions"):
            if key in refined and not isinstance(refined[key], list):
                refined.pop(key, None)
        refined["ai_provider"] = self.provider_name
        return refined
