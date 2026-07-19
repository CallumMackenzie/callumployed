const statsEl = document.querySelector("#stats");
const statusListEl = document.querySelector("#status-list");
const statusTabsEl = document.querySelector("#status-tabs");
const searchToggle = document.querySelector("#search-toggle");
const searchDialog = document.querySelector("#search-dialog");
const searchBackdrop = document.querySelector("#search-backdrop");
const searchForm = document.querySelector("#search-form");
const searchInput = document.querySelector("#search-input");
const closeSearchButton = document.querySelector("#close-search");
const materialsPanel = document.querySelector("#materials-panel");
const materialsToggle = document.querySelector("#materials-toggle");
const materialsBody = document.querySelector("#materials-body");
const materialsSummary = document.querySelector("#materials-summary");
const resumeMeta = document.querySelector("#resume-meta");
const resumeUpload = document.querySelector("#resume-upload");
const resumeUploadButton = document.querySelector("#resume-upload-button");
const coverLetterMeta = document.querySelector("#cover-letter-meta");
const coverLetterUpload = document.querySelector("#cover-letter-upload");
const coverLetterUploadButton = document.querySelector("#cover-letter-upload-button");
const coverLetterList = document.querySelector("#cover-letter-list");
const reviewDiscoveredButton = document.querySelector("#review-discovered");
const reviewView = document.querySelector("#review-view");
const reviewHeading = document.querySelector("#review-heading");
const reviewProgress = document.querySelector("#review-progress");
const reviewCard = document.querySelector("#review-card");
const closeReviewButton = document.querySelector("#close-review");
const scanAllButton = document.querySelector("#scan-all-button");
const scanStatusBar = document.querySelector("#scan-status-bar");
const scanStatusText = document.querySelector("#scan-status-text");
const scanLastTime = document.querySelector("#scan-last-time");
const toggleAllButton = document.querySelector("#toggle-all");
const collapseEmptyButton = document.querySelector("#collapse-empty");

const REVIEW_LATER_RECOMMENDATION_THRESHOLD = 3;

let hideEmpty = true;
let trackerData = null;
let masterResume = null;
let coverLetterExamples = [];
let reviewQueue = [];
let materialsInitialized = false;
let scanStatusPoll = null;
let wasScanning = false;

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

function renderLinkIcon() {
  return `
    <svg class="role-link-icon" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M7 17 17 7"></path>
      <path d="M8 7h9v9"></path>
    </svg>
  `;
}

