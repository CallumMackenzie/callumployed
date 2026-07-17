const statsEl = document.querySelector("#stats");
const statusListEl = document.querySelector("#status-list");
const statusTabsEl = document.querySelector("#status-tabs");
const searchToggle = document.querySelector("#search-toggle");
const searchDialog = document.querySelector("#search-dialog");
const searchBackdrop = document.querySelector("#search-backdrop");
const searchForm = document.querySelector("#search-form");
const searchInput = document.querySelector("#search-input");
const closeSearchButton = document.querySelector("#close-search");
const reviewDiscoveredButton = document.querySelector("#review-discovered");
const reviewView = document.querySelector("#review-view");
const reviewHeading = document.querySelector("#review-heading");
const reviewProgress = document.querySelector("#review-progress");
const reviewCard = document.querySelector("#review-card");
const closeReviewButton = document.querySelector("#close-review");
const expandAllButton = document.querySelector("#expand-all");
const collapseAllButton = document.querySelector("#collapse-all");
const collapseEmptyButton = document.querySelector("#collapse-empty");

const REVIEW_LATER_RECOMMENDATION_THRESHOLD = 3;

let hideEmpty = true;
let trackerData = null;
let reviewQueue = [];

function getActiveSearchQuery() {
  return trackerData?.query?.trim() ?? "";
}

function updateSearchButton() {
  const active = Boolean(getActiveSearchQuery());
  searchToggle.classList.toggle("search-active", active);
  searchToggle.setAttribute("aria-label", active ? "Clear search" : "Search jobs");
}

function openSearchDialog() {
  searchInput.value = getActiveSearchQuery();
  searchDialog.hidden = false;
  searchForm.hidden = false;
  searchInput.focus();
  searchInput.select();
}

function closeSearchDialog() {
  searchDialog.hidden = true;
  searchForm.hidden = true;
  searchToggle.focus();
}

function formatDate(value) {
  if (!value) return "";
  return new Intl.DateTimeFormat(undefined, {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(value));
}

function formatCompactDate(value) {
  if (!value) return "";
  return new Intl.DateTimeFormat(undefined, {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  })
    .format(new Date(value))
    .replace(", ", " ");
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
    <div class="job-actions job-actions-nowrap" aria-label="Discovered role actions">
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
    <div class="job-actions job-actions-nowrap" aria-label="Applied role actions">
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
  updateSearchButton();
  renderStats(data.stats);
  renderTabs(data.statuses);
  renderStatuses(data.statuses);
  updateReviewButton(data.statuses);
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
  closeSearchDialog();
});

searchToggle.addEventListener("click", () => {
  if (getActiveSearchQuery()) {
    loadTracker();
    return;
  }
  openSearchDialog();
});

searchInput.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") return;
  event.stopPropagation();
  closeSearchDialog();
});

closeSearchButton.addEventListener("click", closeSearchDialog);

searchBackdrop.addEventListener("click", closeSearchDialog);

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
    await loadTracker(getActiveSearchQuery());
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

function updateReviewButton(statuses) {
  const discovered = getDiscoveredJobs(statuses);
  reviewDiscoveredButton.disabled = discovered.length === 0;
  reviewDiscoveredButton.textContent =
    discovered.length === 0 ? "Review discovered" : `Review discovered (${discovered.length})`;
}

function getDiscoveredJobs(statuses = trackerData?.statuses ?? []) {
  return statuses.find((status) => status.key === "discovered")?.jobs ?? [];
}

function openReviewView() {
  reviewQueue = [...getDiscoveredJobs()];
  reviewView.hidden = false;
  document.body.classList.add("review-open");
  renderReviewRole();
}

function closeReviewView() {
  reviewView.hidden = true;
  document.body.classList.remove("review-open");
  reviewQueue = [];
}

function renderReviewRole(message = "") {
  const current = reviewQueue[0];
  const total = reviewQueue.length;
  const reviewLaterMessage = current ? getReviewLaterRecommendation(current) : "";
  reviewHeading.textContent = total > 0 ? "Review queue" : "Review complete";
  reviewProgress.textContent =
    total > 0 ? `${total} discovered ${total === 1 ? "role" : "roles"} in queue` : "";

  reviewView.querySelectorAll(".review-action").forEach((button) => {
    button.disabled = total === 0;
  });

  if (!current) {
    reviewCard.innerHTML = `
      <div class="review-empty">
        <h3>No discovered jobs left.</h3>
        <p>Everything in this queue has been handled or moved out of discovered.</p>
      </div>
    `;
    return;
  }

  reviewCard.innerHTML = `
    ${message ? `<p class="review-message">${escapeHtml(message)}</p>` : ""}
    ${reviewLaterMessage ? `<p class="review-message review-message-warning">${escapeHtml(reviewLaterMessage)}</p>` : ""}
    <div class="review-title-row">
      <p class="review-company">${escapeHtml(current.company_name)}</p>
      <a class="review-role-title" href="${escapeHtml(current.role_url)}" target="_blank" rel="noreferrer">${escapeHtml(current.title)}</a>
    </div>
    <dl class="review-details">
      ${renderReviewDetail("Location", current.location)}
      ${renderReviewDetail("First", formatCompactDate(current.first_seen_at))}
      ${renderReviewDetail("Last", formatCompactDate(current.last_seen_at))}
      ${renderReviewDetail("Notes", current.notes)}
    </dl>
    ${renderReviewDescription(current.description)}
    <dl class="review-details review-technical-details">
      ${renderReviewDetail("Company ID", current.company_id)}
      ${renderReviewDetail("Role ID", current.id)}
      ${renderReviewDetail("Status", current.role_status)}
      ${renderReviewDetail("Posting ID", current.posting_id)}
      ${renderReviewDetail("Created", formatCompactDate(current.created_at))}
      ${renderReviewDetail("Updated", formatCompactDate(current.updated_at))}
      ${renderReviewDetail("URL", current.role_url, true)}
    </dl>
  `;
}

