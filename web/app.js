const state = {
  result: null,
  pendingManual: null,
};

const $ = (id) => document.getElementById(id);

function toast(message) {
  const node = $("toast");
  node.textContent = message;
  node.classList.remove("hidden");
  window.setTimeout(() => node.classList.add("hidden"), 3600);
}

function percent(value) {
  if (value === undefined || value === null) return "--";
  return `${Math.round(Number(value) * 100)}%`;
}

function formatIssue(value) {
  return value ? value.replaceAll("_", " ") : "--";
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function scrollChat() {
  $("chatStream").scrollTop = $("chatStream").scrollHeight;
}

function addMessage(role, title, body, stats = null) {
  const article = document.createElement("article");
  article.className = `message ${role}`;
  article.innerHTML = `
    <div class="avatar">${role === "user" ? "CU" : "AI"}</div>
    <div class="bubble">
      <strong>${escapeHtml(title)}</strong>
      <p>${escapeHtml(body)}</p>
      ${stats ? `<div class="bubble-grid">${stats.map((item) => `<div><span>${escapeHtml(item.label)}</span><strong>${escapeHtml(item.value)}</strong></div>`).join("")}</div>` : ""}
    </div>
  `;
  $("chatStream").appendChild(article);
  scrollChat();
}

async function checkHealth() {
  try {
    const response = await fetch("/health");
    const data = await response.json();
    $("healthText").textContent = data.status === "ok" ? "API online" : "API degraded";
  } catch {
    $("healthText").textContent = "API offline";
  }
}

async function sendIssue(message) {
  const payload = {
    customer_id: $("customerId").value.trim(),
    message: message.trim(),
    channel: $("channel").value,
  };

  if (!payload.customer_id || !payload.message) {
    toast("Customer ID and message are required.");
    return;
  }

  addMessage("user", payload.customer_id, payload.message);
<<<<<<< HEAD
  addMessage("agent", "OmniSupport AI", "I am starting the investigation. I will check tickets first, then customer/order data, vector knowledge, risk, and workflow routing.");
  renderProcessingAgents();
=======
  addMessage("agent", "ERA Assistant", "I am checking the customer record, matching the right policy, and preparing the safest resolution.");
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
  $("sendBtn").disabled = true;
  $("sendBtn").textContent = "Working";

  try {
    const response = await fetch("/resolve", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) throw new Error(`Resolve failed: ${response.status}`);
    state.result = await response.json();
    renderResult(state.result);
<<<<<<< HEAD
    renderAgentRoom(state.result);
=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
    renderAgentReply(state.result);
    await loadRuns();
    await loadStats();
  } catch (error) {
    addMessage("agent", "ERA Error", error.message);
  } finally {
    $("sendBtn").disabled = false;
    $("sendBtn").textContent = "Send";
  }
}

<<<<<<< HEAD
function renderProcessingAgents() {
  const steps = [
    ["Supervisor", "Understanding request and assigning investigation tasks"],
    ["Customer Agent", "Identifying customer profile and history"],
    ["Ticket Agent", "Checking active tickets before creating anything new"],
    ["Order Agent", "Checking booking, payment, refund, or account context"],
    ["Knowledge Agent", "Searching vector knowledge and historical cases"],
    ["Resolution Agent", "Reasoning with Groq/local policy controls"],
    ["Workflow Agent", "Preparing team routing and customer update"],
  ];
  $("agentRoom").innerHTML = steps
    .map(([name, detail], index) => `<div class="agent-card ${index < 3 ? "running" : "idle"}"><strong>${name}</strong><span>${detail}</span></div>`)
    .join("");
}

function renderAgentRoom(result) {
  $("agentProvider").textContent = result.decision?.ai_provider || "local_rules";
  const events = result.events || [];
  const cards = events.map((event) => {
    const status = event.action === "hold" ? "waiting" : "done";
    return `<div class="agent-card ${status}"><strong>${escapeHtml(event.agent)}</strong><span>${escapeHtml(event.detail)}</span></div>`;
  });
  $("agentRoom").innerHTML = cards.length
    ? cards.join("")
    : "<div class=\"agent-card idle\"><strong>Supervisor</strong><span>No activity yet</span></div>";
}

=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
function renderAgentReply(result) {
  const decision = result.decision;
  const needsManual = result.approval_status === "manual_required";
  const body = needsManual
    ? `I found a compliant resolution, but this is ${decision.risk_level}-risk and needs human approval before execution. Recommended action: ${decision.recommended_action}.`
    : result.final_response;

  addMessage("agent", needsManual ? "Manual approval required" : "Resolution completed", body, [
    { label: "Issue", value: formatIssue(result.issue_type) },
    { label: "Approval", value: formatIssue(result.approval_status) },
    { label: "SLA", value: decision.sla_target },
  ]);
}

function renderResult(result) {
  const decision = result.decision;
  $("issueType").textContent = formatIssue(result.issue_type);
  $("approval").textContent = formatIssue(result.approval_status);
  $("ticket").textContent = result.ticket_id || "manual";
  $("decisionTitle").textContent = decision.recommended_action;
  $("decisionRationale").textContent = decision.rationale;
  $("confidence").textContent = percent(decision.confidence_score);
  $("risk").textContent = decision.risk_level;
  $("sla").textContent = decision.sla_target;
<<<<<<< HEAD
  $("agentProvider").textContent = decision.ai_provider || "local_rules";

  const customer = result.case_context?.customer;
  if (customer?.tier) $("customerTier").textContent = customer.tier;
  renderActiveTickets(result.case_context?.active_tickets || []);
  renderWorkflow(result.workflow_status || {});
  renderInternalUpdates(result.internal_updates || []);
  renderToolCalls(result.tool_call_log || []);
=======

  const customer = result.case_context?.customer;
  if (customer?.tier) $("customerTier").textContent = customer.tier;
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539

  $("trace").innerHTML = (result.automation_trace || [])
    .map((item) => `<div class="timeline-item"><strong>${item.stage}</strong><span>${item.status}: ${item.summary}</span></div>`)
    .join("");

  $("evidence").innerHTML = (result.evidence || [])
    .map((item) => `<div class="evidence-item"><strong>${item.title}</strong><span>${item.collection} | score ${item.score}</span><p>${item.content}</p></div>`)
    .join("");

  $("riskFlags").innerHTML = (decision.risk_flags || []).map((flag) => `<span>${formatIssue(flag)}</span>`).join("");
  $("nextActions").innerHTML = (decision.next_best_actions || []).map((action) => `<li>${action}</li>`).join("");

  if (result.approval_status === "manual_required") {
    state.pendingManual = result;
    $("approveBtn").disabled = false;
    $("approvalHint").textContent = `${formatIssue(result.issue_type)} is waiting for approval.`;
  } else {
    state.pendingManual = null;
    $("approveBtn").disabled = true;
    $("approvalHint").textContent = result.ticket_id ? `Executed as ${result.ticket_id}.` : "No manual approval waiting.";
  }
}

<<<<<<< HEAD
function renderActiveTickets(tickets) {
  $("activeTickets").innerHTML = tickets.length
    ? tickets.slice(0, 4).map((ticket) => `<div class="mini-row"><span>${escapeHtml(ticket.ticket_id)}</span><strong>${escapeHtml(ticket.status)}</strong></div>`).join("")
    : "<div class=\"mini-row\"><span>No active ticket</span><strong>Clear</strong></div>";
}

function renderWorkflow(workflow) {
  $("workflowPhase").textContent = formatIssue(workflow.phase || "waiting");
  $("workflowOwner").textContent = workflow.owner || "--";
  $("workflowBar").style.width = `${Math.max(0, Math.min(100, Number(workflow.progress || 0)))}%`;
}

function renderInternalUpdates(updates) {
  $("internalUpdates").innerHTML = updates.length
    ? updates.map((item) => `<div class="run-item"><span>${escapeHtml(item.team)}: ${escapeHtml(item.message)}</span><strong>${escapeHtml(item.status)}</strong></div>`).join("")
    : "<div class=\"run-item\"><span>No internal updates yet</span><strong>--</strong></div>";
}

function renderToolCalls(calls) {
  $("toolCalls").innerHTML = calls.length
    ? calls.map((call) => `<div class="run-item"><span>${escapeHtml(call.tool)} / ${escapeHtml(call.operation)}</span><strong>${escapeHtml(call.status)}</strong></div>`).join("")
    : "<div class=\"run-item\"><span>No tool calls yet</span><strong>--</strong></div>";
}

=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
async function approvePending() {
  if (!state.pendingManual) return;
  const result = state.pendingManual;
  const payload = {
    customer_id: $("customerId").value.trim(),
    issue_type: result.issue_type,
    recommended_action: result.decision.recommended_action,
    approver: $("approver").value.trim() || "Manual approver",
    note: $("approvalNote").value.trim(),
  };

  $("approveBtn").disabled = true;
  $("approveBtn").textContent = "Executing";

  try {
    const response = await fetch("/manual/execute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) throw new Error(`Manual execution failed: ${response.status}`);
    const data = await response.json();
    $("ticket").textContent = data.ticket_id;
    $("approval").textContent = "approved";
    $("approvalHint").textContent = `Approved by ${data.approver}. Ticket ${data.ticket_id} created.`;
    addMessage("agent", "Manual action executed", `Approval accepted. I created incident ${data.ticket_id} and attached the approver note for audit.`);
    state.pendingManual = null;
    await loadRuns();
    await loadStats();
  } catch (error) {
    toast(error.message);
    $("approveBtn").disabled = false;
  } finally {
    $("approveBtn").textContent = "Approve and execute";
  }
}

async function loadStats() {
  try {
    const response = await fetch("/stats");
    const stats = await response.json();
    $("resolvedCount").textContent = stats.auto_resolved ?? 0;
    $("queryCount").textContent = stats.total_queries ?? 0;
    $("ticketCount").textContent = stats.tickets_created ?? 0;
    $("pendingCount").textContent = stats.pending_review ?? 0;
  } catch {
    $("resolvedCount").textContent = "--";
    $("queryCount").textContent = "--";
    $("ticketCount").textContent = "--";
    $("pendingCount").textContent = "--";
  }
}

async function loadRuns() {
  try {
    const response = await fetch("/runs");
    const runs = await response.json();
    $("runs").innerHTML = runs.length
      ? runs.slice(0, 6).map((run) => `<div class="run-item"><span>${formatIssue(run.issue_type)}</span><strong>${run.outcome}</strong></div>`).join("")
      : "<div class=\"run-item\"><span>No runs yet</span><strong>--</strong></div>";
  } catch {
    $("runs").innerHTML = "<div class=\"run-item\"><span>Unable to load runs</span><strong>--</strong></div>";
  }
}

function resetChat() {
  state.result = null;
  state.pendingManual = null;
  $("chatStream").innerHTML = "";
<<<<<<< HEAD
  addMessage("agent", "OmniSupport AI", "New case started. Send the next customer issue when ready.");
=======
  addMessage("agent", "ERA Assistant", "New case started. Send the next customer issue when ready.");
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
  $("approveBtn").disabled = true;
  $("approvalHint").textContent = "No manual approval waiting.";
  $("ticket").textContent = "--";
  $("issueType").textContent = "No case";
  $("approval").textContent = "Waiting";
  $("decisionTitle").textContent = "Resolution will appear here";
  $("decisionRationale").textContent = "The agent will explain why it selected a playbook and whether a human approval is required.";
<<<<<<< HEAD
  renderActiveTickets([]);
  renderWorkflow({});
  renderInternalUpdates([]);
  renderToolCalls([]);
  $("agentProvider").textContent = "Groq ready";
  $("agentRoom").innerHTML = `
    <div class="agent-card idle"><strong>Supervisor</strong><span>Waiting for customer message</span></div>
    <div class="agent-card idle"><strong>Ticket Agent</strong><span>Ready to check active cases</span></div>
    <div class="agent-card idle"><strong>Knowledge Agent</strong><span>Ready to search vector knowledge</span></div>
  `;
=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
}

document.querySelectorAll(".scenario").forEach((button) => {
  button.addEventListener("click", () => {
    $("messageInput").value = button.dataset.message;
    $("messageInput").focus();
  });
});

$("chatForm").addEventListener("submit", (event) => {
  event.preventDefault();
  const message = $("messageInput").value;
  $("messageInput").value = "";
  sendIssue(message);
});

$("approveBtn").addEventListener("click", approvePending);
$("newChatBtn").addEventListener("click", resetChat);
$("loadRunsBtn").addEventListener("click", loadRuns);

checkHealth();
loadRuns();
loadStats();
<<<<<<< HEAD
renderWorkflow({});
=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
