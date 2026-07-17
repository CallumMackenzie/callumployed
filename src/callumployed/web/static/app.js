const statsEl = document.querySelector("#stats");
const statusListEl = document.querySelector("#status-list");
const statusTabsEl = document.querySelector("#status-tabs");
const searchForm = document.querySelector("#search-form");
const searchInput = document.querySelector("#search-input");
const expandAllButton = document.querySelector("#expand-all");
const collapseEmptyButton = document.querySelector("#collapse-empty");

let hideEmpty = false;
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
          <button class="pane-toggle" type="button" aria-expanded="true">
            <span class="chevron">v</span>
            <span class="pane-title">${escapeHtml(status.label)}</span>
            <span class="count">${status.count}</span>
          </button>
          <div class="pane-body">
            ${jobs ? `<div class="jobs">${jobs}</div>` : `<p class="empty-copy">No jobs in this status.</p>`}
          </div>
        </section>
      `;
    })
    .join("");
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
  const toggle = event.target.closest(".pane-toggle");
  if (!toggle) return;
  const body = toggle.parentElement.querySelector(".pane-body");
  const expanded = toggle.getAttribute("aria-expanded") === "true";
  toggle.setAttribute("aria-expanded", String(!expanded));
  toggle.querySelector(".chevron").textContent = expanded ? ">" : "v";
  body.hidden = expanded;
});

expandAllButton.addEventListener("click", () => {
  document.querySelectorAll(".pane-toggle").forEach((toggle) => {
    toggle.setAttribute("aria-expanded", "true");
    toggle.querySelector(".chevron").textContent = "v";
    toggle.parentElement.querySelector(".pane-body").hidden = false;
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