function renderRoleTitle(title, url, className) {
  const label = `<span class="role-title-text">${escapeHtml(title)}</span>`;
  if (!url) return `<span class="${className}">${label}</span>`;
  return `<a class="${className}" href="${escapeHtml(url)}" target="_blank" rel="noreferrer">${label}${renderLinkIcon()}</a>`;
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

function renderMasterResume(resume, message = "") {
  masterResume = resume;
  resumeUploadButton.textContent = resume ? "Replace" : "Upload";
  if (message) {
    resumeMeta.textContent = message;
    return;
  }
  if (!resume) {
    resumeMeta.textContent = "No resume uploaded";
    return;
  }
  const updated = formatCompactDate(resume.updated_at);
  const size = formatFileSize(resume.content_bytes);
  resumeMeta.textContent = [resume.filename, size, updated].filter(Boolean).join(" | ");
}

function renderCoverLetterExamples(examples, message = "") {
  coverLetterExamples = Array.isArray(examples) ? examples : [];
  coverLetterUploadButton.textContent = coverLetterExamples.length > 0 ? "Add" : "Upload";
  if (message) {
    coverLetterMeta.textContent = message;
  } else if (coverLetterExamples.length === 0) {
    coverLetterMeta.textContent = "No examples uploaded";
  } else {
    coverLetterMeta.textContent = `${coverLetterExamples.length} ${coverLetterExamples.length === 1 ? "example" : "examples"} stored`;
  }

  const visibleExamples = coverLetterExamples.slice(0, 3);
  const hiddenCount = Math.max(coverLetterExamples.length - visibleExamples.length, 0);
  coverLetterList.innerHTML = visibleExamples
    .map((example) => {
      const size = formatFileSize(example.content_bytes);
      return `
        <li title="${escapeHtml(example.filename)}">
          <span>${escapeHtml(example.filename)}</span>
          <small>${escapeHtml(size)}</small>
        </li>
      `;
    })
    .join("");
  if (hiddenCount > 0) {
    coverLetterList.insertAdjacentHTML(
      "beforeend",
      `<li class="examples-more"><span>+${hiddenCount} more</span></li>`,
    );
  }
}

function renderApplicationMaterials(payload, options = {}) {
  renderMasterResume(payload?.master_resume ?? null);
  renderCoverLetterExamples(payload?.cover_letter_examples ?? []);
  updateMaterialsSummary();
  if (!materialsInitialized || options.applyDefaultCollapsed) {
    setMaterialsCollapsed(Boolean(payload?.ui?.default_collapsed));
    materialsInitialized = true;
  }
}

function updateMaterialsSummary() {
  const resumeText = masterResume ? "resume ready" : "no resume";
  const exampleCount = coverLetterExamples.length;
  const coverText =
    exampleCount === 0
      ? "no cover letters"
      : `${exampleCount} cover ${exampleCount === 1 ? "letter" : "letters"}`;
  materialsSummary.textContent = `${resumeText} | ${coverText}`;
}

function setMaterialsCollapsed(collapsed) {
  materialsPanel.classList.toggle("collapsed", collapsed);
  materialsToggle.setAttribute("aria-expanded", String(!collapsed));
  materialsToggle.querySelector(".materials-chevron").textContent = collapsed ? ">" : "v";
  materialsBody.hidden = collapsed;
}

function formatFileSize(bytes) {
  if (!Number.isFinite(bytes)) return "";
  if (bytes < 1024) return `${bytes} B`;
  return `${Math.round(bytes / 1024)} KB`;
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
                  ${renderRoleTitle(job.title, job.role_url, "job-title")}
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
  updateToggleAllButton();
  updateReviewButton(data.statuses);
}

function renderScanStatus(payload) {
  const scanning = Boolean(payload?.scanning);
  const completed = Number(payload?.completed_companies ?? 0);
  const total = Number(payload?.total_companies ?? 0);
  const failed = Number(payload?.failed_companies ?? 0);

  scanAllButton.disabled = scanning;
  scanAllButton.textContent = scanning ? "Scanning..." : "Scan roles";
  scanStatusBar.hidden = !scanning;
  scanStatusBar.classList.toggle("scanning", scanning);
  scanStatusBar.classList.toggle("scan-error", !scanning && Boolean(payload?.error));

  if (scanning) {
    const progressText = total > 0 ? ` ${completed}/${total}` : "";
    const failureText = failed > 0 ? `, ${failed} failed` : "";
    scanStatusText.textContent = `Scanning roles${progressText}${failureText}`;
  } else if (payload?.error) {
    scanStatusText.textContent = "Last scan had errors";
  } else {
    scanStatusText.textContent = "Scan idle";
  }

  const lastScanAt = payload?.last_scan_at;
  scanLastTime.textContent = lastScanAt ? `Last scan: ${formatCompactDate(lastScanAt)}` : "Last scan: never";

  if (wasScanning && !scanning) {
    loadTracker(getActiveSearchQuery()).catch(() => {});
  }
  wasScanning = scanning;
}

async function loadScanStatus() {
  const response = await fetch("/api/scan/status");
  if (response.status === 404) {
    scanAllButton.disabled = true;
    scanStatusBar.hidden = true;
    scanStatusBar.classList.add("scan-error");
    scanStatusText.textContent = "Restart server to enable scanning";
    return;
  }
  if (!response.ok) throw new Error("Scan status request failed");
  renderScanStatus(await response.json());
}

function startScanStatusPolling() {
  if (scanStatusPoll !== null) return;
  scanStatusPoll = window.setInterval(() => {
    loadScanStatus().catch(() => {});
  }, 3000);
}

async function startScanAll() {
  scanAllButton.disabled = true;
  scanAllButton.textContent = "Scanning...";
  try {
    const response = await fetch("/api/scan/all", { method: "POST" });
    if (response.status === 404) {
      scanAllButton.disabled = true;
      scanAllButton.textContent = "Scan roles";
      scanStatusBar.hidden = true;
      scanStatusBar.classList.add("scan-error");
      scanStatusText.textContent = "Restart server to enable scanning";
      return;
    }
    if (!response.ok && response.status !== 409) throw new Error("Scan start failed");
    renderScanStatus(await response.json());
    startScanStatusPolling();
  } catch {
    scanAllButton.disabled = false;
    scanAllButton.textContent = "Scan roles";
    scanStatusBar.hidden = true;
    scanStatusBar.classList.add("scan-error");
    scanStatusText.textContent = "Could not start scan";
  }
}

async function loadTracker(query = "") {
  statusListEl.innerHTML = '<p class="empty-copy">Loading jobs...</p>';
  const params = new URLSearchParams();
  if (query) params.set("q", query);
  const response = await fetch(`/api/tracker?${params.toString()}`);
  if (!response.ok) throw new Error("Tracker request failed");
  render(await response.json());
}

async function loadMasterResume() {
  const response = await fetch("/api/master-resume");
  if (!response.ok) throw new Error("Master resume request failed");
  const payload = await response.json();
  renderMasterResume(payload.master_resume);
}

async function loadCoverLetterExamples() {
  const response = await fetch("/api/cover-letter-examples");
  if (!response.ok) throw new Error("Cover letter examples request failed");
  const payload = await response.json();
  renderCoverLetterExamples(payload.cover_letter_examples);
}

async function loadApplicationMaterials(options = {}) {
  const response = await fetch("/api/application-materials");
  if (!response.ok) throw new Error("Application materials request failed");
  const payload = await response.json();
  renderApplicationMaterials(payload, options);
}

async function uploadMasterResume(file) {
  if (!file) return;
  if (!file.name.toLowerCase().endsWith(".tex")) {
    renderMasterResume(masterResume, "Resume must be a .tex file.");
    return;
  }

  resumeUploadButton.disabled = true;
  renderMasterResume(masterResume, "Uploading...");
  try {
    const content = await file.text();
    const response = await fetch("/api/master-resume", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        filename: file.name,
        content,
      }),
    });
    if (!response.ok) throw new Error("Master resume upload failed");
    await loadApplicationMaterials();
  } catch {
    renderMasterResume(masterResume, "Could not save resume.");
    updateMaterialsSummary();
  } finally {
    resumeUpload.value = "";
    resumeUploadButton.disabled = false;
  }
}