function getReviewLaterRecommendation(role) {
  const count = Number(role.review_later_count ?? 0);
  if (count <= REVIEW_LATER_RECOMMENDATION_THRESHOLD) return "";
  return `Role review has been postponed ${count} times. It is recommended to set it to disinterested.`;
}

function renderReviewDetail(label, value, isLink = false) {
  if (!value) return "";
  const content = isLink
    ? `<a href="${escapeHtml(value)}" target="_blank" rel="noreferrer">${escapeHtml(value)}</a>`
    : escapeHtml(value);
  return `
    <div class="review-detail">
      <dt>${escapeHtml(label)}</dt>
      <dd>${content}</dd>
    </div>
  `;
}

function renderReviewDescription(value) {
  if (!value) return "";
  return `
    <div class="review-detail review-description">
      <dt>Description</dt>
      <dd>${renderDescriptionMarkdown(value)}</dd>
    </div>
  `;
}

function renderDescriptionMarkdown(value) {
  const lines = String(value)
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
  const blocks = [];
  let listItems = [];

  const flushList = () => {
    if (listItems.length === 0) return;
    blocks.push(`<ul>${listItems.map((item) => `<li>${item}</li>`).join("")}</ul>`);
    listItems = [];
  };

  lines.forEach((line) => {
    const heading = line.match(/^#{2,3}\s+(.+)$/);
    if (heading) {
      flushList();
      blocks.push(`<h3>${escapeHtml(heading[1])}</h3>`);
      return;
    }

    const bullet = line.match(/^[-*]\s+(.+)$/);
    if (bullet) {
      listItems.push(escapeHtml(bullet[1]));
      return;
    }

    flushList();
    blocks.push(`<p>${escapeHtml(line)}</p>`);
  });
  flushList();
  return blocks.join("");
}

async function handleReviewAction(action) {
  const current = reviewQueue[0];
  if (!current) return;

  if (action === "later") {
    const buttons = reviewView.querySelectorAll(".review-action");
    buttons.forEach((button) => {
      button.disabled = true;
    });

    try {
      await recordRoleReviewLater(current.id);
      current.review_later_count = Number(current.review_later_count ?? 0) + 1;
      if (reviewQueue.length > 1) {
        reviewQueue.push(reviewQueue.shift());
        renderReviewRole("Moved to the back of the queue.");
      } else {
        renderReviewRole("Only one role is in the queue.");
      }
    } catch {
      renderReviewRole("Could not postpone that role. Try again.");
    } finally {
      reviewView.querySelectorAll(".review-action").forEach((button) => {
        button.disabled = reviewQueue.length === 0;
      });
    }
    return;
  }

  if (!["interested", "disinterested"].includes(action)) return;

  const buttons = reviewView.querySelectorAll(".review-action");
  buttons.forEach((button) => {
    button.disabled = true;
  });

  try {
    await updateRoleStatusById(current.id, action);
    reviewQueue.shift();
    renderReviewRole(action === "interested" ? "Marked interested." : "Marked disinterested.");
    await loadTracker(getActiveSearchQuery());
  } catch {
    buttons.forEach((button) => {
      button.disabled = false;
    });
    renderReviewRole("Could not update that role. Try again.");
  }
}

async function recordRoleReviewLater(roleId) {
  const response = await fetch(`/api/roles/${encodeURIComponent(roleId)}/review-later`, {
    method: "POST",
  });
  if (!response.ok) throw new Error("Review later update failed");
}

async function updateRoleStatusById(roleId, status) {
  const response = await fetch(`/api/roles/${encodeURIComponent(roleId)}/status`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
  if (!response.ok) throw new Error("Status update failed");
}

reviewDiscoveredButton.addEventListener("click", openReviewView);

closeReviewButton.addEventListener("click", closeReviewView);

reviewView.addEventListener("click", (event) => {
  const button = event.target.closest("[data-review-action]");
  if (!button) return;
  handleReviewAction(button.dataset.reviewAction);
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !searchDialog.hidden) closeSearchDialog();
  if (event.key === "Escape" && !reviewView.hidden) closeReviewView();
});

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
