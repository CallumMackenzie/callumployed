const statsEl = document.querySelector("#stats");
const statusListEl = document.querySelector("#status-list");
const statusTabsEl = document.querySelector("#status-tabs");
const searchForm = document.querySelector("#search-form");
const searchInput = document.querySelector("#search-input");
const expandAllButton = document.querySelector("#expand-all");
const collapseAllButton = document.querySelector("#collapse-all");
const collapseEmptyButton = document.querySelector("#collapse-empty");

let hideEmpty = true;
let trackerData = null;

function formatDate(value) {
  if (!value) return "";
  return new Intl.DateTimeFormat(undefined, {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(value));
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderStats(stats) {
  const items = [
    ["Companies", stats.companies_total],
    ["Jobs", stats.jobs_total],
    ["Applications", stats.applications_total],
  ];
  statsEl.innerHTML = items
    .map(([label, value]) => `<dl class="stat"><dt>${escapeHtml(label)}</dt><dd>${value}</dd></dl>`)
    .join("");
}

function renderTabs(statuses) {
  statusTabsEl.innerHTML = statuses
    .map(
      (status) =>
        `<button class="status-tab" type="button" data-target="${escapeHtml(status.key)}" data-bucket="${escapeHtml(status.key)}">${escapeHtml(status.label)} <strong>${status.count}</strong></button>`,
    )
    .join("");
}

function renderStatuses(statuses) {
  statusListEl.innerHTML = statuses
    .map((status) => {
      const jobs = status.jobs
        .map(
          (job) => `
            <details class="job">
              <summary class="job-summary">
                <span class="job-chevron">></span>
                <span class="job-identity">
                  <span class="job-company">[${escapeHtml(job.company_name)}]</span>
                  <a class="job-title" href="${escapeHtml(job.role_url)}" target="_blank" rel="noreferrer">${escapeHtml(job.title)}</a>
                </span>
              </summary>
              <div class="job-detail">
                ${status.key === "discovered" ? renderDiscoveredActions(job) : ""}
                ${status.key === "interested" ? renderInterestedActions(job) : ""}
                ${status.key === "applied" ? renderAppliedActions(job) : ""}
                ${status.key === "OA" ? renderOaActions(job) : ""}
                ${status.key === "interview" ? renderInterviewActions(job) : ""}
                <dl>
                  ${
                    job.location
                      ? `<div>
                          <dt>Location</dt>
                          <dd>${escapeHtml(job.location)}</dd>
                        </div>`
                      : ""
                  }
                  <div>
                    <dt>Updated</dt>
                    <dd>${formatDate(job.updated_at)}</dd>
                  </div>
                </dl>
              </div>
            </details>
          `,
        )
        .join("");

      return `
        <section class="status-pane ${status.count === 0 ? "empty" : ""} ${hideEmpty ? "hidden-empty" : ""}" id="status-${escapeHtml(status.key)}" data-bucket="${escapeHtml(status.key)}">
          <button class="pane-toggle" type="button" aria-expanded="false">
            <span class="chevron">></span>
            <span class="pane-title">${escapeHtml(status.label)}</span>
            <span class="count">${status.count}</span>
          </button>
          <div class="pane-body" hidden>
            ${jobs ? `<div class="jobs">${jobs}</div>` : `<p class="empty-copy">No jobs in this status.</p>`}
          </div>
        </section>
      `;
    })
    .join("");
}

function renderDiscoveredActions(job) {
  return `
    <div class="job-actions" aria-label="Discovered role actions">
      <button class="job-action" type="button" data-role-id="${job.id}" data-status="interested">Interested</button>
      <button class="job-action" type="button" data-role-id="${job.id}" data-status="disinterested">Disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${job.id}" data-status="closed">Closed</button>
    </div>
  `;
}

function renderInterestedActions(job) {
  return `
    <div class="job-actions" aria-label="Interested role actions">
      <button class="job-action" type="button" data-role-id="${job.id}" data-status="applied">Applied</button>
      <button class="job-action" type="button" data-role-id="${job.id}" data-status="disinterested">Disinterested</button>
    </div>
  `;
}

function renderAppliedActions(job) {
  return `
    <div class="job-actions" aria-label="Applied role actions">
      <button class="job-action" type="button" data-role-id="${job.id}" data-status="OA">OA</button>
      <button class="job-action" type="button" data-role-id="${job.id}" data-status="interview">Interview</button>
      <button class="job-action danger" type="button" data-role-id="${job.id}" data-status="rejected">Rejected</button>
    </div>
  `;
}

function renderOaActions(job) {
  return `
    <div class="job-actions" aria-label="OA role actions">
      <button class="job-action" type="button" data-role-id="${job.id}" data-status="interview">Interview</button>
      <button class="job-action danger" type="button" data-role-id="${job.id}" data-status="rejected">Rejected</button>
    </div>
  `;
}

function renderInterviewActions(job) {
  return `
    <div class="job-actions" aria-label="Interview role actions">
      <button class="job-action danger" type="button" data-role-id="${job.id}" data-status="rejected">Rejected</button>
      <button class="job-action success" type="button" data-role-id="${job.id}" data-status="offer">Offer</button>
    </div>
  `;
}

function render(data) {
  trackerData = data;
  searchInput.value = data.query;
  renderStats(data.stats);
  renderTabs(data.statuses);
  renderStatuses(data.statuses);
}

async function loadTracker(query = "") {
  statusListEl.innerHTML = '<p class="empty-copy">Loading jobs...</p>';
  const params = new URLSearchParams();
  if (query) params.set("q", query);
  const response = await fetch(`/api/tracker?${params.toString()}`);
  if (!response.ok) throw new Error("Tracker request failed");
  render(await response.json());
}

searchForm.addEventListener("submit", (event) => {
  event.preventDefault();
  loadTracker(searchInput.value.trim());
});

statusTabsEl.addEventListener("click", (event) => {
  const button = event.target.closest("[data-target]");
  if (!button) return;
  document.querySelector(`#status-${button.dataset.target}`)?.scrollIntoView({
    behavior: "smooth",
    block: "start",
  });
});

statusListEl.addEventListener("click", (event) => {
  const action = event.target.closest(".job-action");
  if (action) {
    updateRoleStatus(action);
    return;
  }

  const toggle = event.target.closest(".pane-toggle");
  if (!toggle) return;
  const body = toggle.parentElement.querySelector(".pane-body");
  const expanded = toggle.getAttribute("aria-expanded") === "true";
  toggle.setAttribute("aria-expanded", String(!expanded));
  toggle.querySelector(".chevron").textContent = expanded ? ">" : "v";
  body.hidden = expanded;
});

async function updateRoleStatus(button) {
  const { roleId, status } = button.dataset;
  if (!roleId || !status) return;

  const actions = button.closest(".job-actions");
  actions.querySelectorAll("button").forEach((item) => {
    item.disabled = true;
  });
  button.textContent = "Updating...";

  try {
    const response = await fetch(`/api/roles/${encodeURIComponent(roleId)}/status`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    });
    if (!response.ok) throw new Error("Status update failed");
    await loadTracker(searchInput.value.trim());
  } catch {
    actions.querySelectorAll("button").forEach((item) => {
      item.disabled = false;
    });
    button.textContent =
      status === "disinterested"
        ? "Disinterested"
        : status.charAt(0).toUpperCase() + status.slice(1);
  }
}

expandAllButton.addEventListener("click", () => {
  document.querySelectorAll(".pane-toggle").forEach((toggle) => {
    toggle.setAttribute("aria-expanded", "true");
    toggle.querySelector(".chevron").textContent = "v";
    toggle.parentElement.querySelector(".pane-body").hidden = false;
  });
});

collapseAllButton.addEventListener("click", () => {
  document.querySelectorAll(".job[open]").forEach((job) => {
    job.open = false;
  });
  document.querySelectorAll(".pane-toggle").forEach((toggle) => {
    toggle.setAttribute("aria-expanded", "false");
    toggle.querySelector(".chevron").textContent = ">";
    toggle.parentElement.querySelector(".pane-body").hidden = true;
  });
});

collapseEmptyButton.addEventListener("click", () => {
  hideEmpty = !hideEmpty;
  collapseEmptyButton.textContent = hideEmpty ? "Show empty" : "Hide empty";
  if (trackerData) renderStatuses(trackerData.statuses);
});

loadTracker().catch(() => {
  statusListEl.innerHTML = '<p class="empty-copy">Could not load jobs.</p>';
});
