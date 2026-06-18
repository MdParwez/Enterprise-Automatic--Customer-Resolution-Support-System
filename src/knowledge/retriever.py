from dataclasses import dataclass
import hashlib
import math

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, PointStruct, VectorParams
except ImportError:  # pragma: no cover - fallback path for minimal installs
    QdrantClient = None
    Distance = None
    PointStruct = None
    VectorParams = None


@dataclass(frozen=True)
class KnowledgeDocument:
    collection: str
    title: str
    content: str
    score: float


LOCAL_KNOWLEDGE = [
    KnowledgeDocument(
        collection="policies",
        title="Refund Policy",
        content="Refunds pending more than 7 days require proactive investigation. Platinum customers may receive priority handling and a goodwill credit up to 50 USD when delay is company-caused.",
        score=0,
    ),
    KnowledgeDocument(
        collection="policies",
        title="Compensation Policy",
        content="Low-risk compensation can be auto-approved up to 50 USD for platinum and gold customers when policy conditions are met.",
        score=0,
    ),
    KnowledgeDocument(
        collection="policies",
        title="Escalation Policy",
        content="High-risk, fraud-sensitive, or compensation requests above 50 USD require manual approval before execution.",
        score=0,
    ),
    KnowledgeDocument(
        collection="policies",
        title="Customer Support SOPs",
        content="Create an incident, verify downstream state, send customer-facing summary, and record an audit trail for every autonomous resolution.",
        score=0,
    ),
    KnowledgeDocument(
        collection="policies",
        title="Flight Delay Policy",
        content="Flight delays above 120 minutes qualify for proactive notification, rebooking options, meal vouchers, and compensation review based on customer tier and jurisdiction.",
        score=0,
    ),
    KnowledgeDocument(
        collection="policies",
        title="Baggage Recovery SOP",
        content="Delayed baggage cases require bag-trace creation, airport ops routing, customer updates every 12 hours, and reimbursement review for essentials.",
        score=0,
    ),
    KnowledgeDocument(
        collection="policies",
        title="Billing Dispute Policy",
        content="Duplicate charge and billing dispute cases require payment reconciliation, transaction evidence, charge reversal eligibility checks, and fraud-risk screening.",
        score=0,
    ),
    KnowledgeDocument(
        collection="policies",
        title="Subscription Retention Policy",
        content="Subscription cancellation, renewal, and plan-change issues should include entitlement validation, prorated credit checks, and save-offer eligibility.",
        score=0,
    ),
    KnowledgeDocument(
        collection="policies",
        title="Account Security Policy",
        content="Account lockout, login, and identity-sensitive requests require verification. High-risk account recovery actions must be routed for manual approval.",
        score=0,
    ),
    KnowledgeDocument(
        collection="historical_cases",
        title="Delayed refund after cancellation",
        content="A 12-day pending refund was resolved by creating a finance escalation ticket and offering a 25 USD goodwill credit. Outcome: successful.",
        score=0,
    ),
    KnowledgeDocument(
        collection="historical_cases",
        title="Payment gateway reconciliation delay",
        content="Refund delayed by gateway reconciliation was routed to payments ops with customer notification. Outcome: successful after verification.",
        score=0,
    ),
    KnowledgeDocument(
        collection="historical_cases",
        title="Delayed flight with premium customer",
        content="A 3-hour flight delay was resolved by issuing a meal voucher, creating an ops ticket, and offering rebooking. Outcome: high satisfaction.",
        score=0,
    ),
    KnowledgeDocument(
        collection="historical_cases",
        title="Duplicate billing charge",
        content="Duplicate billing was resolved by payment reconciliation, reversal ticket creation, and verification against transaction logs. Outcome: successful.",
        score=0,
    ),
    KnowledgeDocument(
        collection="historical_cases",
        title="Account lockout recovery",
        content="Account lockout was triaged with identity checks and manual approval due to security risk. Outcome: resolved after verification.",
        score=0,
    ),
]


class KnowledgeRetriever:
    def __init__(self) -> None:
        self.vector_size = 48
        self.documents = LOCAL_KNOWLEDGE
        self.vectors = [self._embed(f"{document.title} {document.content}") for document in self.documents]
        self.collection_name = "omnisupport_knowledge"
        self.qdrant = None
        self._initialize_qdrant()

    def search(self, query: str, limit: int = 4) -> list[KnowledgeDocument]:
        query_vector = self._embed(query)
        if self.qdrant is not None:
            try:
                hits = self.qdrant.search(
                    collection_name=self.collection_name,
                    query_vector=query_vector,
                    limit=limit,
                )
                return [
                    KnowledgeDocument(
                        collection=hit.payload["collection"],
                        title=hit.payload["title"],
                        content=hit.payload["content"],
                        score=float(hit.score),
                    )
                    for hit in hits
                ]
            except Exception:
                self.qdrant = None

        query_terms = {term.strip(".,!?").lower() for term in query.split() if len(term) > 2}
        ranked: list[KnowledgeDocument] = []
        for document, vector in zip(self.documents, self.vectors):
            haystack = f"{document.title} {document.content}".lower()
            keyword_score = sum(1 for term in query_terms if term in haystack)
            vector_score = self._cosine(query_vector, vector)
            score = float(keyword_score) + vector_score
            ranked.append(KnowledgeDocument(document.collection, document.title, document.content, float(score)))
        return sorted(ranked, key=lambda item: item.score, reverse=True)[:limit]

    def _embed(self, text: str) -> list[float]:
        vector = [0.0] * self.vector_size
        for raw in text.lower().replace("/", " ").replace("-", " ").split():
            token = raw.strip(".,!?():;")
            if not token:
                continue
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = digest[0] % self.vector_size
            sign = 1.0 if digest[1] % 2 == 0 else -1.0
            vector[index] += sign
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]

    def _cosine(self, left: list[float], right: list[float]) -> float:
        return sum(a * b for a, b in zip(left, right))

    def _initialize_qdrant(self) -> None:
        if QdrantClient is None:
            return
        try:
            self.qdrant = QdrantClient(":memory:")
            self.qdrant.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
            )
            points = [
                PointStruct(
                    id=index,
                    vector=vector,
                    payload={
                        "collection": document.collection,
                        "title": document.title,
                        "content": document.content,
                    },
                )
                for index, (document, vector) in enumerate(zip(self.documents, self.vectors), start=1)
            ]
            self.qdrant.upsert(collection_name=self.collection_name, points=points)
        except Exception:
            self.qdrant = None