async function uploadCoverLetterExamples(files) {
  const selectedFiles = Array.from(files ?? []);
  if (selectedFiles.length === 0) return;

  coverLetterUploadButton.disabled = true;
  renderCoverLetterExamples(
    coverLetterExamples,
    `Uploading ${selectedFiles.length} ${selectedFiles.length === 1 ? "example" : "examples"}...`,
  );
  try {
    for (const file of selectedFiles) {
      const content = await file.text();
      const response = await fetch("/api/cover-letter-examples", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          filename: file.name,
          content,
        }),
      });
      if (!response.ok) throw new Error("Cover letter example upload failed");
    }
    await loadApplicationMaterials();
  } catch {
    renderCoverLetterExamples(coverLetterExamples, "Could not save every example.");
    updateMaterialsSummary();
  } finally {
    coverLetterUpload.value = "";
    coverLetterUploadButton.disabled = false;
  }
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

resumeUploadButton.addEventListener("click", () => {
  resumeUpload.click();
});

resumeUpload.addEventListener("change", () => {
  uploadMasterResume(resumeUpload.files?.[0]);
});

coverLetterUploadButton.addEventListener("click", () => {
  coverLetterUpload.click();
});

coverLetterUpload.addEventListener("change", () => {
  uploadCoverLetterExamples(coverLetterUpload.files);
});

materialsToggle.addEventListener("click", () => {
  setMaterialsCollapsed(materialsToggle.getAttribute("aria-expanded") === "true");
});

