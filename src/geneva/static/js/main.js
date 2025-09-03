let currentUser = null;

// ---- helper: safe fetch ----
async function safeFetch(url, options) {
  try {
    const res = await fetch(url, options);
    const data = await res.json();
    if (data.error) throw new Error(data.error);
    return data;
  } catch (err) {
    return { error: err.message };
  }
}

// ---- LOGIN ----
async function login() {
  const username = document.getElementById("username").value;
  const apiKey = document.getElementById("api_key").value;

  const data = await safeFetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, api_key: apiKey })
  });

  const msg = document.getElementById("login-message");
  if (data.error) {
    msg.innerText = `❌ ${data.error}`;
  } else {
    msg.innerText = `✅ ${data.message}`;
    currentUser = username;
  }
}

// ---- CREATE QUERY ----
async function createQuery() {
  if (!currentUser) {
    alert("Login first!");
    return;
  }

  const fetchBtn = document.querySelector("#association-section button");
  fetchBtn.disabled = true;
  fetchBtn.innerText = "Fetching...";

  const gene = document.getElementById("gene").value;
  const disease = document.getElementById("disease").value;

  const data = await safeFetch("/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: currentUser, gene, disease })
  });

  fetchBtn.disabled = false;
  fetchBtn.innerText = "Fetch";

  const summaryText = document.getElementById("summary-text");
  const keyFindings = document.getElementById("key-findings");
  const confidenceEl = document.getElementById("confidence");
  const serviceJson = document.getElementById("service-json");
  const serviceDetails = document.getElementById("service-details");
  const resultEl = document.getElementById("association-result");

  if (data.error) {
    resultEl.style.display = "block";
    resultEl.innerText = `❌ ${data.error}`;
    summaryText.innerText = "";
    keyFindings.innerHTML = "";
    confidenceEl.innerText = "";
    serviceJson.innerText = "";
    serviceDetails.open = false;
    return;
  }

  // Correct paths
  const llm = data.data.llm_response;
  const service = data.data.service_response;

  // LLM summary
  summaryText.innerText = llm.summary_text || "";
  keyFindings.innerHTML = "";
  (llm.key_findings || []).forEach(f => {
    const li = document.createElement("li");
    li.innerText = f;
    keyFindings.appendChild(li);
  });
  confidenceEl.innerText = llm.confidence !== null ? `Confidence: ${llm.confidence}` : "";

  // Service response
  serviceJson.innerText = service ? JSON.stringify(service, null, 2) : "No service response";
  serviceDetails.open = false;

  // Hide raw result
  resultEl.style.display = "none";
}

// ---- LOAD USER QUERIES ----
async function loadQueries() {
  if (!currentUser) {
    alert("Login first!");
    return;
  }

  const data = await safeFetch(`/queries/${currentUser}`);
  const historyDiv = document.getElementById("history");
  historyDiv.innerHTML = "";

  if (data.error) {
    historyDiv.innerHTML = `<p>❌ ${data.error}</p>`;
    return;
  }

  if (!data.data || data.data.length === 0) {
    historyDiv.innerHTML = "<p>No queries found.</p>";
    return;
  }

  // Most recent first
  data.data.slice().reverse().forEach(q => {
    const card = document.createElement("div");
    card.className = "analysis-card";
    card.innerHTML = `
      <strong>${q.gene} → ${q.disease}</strong><br>
      <small>${q.created_at}</small><br>
      <div><strong>Summary:</strong><pre>${JSON.stringify(q.llm_response, null, 2)}</pre></div>
      <details>
        <summary style="cursor:pointer; font-weight:bold;">🔍 Show full service response</summary>
        <pre class="history-service" style="max-height: 300px; overflow-x:auto;">${JSON.stringify(q.service_response || {}, null, 2)}</pre>
      </details>
    `;
    historyDiv.appendChild(card);
  });
}