scanAllButton.addEventListener("click", () => {
  startScanAll();
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
  updateToggleAllButton();
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
  reviewDiscoveredButton.setAttribute("aria-label", "Review discovered");
  reviewDiscoveredButton.innerHTML = '<span class="review-discovered-label">Review discovered</span>';
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
      ${renderRoleTitle(current.title, current.role_url, "review-role-title")}
    </div>
    <dl class="review-details review-primary-details">
      ${renderReviewDetail("Location", current.location, false, "review-location-detail")}
      ${renderReviewDetail("First", formatCompactDate(current.first_seen_at))}
      ${renderReviewDetail("Last", formatCompactDate(current.last_seen_at))}
    </dl>
    ${renderReviewDescription(current.description)}
    <dl class="review-details review-technical-details">
      ${renderReviewDetail("Notes", current.notes, false, "review-wide-detail")}
      ${renderReviewDetail("Company ID", current.company_id)}
      ${renderReviewDetail("Role ID", current.id)}
      ${renderReviewDetail("Status", current.role_status)}
      ${renderReviewDetail("Posting ID", current.posting_id)}
      ${renderReviewDetail("Created", formatCompactDate(current.created_at))}
      ${renderReviewDetail("Updated", formatCompactDate(current.updated_at))}
      ${renderReviewDetail("URL", current.role_url, true, "review-wide-detail")}
    </dl>
  `;
}

function getReviewLaterRecommendation(role) {
  const count = Number(role.review_later_count ?? 0);
  if (count <= REVIEW_LATER_RECOMMENDATION_THRESHOLD) return "";
  return `Role review has been postponed ${count} times. It is recommended to set it to disinterested.`;
}

function renderReviewDetail(label, value, isLink = false, className = "") {
  if (!value) return "";
  const content = isLink
    ? `<a href="${escapeHtml(value)}" target="_blank" rel="noreferrer">${escapeHtml(value)}</a>`
    : escapeHtml(value);
  return `
    <div class="review-detail ${escapeHtml(className)}">
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

function statusPaneToggles() {
  return Array.from(document.querySelectorAll(".pane-toggle"));
}

function hasExpandedStatusPane() {
  return statusPaneToggles().some((toggle) => toggle.getAttribute("aria-expanded") === "true");
}

function updateToggleAllButton() {
  toggleAllButton.textContent = hasExpandedStatusPane() ? "Collapse all" : "Expand all";
}

function expandAllStatusPanes() {
  document.querySelectorAll(".pane-toggle").forEach((toggle) => {
    toggle.setAttribute("aria-expanded", "true");
    toggle.querySelector(".chevron").textContent = "v";
    toggle.parentElement.querySelector(".pane-body").hidden = false;
  });
}

function collapseAllStatusPanes() {
  document.querySelectorAll(".job[open]").forEach((job) => {
    job.open = false;
  });
  document.querySelectorAll(".pane-toggle").forEach((toggle) => {
    toggle.setAttribute("aria-expanded", "false");
    toggle.querySelector(".chevron").textContent = ">";
    toggle.parentElement.querySelector(".pane-body").hidden = true;
  });
}

toggleAllButton.addEventListener("click", () => {
  if (hasExpandedStatusPane()) {
    collapseAllStatusPanes();
  } else {
    expandAllStatusPanes();
  }
  updateToggleAllButton();
});

collapseEmptyButton.addEventListener("click", () => {
  hideEmpty = !hideEmpty;
  collapseEmptyButton.textContent = hideEmpty ? "Show empty" : "Hide empty";
  if (trackerData) renderStatuses(trackerData.statuses);
});

loadTracker().catch(() => {
  statusListEl.innerHTML = '<p class="empty-copy">Could not load jobs.</p>';
});

loadApplicationMaterials({ applyDefaultCollapsed: true }).catch(() => {
  renderMasterResume(null, "Could not load resume.");
  renderCoverLetterExamples([], "Could not load cover letter examples.");
  updateMaterialsSummary();
});

loadScanStatus()
  .then(() => {
    startScanStatusPolling();
  })
  .catch(() => {
    scanStatusText.textContent = "Could not load scan status";
  });
