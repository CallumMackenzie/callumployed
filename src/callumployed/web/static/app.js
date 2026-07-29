const statsEl = document.querySelector("#stats");
const statusListEl = document.querySelector("#status-list");
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
const resumeResourceMeta = document.querySelector("#resume-resource-meta");
const resumeResourceUpload = document.querySelector("#resume-resource-upload");
const resumeResourceUploadButton = document.querySelector("#resume-resource-upload-button");
const resumeResourceList = document.querySelector("#resume-resource-list");
const coverLetterMeta = document.querySelector("#cover-letter-meta");
const coverLetterUpload = document.querySelector("#cover-letter-upload");
const coverLetterUploadButton = document.querySelector("#cover-letter-upload-button");
const coverLetterList = document.querySelector("#cover-letter-list");
const reviewDiscoveredButton = document.querySelector("#review-discovered");
const prepInterestedButton = document.querySelector("#prep-interested");
const reviewView = document.querySelector("#review-view");
const reviewHeading = document.querySelector("#review-heading");
const reviewProgress = document.querySelector("#review-progress");
const reviewCard = document.querySelector("#review-card");
const closeReviewButton = document.querySelector("#close-review");
const prepView = document.querySelector("#prep-view");
const prepHeading = document.querySelector("#prep-heading");
const prepProgress = document.querySelector("#prep-progress");
const prepCard = document.querySelector("#prep-card");
const closePrepButton = document.querySelector("#close-prep");
const scanAllButton = document.querySelector("#scan-all-button");
const scanStatusBar = document.querySelector("#scan-status-bar");
const scanStatusText = document.querySelector("#scan-status-text");
const scanLastTime = document.querySelector("#scan-last-time");
const toggleAllButton = document.querySelector("#toggle-all");
const collapseEmptyButton = document.querySelector("#collapse-empty");
const toolbarSummary = document.querySelector("#toolbar-summary");
const settingsOpenButton = document.querySelector("#settings-open");
const settingsView = document.querySelector("#settings-view");
const settingsCloseButton = document.querySelector("#settings-close");
const settingsStatus = document.querySelector("#settings-status");
const settingsForm = document.querySelector("#settings-form");
const settingsOptions = document.querySelector("#settings-options");
const recommendationHistorySummary = document.querySelector("#recommendation-history-summary");
const clearRecommendationHistoryButton = document.querySelector("#clear-recommendation-history");

const REVIEW_LATER_RECOMMENDATION_THRESHOLD = 3;
const APPLICATION_STATUSES = new Set(["applied", "OA", "interview", "rejected", "offer"]);
let hideEmpty = true;
let trackerData = null;
let masterResume = null;
let resumeResources = [];
let coverLetterExamples = [];
let reviewQueue = [];
let prepQueue = [];
let prepAnalysisByRoleId = new Map();
let prepFeedbackIndexByRoleId = new Map();
let prepCoverLetterByRoleId = new Map();
let materialsInitialized = false;
let scanStatusPoll = null;
let wasScanning = false;
let settingsData = null;

function getActiveSearchQuery() {
  return trackerData?.query?.trim() ?? "";
}

function updateSearchButton() {
  const active = Boolean(getActiveSearchQuery());
  searchToggle.classList.toggle("search-active", active);
  searchToggle.setAttribute("aria-label", active ? "clear search" : "search jobs");
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
  })
    .format(new Date(value))
    .toLocaleLowerCase();
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
    .replace(", ", " ")
    .toLocaleLowerCase();
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatUiText(value) {
  return String(value ?? "").toLocaleLowerCase();
}

function escapeUiText(value) {
  return escapeHtml(formatUiText(value));
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
  const label = `<span class="role-title-text">${escapeUiText(title)}</span>`;
  if (!url) return `<span class="${className}">${label}</span>`;
  return `<a class="${className}" href="${escapeHtml(url)}" target="_blank" rel="noreferrer">${label}${renderLinkIcon()}</a>`;
}

function renderStats(stats) {
  const items = [
    ["companies", stats.companies_total],
    ["jobs", stats.jobs_total],
    ["applications", stats.applications_total],
  ];
  statsEl.innerHTML = items
    .map(([label, value]) => `<dl class="stat"><dt>${escapeUiText(label)}</dt><dd>${value}</dd></dl>`)
    .join("");
}

function renderToolbarSummary(data = trackerData) {
  if (!data) {
    toolbarSummary.innerHTML = "";
    return;
  }
  const countFor = (key) =>
    data.statuses.find((status) => status.key === key)?.count ?? 0;
  const items = [
    ["discovered", countFor("discovered")],
    ["interested", countFor("interested")],
    ["applied", data.stats?.applications_total ?? 0],
    ["total", data.stats?.jobs_total ?? 0],
  ];
  toolbarSummary.innerHTML = items
    .map(
      ([label, value]) => `
        <dl>
          <dt>${escapeUiText(label)}</dt>
          <dd>${value}</dd>
        </dl>
      `,
    )
    .join("");
}

function renderMasterResume(resume, message = "") {
  masterResume = resume;
  resumeUploadButton.textContent = resume ? "replace" : "upload";
  if (message) {
    resumeMeta.textContent = message;
    return;
  }
  if (!resume) {
    resumeMeta.textContent = "no resume uploaded";
    return;
  }
  const updated = formatCompactDate(resume.updated_at);
  const size = formatFileSize(resume.content_bytes);
  resumeMeta.textContent = [formatUiText(resume.filename), size, updated].filter(Boolean).join(" | ");
}

function renderCoverLetterExamples(examples, message = "") {
  coverLetterExamples = Array.isArray(examples) ? examples : [];
  coverLetterUploadButton.textContent = coverLetterExamples.length > 0 ? "add" : "upload";
  if (message) {
    coverLetterMeta.textContent = message;
  } else if (coverLetterExamples.length === 0) {
    coverLetterMeta.textContent = "no examples uploaded";
  } else {
    coverLetterMeta.textContent = `${coverLetterExamples.length} ${coverLetterExamples.length === 1 ? "example" : "examples"} stored`;
  }

  const visibleExamples = coverLetterExamples.slice(0, 3);
  const hiddenCount = Math.max(coverLetterExamples.length - visibleExamples.length, 0);
  coverLetterList.innerHTML = visibleExamples
    .map((example) => {
      const size = formatFileSize(example.content_bytes);
      return `
        <li title="${escapeUiText(example.filename)}">
          <span>${escapeUiText(example.filename)}</span>
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

function renderResumeResources(resources, message = "") {
  resumeResources = Array.isArray(resources) ? resources : [];
  resumeResourceUploadButton.textContent = resumeResources.length > 0 ? "add" : "upload";
  if (message) {
    resumeResourceMeta.textContent = message;
  } else if (resumeResources.length === 0) {
    resumeResourceMeta.textContent = "no resources uploaded";
  } else {
    resumeResourceMeta.textContent = `${resumeResources.length} ${resumeResources.length === 1 ? "resource" : "resources"} stored`;
  }

  const visibleResources = resumeResources.slice(0, 3);
  const hiddenCount = Math.max(resumeResources.length - visibleResources.length, 0);
  resumeResourceList.innerHTML = visibleResources
    .map((resource) => {
      const size = formatFileSize(resource.bytes);
      return `
        <li title="${escapeUiText(resource.filename)}">
          <span>${escapeUiText(resource.filename)}</span>
          <small>${escapeHtml(size)}</small>
        </li>
      `;
    })
    .join("");
  if (hiddenCount > 0) {
    resumeResourceList.insertAdjacentHTML(
      "beforeend",
      `<li class="examples-more"><span>+${hiddenCount} more</span></li>`,
    );
  }
}

function renderApplicationMaterials(payload, options = {}) {
  renderMasterResume(payload?.master_resume ?? null);
  renderResumeResources(payload?.resume_resources ?? []);
  renderCoverLetterExamples(payload?.cover_letter_examples ?? []);
  updateMaterialsSummary();
  if (!materialsInitialized || options.applyDefaultCollapsed) {
    setMaterialsCollapsed(Boolean(payload?.ui?.default_collapsed));
    materialsInitialized = true;
  }
}

function updateMaterialsSummary() {
  const resumeText = masterResume ? "resume ready" : "no resume";
  const resourceText =
    resumeResources.length === 0
      ? "no resources"
      : `${resumeResources.length} ${resumeResources.length === 1 ? "resource" : "resources"}`;
  const exampleCount = coverLetterExamples.length;
  const coverText =
    exampleCount === 0
      ? "no cover letters"
      : `${exampleCount} cover ${exampleCount === 1 ? "letter" : "letters"}`;
  materialsSummary.textContent = `${resumeText} | ${resourceText} | ${coverText}`;
}

function setMaterialsCollapsed(collapsed) {
  materialsPanel.classList.toggle("collapsed", collapsed);
  materialsToggle.setAttribute("aria-expanded", String(!collapsed));
  materialsToggle.querySelector(".materials-chevron").textContent = collapsed ? ">" : "v";
  materialsBody.hidden = collapsed;
}

function formatFileSize(bytes) {
  if (!Number.isFinite(bytes)) return "";
  if (bytes < 1024) return `${bytes} b`;
  return `${Math.round(bytes / 1024)} kb`;
}

function renderStatuses(statuses) {
  statusListEl.innerHTML = statuses
    .map((status) => {
      const jobs = status.jobs.map((job) => renderJob(job, status.key)).join("");

      return `
        <section class="status-pane ${status.count === 0 ? "empty" : ""} ${hideEmpty ? "hidden-empty" : ""}" id="status-${escapeHtml(status.key)}" data-bucket="${escapeHtml(status.key)}">
          <button class="pane-toggle" type="button" aria-expanded="false">
            <span class="chevron">></span>
            <span class="pane-title">${escapeUiText(status.label)}</span>
            <span class="count">${status.count}</span>
          </button>
          <div class="pane-body" hidden>
            ${jobs ? `<div class="jobs">${jobs}</div>` : `<p class="empty-copy">no jobs in this status.</p>`}
          </div>
        </section>
      `;
    })
    .join("");
}

function renderJob(job, statusKey) {
  return `
    <details class="job" data-role-id="${escapeHtml(job.id)}">
      <summary class="job-summary">
        <span class="job-chevron">></span>
        <span class="job-identity">
          <span class="job-company">[${escapeUiText(job.company_name)}]</span>
          ${renderRoleTitle(job.title, job.role_url, "job-title")}
        </span>
      </summary>
      <div class="job-detail">
        ${statusKey === "discovered" ? renderDiscoveredActions(job) : ""}
        ${statusKey === "interested" ? renderInterestedActions(job) : ""}
        ${statusKey === "applied" ? renderAppliedActions(job) : ""}
        ${statusKey === "OA" ? renderOaActions(job) : ""}
        ${statusKey === "interview" ? renderInterviewActions(job) : ""}
        <dl>
          ${
            job.location
              ? `<div>
                  <dt>location</dt>
                  <dd>${escapeUiText(job.location)}</dd>
                </div>`
              : ""
          }
          <div>
            <dt>updated</dt>
            <dd>${formatDate(job.updated_at)}</dd>
          </div>
        </dl>
      </div>
    </details>
  `;
}

function renderDiscoveredActions(job) {
  return `
    <div class="job-actions job-actions-nowrap" aria-label="discovered role actions">
      <button class="job-action" type="button" data-role-id="${job.id}" data-status="interested">interested</button>
      <button class="job-action" type="button" data-role-id="${job.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${job.id}" data-status="closed">closed</button>
    </div>
  `;
}

function renderInterestedActions(job) {
  return `
    <div class="job-actions" aria-label="interested role actions">
      <button class="job-action success" type="button" data-prep-role-id="${job.id}">prep</button>
      <button class="job-action" type="button" data-role-id="${job.id}" data-status="applied">applied</button>
      <button class="job-action" type="button" data-role-id="${job.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${job.id}" data-status="closed">closed</button>
    </div>
  `;
}

function renderAppliedActions(job) {
  return `
    <div class="job-actions job-actions-nowrap" aria-label="applied role actions">
      <button class="job-action" type="button" data-role-id="${job.id}" data-status="OA">oa</button>
      <button class="job-action" type="button" data-role-id="${job.id}" data-status="interview">interview</button>
      <button class="job-action danger" type="button" data-role-id="${job.id}" data-status="rejected">rejected</button>
    </div>
  `;
}

function renderOaActions(job) {
  return `
    <div class="job-actions job-actions-nowrap" aria-label="oa role actions">
      <button class="job-action" type="button" data-role-id="${job.id}" data-status="interview">interview</button>
      <button class="job-action" type="button" data-role-id="${job.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${job.id}" data-status="rejected">rejected</button>
    </div>
  `;
}

function renderInterviewActions(job) {
  return `
    <div class="job-actions" aria-label="interview role actions">
      <button class="job-action danger" type="button" data-role-id="${job.id}" data-status="rejected">rejected</button>
      <button class="job-action success" type="button" data-role-id="${job.id}" data-status="offer">offer</button>
    </div>
  `;
}

function render(data) {
  trackerData = data;
  searchInput.value = data.query;
  updateSearchButton();
  renderStats(data.stats);
  renderToolbarSummary(data);
  renderStatuses(data.statuses);
  updateToggleAllButton();
  updateReviewButton(data.statuses);
  updatePrepButton(data.statuses);
}

function renderScanStatus(payload) {
  const scanning = Boolean(payload?.scanning);
  const completed = Number(payload?.completed_companies ?? 0);
  const total = Number(payload?.total_companies ?? 0);
  const failed = Number(payload?.failed_companies ?? 0);

  scanAllButton.disabled = scanning;
  scanAllButton.textContent = scanning ? "scanning..." : "scan roles";
  scanStatusBar.hidden = !scanning;
  scanStatusBar.classList.toggle("scanning", scanning);
  scanStatusBar.classList.toggle("scan-error", !scanning && Boolean(payload?.error));

  if (scanning) {
    const progressText = total > 0 ? ` ${completed}/${total}` : "";
    const failureText = failed > 0 ? `, ${failed} failed` : "";
    scanStatusText.textContent = `scanning roles${progressText}${failureText}`;
  } else if (payload?.error) {
    scanStatusText.textContent = "last scan had errors";
  } else {
    scanStatusText.textContent = "scan idle";
  }

  const lastScanAt = payload?.last_scan_at;
  scanLastTime.textContent = lastScanAt ? `last scan: ${formatCompactDate(lastScanAt)}` : "last scan: never";

  if (wasScanning && !scanning) {
    loadTracker(getActiveSearchQuery()).catch(() => {});
  }
  wasScanning = scanning;
}

function renderSettings(payload, message = "") {
  settingsData = payload;
  const settings = Array.isArray(payload?.settings) ? payload.settings : [];
  settingsStatus.textContent = message;
  settingsStatus.classList.toggle("is-empty", !message);
  const historyCount = Number(payload?.recommendation_history_count ?? 0);
  recommendationHistorySummary.textContent =
    historyCount > 0
      ? `${historyCount} saved ${historyCount === 1 ? "feedback decision" : "feedback decisions"}`
      : "no saved resume feedback decisions";
  clearRecommendationHistoryButton.disabled = historyCount === 0;
  settingsOptions.innerHTML = settings
    .map((setting) => renderSettingOption(setting))
    .join("");
}

function renderSettingOption(setting) {
  if (setting.control === "select" && setting.editable !== false) {
    return renderSelectSettingOption(setting);
  }
  if (setting.control !== "toggle" || setting.editable === false) {
    return renderComputedSettingOption(setting);
  }
  const checked = setting.value ? "checked" : "";
  const defaultText = setting.default ? "on by default" : "off by default";
  return `
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${escapeUiText(setting.label)}</span>
        <span class="setting-description">${escapeUiText(setting.description)}</span>
        <span class="setting-default">${escapeUiText(defaultText)}</span>
      </span>
      <span class="setting-switch">
        <input type="checkbox" name="${escapeHtml(setting.key)}" ${checked} />
        <span aria-hidden="true"></span>
      </span>
    </label>
  `;
}

function renderSelectSettingOption(setting) {
  const options = Array.isArray(setting.options) ? setting.options : [];
  const defaultText = `default: ${formatUiText(setting.default)}`;
  return `
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${escapeUiText(setting.label)}</span>
        <span class="setting-description">${escapeUiText(setting.description)}</span>
        <span class="setting-default">${escapeUiText(defaultText)}</span>
      </span>
      <select class="setting-select" name="${escapeHtml(setting.key)}">
        ${options
          .map((option) => {
            const selected = option.value === setting.value ? "selected" : "";
            return `<option value="${escapeHtml(option.value)}" ${selected}>${escapeUiText(option.label)}</option>`;
          })
          .join("")}
      </select>
    </label>
  `;
}

function renderComputedSettingOption(setting) {
  const defaultText = setting.default ? "on by default" : "off by default";
  const valueText = setting.value ? "automatic" : "off";
  return `
    <div class="setting-option setting-option-readonly">
      <span class="setting-copy">
        <span class="setting-label">${escapeUiText(setting.label)}</span>
        <span class="setting-description">${escapeUiText(setting.description)}</span>
        <span class="setting-default">${escapeUiText(defaultText)}</span>
      </span>
      <span class="setting-badge">${escapeUiText(valueText)}</span>
    </div>
  `;
}

function setSettingsDisabled(disabled) {
  settingsForm.querySelectorAll("input, select").forEach((input) => {
    input.disabled = disabled;
  });
}

async function openSettingsView() {
  settingsView.hidden = false;
  document.body.classList.add("settings-open");
  settingsCloseButton.focus();
  if (settingsData) {
    renderSettings(settingsData);
  } else {
    settingsStatus.textContent = "loading settings...";
    settingsStatus.classList.remove("is-empty");
    settingsOptions.innerHTML = "";
  }
  try {
    await loadSettings();
  } catch {
    settingsStatus.textContent = "could not load settings.";
  }
}

function closeSettingsView() {
  settingsView.hidden = true;
  document.body.classList.remove("settings-open");
  settingsOpenButton.focus();
}

async function loadSettings() {
  const response = await fetch("/api/config");
  if (!response.ok) throw new Error("Config request failed");
  renderSettings(await response.json());
}

async function saveSetting(control) {
  const key = control.name;
  if (!key) return;
  const previousValue = control.type === "checkbox" ? !control.checked : settingsData?.settings
    ?.find((setting) => setting.key === key)?.value;
  const nextValue = control.type === "checkbox" ? control.checked : control.value;
  setSettingsDisabled(true);
  settingsStatus.textContent = "saving settings...";
  settingsStatus.classList.remove("is-empty");
  try {
    const response = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ [key]: nextValue }),
    });
    if (!response.ok) throw new Error("Config update failed");
    renderSettings(await response.json(), "settings saved.");
  } catch {
    if (control.type === "checkbox") {
      control.checked = previousValue;
    } else if (previousValue !== undefined) {
      control.value = previousValue;
    }
    settingsStatus.textContent = "could not save settings.";
    setSettingsDisabled(false);
  }
}

async function clearRecommendationHistory() {
  clearRecommendationHistoryButton.disabled = true;
  settingsStatus.textContent = "clearing recommendation history...";
  settingsStatus.classList.remove("is-empty");
  try {
    const response = await fetch("/api/recommendation-history/clear", {
      method: "POST",
    });
    if (!response.ok) throw new Error("Recommendation history clear failed");
    const payload = await response.json();
    renderSettings(payload.config, `cleared ${payload.deleted_count} saved decisions.`);
  } catch {
    settingsStatus.textContent = "could not clear recommendation history.";
    clearRecommendationHistoryButton.disabled = false;
  }
}

async function loadScanStatus() {
  const response = await fetch("/api/scan/status");
  if (response.status === 404) {
    scanAllButton.disabled = true;
    scanStatusBar.hidden = true;
    scanStatusBar.classList.add("scan-error");
    scanStatusText.textContent = "restart server to enable scanning";
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
  scanAllButton.textContent = "scanning...";
  try {
    const response = await fetch("/api/scan/all", { method: "POST" });
    if (response.status === 404) {
      scanAllButton.disabled = true;
      scanAllButton.textContent = "scan roles";
      scanStatusBar.hidden = true;
      scanStatusBar.classList.add("scan-error");
      scanStatusText.textContent = "restart server to enable scanning";
      return;
    }
    if (!response.ok && response.status !== 409) throw new Error("Scan start failed");
    renderScanStatus(await response.json());
    startScanStatusPolling();
  } catch {
    scanAllButton.disabled = false;
    scanAllButton.textContent = "scan roles";
    scanStatusBar.hidden = true;
    scanStatusBar.classList.add("scan-error");
    scanStatusText.textContent = "could not start scan";
  }
}

async function loadTracker(query = "") {
  statusListEl.innerHTML = '<p class="empty-copy">loading jobs...</p>';
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
    renderMasterResume(masterResume, "resume must be a .tex file.");
    return;
  }

  resumeUploadButton.disabled = true;
  renderMasterResume(masterResume, "uploading...");
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
    renderMasterResume(masterResume, "could not save resume.");
    updateMaterialsSummary();
  } finally {
    resumeUpload.value = "";
    resumeUploadButton.disabled = false;
  }
}

async function uploadResumeResources(files) {
  const selectedFiles = Array.from(files ?? []);
  if (selectedFiles.length === 0) return;

  resumeResourceUploadButton.disabled = true;
  renderResumeResources(
    resumeResources,
    `uploading ${selectedFiles.length} ${selectedFiles.length === 1 ? "resource" : "resources"}...`,
  );
  try {
    for (const file of selectedFiles) {
      const response = await fetch("/api/resume-resources", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          filename: file.name,
          content_base64: await readFileAsBase64(file),
        }),
      });
      if (!response.ok) throw new Error("Resume resource upload failed");
    }
    await loadApplicationMaterials();
  } catch {
    renderResumeResources(resumeResources, "could not save every resource.");
    updateMaterialsSummary();
  } finally {
    resumeResourceUpload.value = "";
    resumeResourceUploadButton.disabled = false;
  }
}

async function uploadCoverLetterExamples(files) {
  const selectedFiles = Array.from(files ?? []);
  if (selectedFiles.length === 0) return;

  coverLetterUploadButton.disabled = true;
  renderCoverLetterExamples(
    coverLetterExamples,
    `uploading ${selectedFiles.length} ${selectedFiles.length === 1 ? "example" : "examples"}...`,
  );
  try {
    for (const file of selectedFiles) {
      const payload = { filename: file.name };
      if (file.name.toLowerCase().endsWith(".docx")) {
        payload.content_base64 = await readFileAsBase64(file);
      } else {
        payload.content = await file.text();
      }
      const response = await fetch("/api/cover-letter-examples", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!response.ok) throw new Error("Cover letter example upload failed");
    }
    await loadApplicationMaterials();
  } catch {
    renderCoverLetterExamples(coverLetterExamples, "could not save every example.");
    updateMaterialsSummary();
  } finally {
    coverLetterUpload.value = "";
    coverLetterUploadButton.disabled = false;
  }
}

function readFileAsBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.addEventListener("load", () => {
      const result = String(reader.result ?? "");
      resolve(result.includes(",") ? result.split(",", 2)[1] : result);
    });
    reader.addEventListener("error", () => reject(reader.error));
    reader.readAsDataURL(file);
  });
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

resumeResourceUploadButton.addEventListener("click", () => {
  resumeResourceUpload.click();
});

resumeResourceUpload.addEventListener("change", () => {
  uploadResumeResources(resumeResourceUpload.files);
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

statusListEl.addEventListener("click", (event) => {
  const prepAction = event.target.closest("[data-prep-role-id]");
  if (prepAction) {
    openPrepView(prepAction.dataset.prepRoleId);
    return;
  }

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
  const currentJobEl = button.closest(".job");
  actions.querySelectorAll("button").forEach((item) => {
    item.disabled = true;
  });
  button.textContent = "updating...";

  try {
    const response = await fetch(`/api/roles/${encodeURIComponent(roleId)}/status`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    });
    if (!response.ok) throw new Error("Status update failed");
    const payload = await response.json();
    applyRoleStatusUpdate(payload.role, currentJobEl);
  } catch {
    actions.querySelectorAll("button").forEach((item) => {
      item.disabled = false;
    });
    button.textContent =
      status === "disinterested"
        ? "disinterested"
        : status.toLowerCase();
  }
}

function applyRoleStatusUpdate(updatedRole, currentJobEl) {
  if (!updatedRole || !trackerData) return;
  const previousStatus = currentJobEl?.closest(".status-pane")?.dataset.bucket ?? updatedRole.role_status;
  const nextStatus = updatedRole.role_status;
  const movedRole = moveRoleInTrackerData(updatedRole, previousStatus, nextStatus);
  updateStatusCounts(previousStatus, nextStatus);
  updateApplicationStats(previousStatus, nextStatus);
  renderToolbarSummary();
  updateReviewButton(trackerData.statuses);
  updatePrepButton(trackerData.statuses);
  moveRoleElement(currentJobEl, movedRole, previousStatus, nextStatus);
  updateToggleAllButton();
}

function moveRoleInTrackerData(updatedRole, previousStatus, nextStatus) {
  let movedRole = updatedRole;
  trackerData.statuses.forEach((status) => {
    const index = status.jobs.findIndex((job) => String(job.id) === String(updatedRole.id));
    if (index === -1) return;
    movedRole = { ...status.jobs[index], ...updatedRole };
    status.jobs.splice(index, 1);
    status.count = status.jobs.length;
  });

  const nextBucket = trackerData.statuses.find((status) => status.key === nextStatus);
  if (nextBucket) {
    nextBucket.jobs.unshift(movedRole);
    nextBucket.count = nextBucket.jobs.length;
  }

  return movedRole;
}

function updateStatusCounts(previousStatus, nextStatus) {
  trackerData.statuses.forEach((status) => {
    const pane = document.querySelector(`#status-${CSS.escape(status.key)}`);
    pane?.classList.toggle("empty", status.count === 0);
    const paneCount = pane?.querySelector(".count");
    if (paneCount) paneCount.textContent = status.count;
  });

  [previousStatus, nextStatus].forEach((status) => {
    const pane = document.querySelector(`#status-${CSS.escape(status)}`);
    refreshEmptyMessage(pane);
  });
}

function updateApplicationStats(previousStatus, nextStatus) {
  if (!trackerData.stats) return;
  const wasApplication = APPLICATION_STATUSES.has(previousStatus);
  const isApplication = APPLICATION_STATUSES.has(nextStatus);
  if (wasApplication === isApplication) {
    renderStats(trackerData.stats);
    return;
  }

  trackerData.stats.applications_total =
    Number(trackerData.stats.applications_total ?? 0) + (isApplication ? 1 : -1);
  renderStats(trackerData.stats);
}

function moveRoleElement(currentJobEl, movedRole, previousStatus, nextStatus) {
  const nextPane = document.querySelector(`#status-${CSS.escape(nextStatus)}`);
  const nextBody = nextPane?.querySelector(".pane-body");
  if (!currentJobEl || !nextPane || !nextBody) return;

  currentJobEl.remove();
  refreshEmptyMessage(document.querySelector(`#status-${CSS.escape(previousStatus)}`));

  nextBody.hidden = false;
  const nextToggle = nextPane.querySelector(".pane-toggle");
  nextToggle?.setAttribute("aria-expanded", "true");
  const chevron = nextToggle?.querySelector(".chevron");
  if (chevron) chevron.textContent = "v";

  let jobsEl = nextBody.querySelector(".jobs");
  if (!jobsEl) {
    nextBody.innerHTML = '<div class="jobs"></div>';
    jobsEl = nextBody.querySelector(".jobs");
  }
  jobsEl.insertAdjacentHTML("afterbegin", renderJob(movedRole, nextStatus));
  refreshEmptyMessage(nextPane);
}

function refreshEmptyMessage(pane) {
  if (!pane) return;
  const body = pane.querySelector(".pane-body");
  if (!body) return;

  const jobsEl = body.querySelector(".jobs");
  const hasJobs = Boolean(jobsEl?.querySelector(".job"));
  const emptyCopy = body.querySelector(".empty-copy");

  if (hasJobs) {
    emptyCopy?.remove();
    return;
  }

  jobsEl?.remove();
  if (!emptyCopy) {
    body.insertAdjacentHTML("beforeend", '<p class="empty-copy">no jobs in this status.</p>');
  }
}

function updateReviewButton(statuses) {
  const discovered = getDiscoveredJobs(statuses);
  reviewDiscoveredButton.disabled = discovered.length === 0;
  reviewDiscoveredButton.setAttribute("aria-label", "review discovered");
  reviewDiscoveredButton.innerHTML = '<span class="review-discovered-label">review discovered</span>';
}

function getDiscoveredJobs(statuses = trackerData?.statuses ?? []) {
  return statuses.find((status) => status.key === "discovered")?.jobs ?? [];
}

function updatePrepButton(statuses) {
  const interested = getInterestedJobs(statuses);
  prepInterestedButton.disabled = interested.length === 0;
  prepInterestedButton.setAttribute("aria-label", "prep interested");
  prepInterestedButton.innerHTML = '<span class="review-discovered-label">prep interested</span>';
}

function getInterestedJobs(statuses = trackerData?.statuses ?? []) {
  return statuses.find((status) => status.key === "interested")?.jobs ?? [];
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

function openPrepView(focusedRoleId = null) {
  const interestedJobs = [...getInterestedJobs()];
  const focusedId = focusedRoleId == null ? null : String(focusedRoleId);
  if (focusedId) {
    const focusedIndex = interestedJobs.findIndex((role) => String(role.id) === focusedId);
    if (focusedIndex > 0) {
      const [focusedRole] = interestedJobs.splice(focusedIndex, 1);
      interestedJobs.unshift(focusedRole);
    }
  }
  prepQueue = interestedJobs;
  prepView.hidden = false;
  document.body.classList.add("prep-open");
  renderPrepRole();
}

function closePrepView() {
  prepView.hidden = true;
  document.body.classList.remove("prep-open");
  prepQueue = [];
}

function renderReviewRole(message = "") {
  const current = reviewQueue[0];
  const total = reviewQueue.length;
  const reviewLaterMessage = current ? getReviewLaterRecommendation(current) : "";
  reviewHeading.textContent = total > 0 ? "review queue" : "review complete";
  reviewProgress.textContent =
    total > 0 ? `${total} discovered ${total === 1 ? "role" : "roles"} in queue` : "";

  reviewView.querySelectorAll(".review-action").forEach((button) => {
    button.disabled = total === 0;
  });

  if (!current) {
    reviewCard.innerHTML = `
      <div class="review-empty">
        <h3>no discovered jobs left.</h3>
        <p>everything in this queue has been handled or moved out of discovered.</p>
      </div>
    `;
    return;
  }

  reviewCard.innerHTML = `
    ${message ? `<p class="review-message">${escapeHtml(message)}</p>` : ""}
    ${reviewLaterMessage ? `<p class="review-message review-message-warning">${escapeHtml(reviewLaterMessage)}</p>` : ""}
    <div class="review-title-row">
      <p class="review-company">${escapeUiText(current.company_name)}</p>
      ${renderRoleTitle(current.title, current.role_url, "review-role-title")}
    </div>
    <dl class="review-details review-primary-details">
      ${renderReviewDetail("location", current.location, false, "review-location-detail")}
      ${renderReviewDetail("first", formatCompactDate(current.first_seen_at))}
      ${renderReviewDetail("last", formatCompactDate(current.last_seen_at))}
    </dl>
    ${renderReviewDescription(current.description)}
    <dl class="review-details review-technical-details">
      ${renderReviewDetail("notes", current.notes, false, "review-wide-detail")}
      ${renderReviewDetail("company id", current.company_id)}
      ${renderReviewDetail("role id", current.id)}
      ${renderReviewDetail("status", current.role_status)}
      ${renderReviewDetail("posting id", current.posting_id)}
      ${renderReviewDetail("created", formatCompactDate(current.created_at))}
      ${renderReviewDetail("updated", formatCompactDate(current.updated_at))}
      ${renderReviewDetail("url", current.role_url, true, "review-wide-detail")}
    </dl>
  `;
}

function getReviewLaterRecommendation(role) {
  const count = Number(role.review_later_count ?? 0);
  if (count <= REVIEW_LATER_RECOMMENDATION_THRESHOLD) return "";
  return `role review has been postponed ${count} times. it is recommended to set it to disinterested.`;
}

function renderReviewDetail(label, value, isLink = false, className = "") {
  if (!value) return "";
  const content = isLink
    ? `<a href="${escapeHtml(value)}" target="_blank" rel="noreferrer">${escapeUiText(value)}</a>`
    : escapeUiText(value);
  return `
    <div class="review-detail ${escapeHtml(className)}">
      <dt>${escapeUiText(label)}</dt>
      <dd>${content}</dd>
    </div>
  `;
}

function renderReviewDescription(value) {
  if (!value) return "";
  return `
    <div class="review-detail review-description">
      <dt>description</dt>
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
      blocks.push(`<h3>${escapeUiText(heading[1])}</h3>`);
      return;
    }

    const bullet = line.match(/^[-*]\s+(.+)$/);
    if (bullet) {
      listItems.push(escapeUiText(bullet[1]));
      return;
    }

    flushList();
    blocks.push(`<p>${escapeUiText(line)}</p>`);
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
        renderReviewRole("moved to the back of the queue.");
      } else {
        renderReviewRole("only one role is in the queue.");
      }
    } catch {
      renderReviewRole("could not postpone that role. try again.");
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
    const updatedRole = await updateRoleStatusById(current.id, action);
    reviewQueue.shift();
    renderReviewRole(action === "interested" ? "marked interested." : "marked disinterested.");
    const currentJobEl = document.querySelector(`.job[data-role-id="${CSS.escape(String(current.id))}"]`);
    applyRoleStatusUpdate(updatedRole, currentJobEl);
  } catch {
    buttons.forEach((button) => {
      button.disabled = false;
    });
    renderReviewRole("could not update that role. try again.");
  }
}

async function renderPrepRole(message = "") {
  const current = prepQueue[0];
  const total = prepQueue.length;
  prepHeading.textContent = total > 0 ? "prep queue" : "prep complete";
  prepProgress.textContent =
    total > 0 ? `${total} interested ${total === 1 ? "role" : "roles"} in queue` : "";

  prepView.querySelectorAll(".review-action").forEach((button) => {
    button.disabled = total === 0;
  });

  if (!current) {
    prepCard.innerHTML = `
      <div class="review-empty">
        <h3>no interested jobs left.</h3>
        <p>everything in this queue has been prepped, moved, or postponed.</p>
      </div>
    `;
    return;
  }

  prepCard.innerHTML = `
    ${message ? `<p class="review-message">${escapeHtml(message)}</p>` : ""}
    <div class="review-title-row">
      <p class="review-company">${escapeUiText(current.company_name)}</p>
      ${renderRoleTitle(current.title, current.role_url, "review-role-title")}
    </div>
    ${renderPrepAnalysis(current)}
    ${renderPrepCoverLetter(current)}
    <dl class="review-details review-primary-details">
      ${renderReviewDetail("location", current.location, false, "review-location-detail")}
      ${renderReviewDetail("last", formatCompactDate(current.last_seen_at))}
      ${renderReviewDetail("updated", formatCompactDate(current.updated_at))}
    </dl>
    ${renderReviewDescription(current.description)}
  `;

  loadPrepCoverLetter(current.id)
    .then((coverLetter) => {
      if (!coverLetter || prepQueue[0]?.id !== current.id) return;
      prepCoverLetterByRoleId.set(current.id, coverLetter);
      prepCard.querySelector(".prep-cover-letter")?.replaceWith(
        htmlToElement(renderPrepCoverLetter(current, { coverLetter })),
      );
    })
    .catch(() => {});
}

function renderPrepCoverLetter(role, state = {}) {
  const savedDraft = prepCoverLetterByRoleId.get(role.id);
  const draft = state.coverLetter ?? savedDraft;
  const tweaks = state.tweaks ?? draft?.tweaks ?? "";
  const pdfUrl = `/api/roles/${encodeURIComponent(role.id)}/cover-letter.pdf`;
  if (state.loading) {
    return `
      <section class="prep-cover-letter" aria-label="cover letter">
        <div class="prep-analysis-header">
          <h3>cover letter</h3>
          <span>generating</span>
        </div>
        <div class="prep-fit-loading" aria-label="generating cover letter">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <p>generating latex cover letter...</p>
        </div>
      </section>
    `;
  }
  return `
    <section class="prep-cover-letter" aria-label="cover letter">
      <div class="prep-analysis-header">
        <h3>cover letter</h3>
        <button type="button" data-prep-cover-letter="${role.id}">
          ${draft ? "regenerate" : "generate"}
        </button>
      </div>
      ${
        draft
          ? `
            <p class="prep-overview">${escapeUiText(draft.summary ?? "cover letter generated")}</p>
            <label class="prep-cover-tweaks">
              <span>tweaks</span>
              <textarea
                data-prep-cover-letter-tweaks="${role.id}"
                rows="3"
                placeholder="make it warmer, cut a paragraph, emphasize systems work..."
              >${escapeUiText(tweaks)}</textarea>
            </label>
            <p class="prep-cover-path">${escapeUiText(draft.path ?? "")}</p>
            ${
              draft.pdf_base64
                ? `
                  <a class="prep-cover-pdf-link" href="${escapeHtml(pdfUrl)}" target="_blank" rel="noreferrer">
                    open PDF
                  </a>
                  <iframe class="prep-cover-pdf" title="cover letter PDF preview" src="data:application/pdf;base64,${escapeHtml(draft.pdf_base64)}"></iframe>
                `
                : '<p class="prep-cover-path">PDF preview unavailable.</p>'
            }
            <pre>${escapeUiText(draft.latex ?? "")}</pre>
          `
          : '<p class="prep-overview">generate a LaTeX cover letter from the resume, posting, and stored examples.</p>'
      }
    </section>
  `;
}

function renderPrepAnalysis(role, state = {}) {
  const savedAnalysis = prepAnalysisByRoleId.get(role.id);
  if (!state.loading && !state.error && !state.analysis && savedAnalysis) {
    return renderPrepAnalysis(role, { analysis: savedAnalysis });
  }
  if (!state.loading && !state.error && !state.analysis) {
    return `
      <section class="prep-analysis" aria-label="ai analysis">
        <div class="prep-analysis-header">
          <h3>ai analysis</h3>
          <button type="button" data-prep-analysis="${role.id}">check fit</button>
        </div>
        <p class="prep-overview">check resume fit when you are ready to review AI feedback.</p>
      </section>
    `;
  }
  if (state.loading) {
    return `
      <section class="prep-analysis" aria-label="ai analysis">
        <div class="prep-analysis-header">
          <h3>ai analysis</h3>
          <span>loading</span>
        </div>
        <div class="prep-fit-loading" aria-label="checking resume fit">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <p>checking resume fit...</p>
        </div>
      </section>
    `;
  }
  if (state.error) {
    return `
      <section class="prep-analysis" aria-label="ai analysis">
        <div class="prep-analysis-header">
          <h3>ai analysis</h3>
          <span>unavailable</span>
        </div>
        <p class="prep-overview">could not generate analysis for this role.</p>
      </section>
    `;
  }

  const analysis = state.analysis;
  const items = Array.isArray(analysis?.feedback_items) ? analysis.feedback_items : [];
  const verdict = analysis?.verdict === "ready_to_apply" ? "ready to apply" : "tweak";
  const currentIndex = Math.min(
    prepFeedbackIndexByRoleId.get(role.id) ?? 0,
    Math.max(items.length - 1, 0),
  );
  const item = items[currentIndex];
  return `
    <section class="prep-analysis" aria-label="ai analysis">
      <div class="prep-analysis-header">
        <h3>ai analysis</h3>
        <span>${items.length} ${items.length === 1 ? "item" : "items"}</span>
      </div>
      <p class="prep-verdict">${escapeUiText(verdict)}</p>
      <p class="prep-overview">${escapeUiText(analysis?.overview ?? "analysis unavailable")}</p>
      ${
        item
          ? `
            <article class="prep-feedback" data-feedback-index="${currentIndex}">
              <p class="prep-feedback-label">${escapeUiText(item.label)}</p>
              <h4>${escapeUiText(item.title)}</h4>
              <p>${escapeUiText(item.detail)}</p>
              ${renderPrepProposedEdit(item)}
              <label class="prep-feedback-comment">
                <span>response comment</span>
                <textarea
                  data-prep-feedback-comment
                  rows="2"
                  placeholder="why accept or ignore this?"
                ></textarea>
              </label>
            </article>
            <div class="prep-feedback-controls">
              <div class="prep-feedback-nav">
                <button type="button" data-prep-feedback="previous" ${currentIndex === 0 ? "disabled" : ""}>previous</button>
                <span>${currentIndex + 1}/${items.length}</span>
                <button type="button" data-prep-feedback="next" ${currentIndex >= items.length - 1 ? "disabled" : ""}>next</button>
              </div>
              <div class="prep-feedback-decisions">
                <button type="button" data-prep-feedback="ignore">ignore</button>
                <button type="button" data-prep-feedback="accept">accept</button>
              </div>
            </div>
          `
          : '<p class="prep-overview">ready to apply with the current resume.</p>'
      }
    </section>
  `;
}

function renderPrepProposedEdit(item) {
  if (item?.target_text && item?.replacement_text) {
    return `
      <div class="prep-proposed-edit">
        <p class="prep-proposed-label">proposed edit</p>
        <div class="prep-edit-pair">
          <div>
            <span>replace</span>
            <pre>${escapeUiText(item.target_text)}</pre>
          </div>
          <div>
            <span>with</span>
            <pre>${escapeUiText(item.replacement_text)}</pre>
          </div>
        </div>
      </div>
    `;
  }
  if (item?.latex_addition) {
    return `
      <div class="prep-proposed-edit">
        <p class="prep-proposed-label">proposed edit</p>
        <pre>${escapeUiText(item.latex_addition)}</pre>
      </div>
    `;
  }
  return `
    <div class="prep-proposed-edit">
      <p class="prep-proposed-label">proposed edit</p>
      <p>${escapeUiText(item?.detail ?? "no exact edit proposed")}</p>
    </div>
  `;
}

async function loadPrepAnalysis(roleId) {
  if (prepAnalysisByRoleId.has(roleId)) return prepAnalysisByRoleId.get(roleId);
  const response = await fetch(`/api/roles/${encodeURIComponent(roleId)}/prep-analysis`);
  if (!response.ok) throw new Error("Prep analysis request failed");
  const payload = await response.json();
  payload.analysis.resources = payload.resources ?? [];
  prepAnalysisByRoleId.set(roleId, payload.analysis);
  return payload.analysis;
}

function htmlToElement(markup) {
  const template = document.createElement("template");
  template.innerHTML = markup.trim();
  return template.content.firstElementChild;
}

async function handlePrepAction(action) {
  const current = prepQueue[0];
  if (!current) return;

  if (action === "pdf") {
    const pdfButton = prepView.querySelector('[data-prep-action="pdf"]');
    const originalLabel = pdfButton?.textContent ?? "generate PDF";
    if (pdfButton) {
      pdfButton.disabled = true;
      pdfButton.textContent = "generating...";
    }
    try {
      const payload = await generatePrepResumePdf(current.id);
      renderPrepRole(`saved PDF to ${payload.pdf_path}`);
    } catch {
      renderPrepRole("could not generate PDF. install pdflatex or latexmk.");
    } finally {
      const nextPdfButton = prepView.querySelector('[data-prep-action="pdf"]');
      if (nextPdfButton) {
        nextPdfButton.disabled = false;
        nextPdfButton.textContent = originalLabel;
      }
    }
    return;
  }

  const buttons = prepView.querySelectorAll(".review-action");
  buttons.forEach((button) => {
    button.disabled = true;
  });

  if (action === "later") {
    try {
      await recordRoleReviewLater(current.id);
      current.review_later_count = Number(current.review_later_count ?? 0) + 1;
      if (prepQueue.length > 1) {
        prepQueue.push(prepQueue.shift());
        renderPrepRole("moved to the back of the prep queue.");
      } else {
        renderPrepRole("only one role is in the prep queue.");
      }
    } catch {
      renderPrepRole("could not postpone prep. try again.");
    }
    return;
  }

  if (action !== "applied") return;

  try {
    const updatedRole = await updateRoleStatusById(current.id, "applied");
    prepQueue.shift();
    renderPrepRole("moved to applied.");
    const currentJobEl = document.querySelector(`.job[data-role-id="${CSS.escape(String(current.id))}"]`);
    applyRoleStatusUpdate(updatedRole, currentJobEl);
  } catch {
    buttons.forEach((button) => {
      button.disabled = false;
    });
    renderPrepRole("could not move that role. try again.");
  }
}

async function acceptPrepFeedback(roleId, feedbackIndex, feedbackItem, comment) {
  const response = await fetch(`/api/roles/${encodeURIComponent(roleId)}/prep-feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ feedback_index: feedbackIndex, feedback_item: feedbackItem, comment }),
  });
  if (!response.ok) throw new Error("Prep feedback update failed");
  return response.json();
}

async function ignorePrepFeedback(roleId, feedbackIndex, feedbackItem, comment) {
  const response = await fetch(`/api/roles/${encodeURIComponent(roleId)}/prep-feedback-ignore`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ feedback_index: feedbackIndex, feedback_item: feedbackItem, comment }),
  });
  if (!response.ok) throw new Error("Prep feedback ignore failed");
  return response.json();
}

async function generatePrepResumePdf(roleId) {
  const response = await fetch(`/api/roles/${encodeURIComponent(roleId)}/resume-pdf`, {
    method: "POST",
  });
  if (!response.ok) throw new Error("Resume PDF generation failed");
  return response.json();
}

async function generatePrepCoverLetter(roleId, tweaks = "") {
  const response = await fetch(`/api/roles/${encodeURIComponent(roleId)}/cover-letter`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tweaks }),
  });
  if (!response.ok) throw new Error("Cover letter generation failed");
  return response.json();
}

async function loadPrepCoverLetter(roleId) {
  if (prepCoverLetterByRoleId.has(roleId)) return prepCoverLetterByRoleId.get(roleId);
  const response = await fetch(`/api/roles/${encodeURIComponent(roleId)}/cover-letter`);
  if (!response.ok) throw new Error("Cover letter request failed");
  const payload = await response.json();
  if (payload.cover_letter) {
    prepCoverLetterByRoleId.set(roleId, payload.cover_letter);
  }
  return payload.cover_letter;
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
  const payload = await response.json();
  return payload.role;
}

reviewDiscoveredButton.addEventListener("click", openReviewView);

closeReviewButton.addEventListener("click", closeReviewView);

prepInterestedButton.addEventListener("click", openPrepView);

closePrepButton.addEventListener("click", closePrepView);

reviewView.addEventListener("click", (event) => {
  const button = event.target.closest("[data-review-action]");
  if (!button) return;
  handleReviewAction(button.dataset.reviewAction);
});

prepView.addEventListener("click", async (event) => {
  const analysisButton = event.target.closest("[data-prep-analysis]");
  if (analysisButton && prepQueue[0]) {
    const roleId = prepQueue[0].id;
    prepCard.querySelector(".prep-analysis")?.replaceWith(
      htmlToElement(renderPrepAnalysis(prepQueue[0], { loading: true })),
    );
    try {
      const analysis = await loadPrepAnalysis(roleId);
      if (prepQueue[0]?.id !== roleId) return;
      prepCard.querySelector(".prep-analysis")?.replaceWith(
        htmlToElement(renderPrepAnalysis(prepQueue[0], { analysis })),
      );
    } catch {
      prepCard.querySelector(".prep-analysis")?.replaceWith(
        htmlToElement(renderPrepAnalysis(prepQueue[0], { error: true })),
      );
    }
    return;
  }

  const coverLetterButton = event.target.closest("[data-prep-cover-letter]");
  if (coverLetterButton && prepQueue[0]) {
    const roleId = prepQueue[0].id;
    const coverSection = prepCard.querySelector(".prep-cover-letter");
    const tweaks =
      coverSection?.querySelector(`[data-prep-cover-letter-tweaks="${roleId}"]`)?.value ?? "";
    coverSection?.replaceWith(htmlToElement(renderPrepCoverLetter(prepQueue[0], { loading: true })));
    try {
      const payload = await generatePrepCoverLetter(roleId, tweaks);
      prepCoverLetterByRoleId.set(roleId, payload.cover_letter);
      prepCard.querySelector(".prep-cover-letter")?.replaceWith(
        htmlToElement(renderPrepCoverLetter(prepQueue[0], { coverLetter: payload.cover_letter })),
      );
    } catch {
      prepCard.querySelector(".prep-cover-letter")?.replaceWith(
        htmlToElement(
          renderPrepCoverLetter(prepQueue[0], {
            coverLetter: prepCoverLetterByRoleId.get(roleId),
            tweaks,
          }),
        ),
      );
    }
    return;
  }

  const actionButton = event.target.closest("[data-prep-action]");
  if (actionButton) {
    handlePrepAction(actionButton.dataset.prepAction);
    return;
  }

  const feedbackButton = event.target.closest("[data-prep-feedback]");
  if (!feedbackButton || !prepQueue[0]) return;
  const roleId = prepQueue[0].id;
  const analysis = prepAnalysisByRoleId.get(roleId);
  const itemCount = Array.isArray(analysis?.feedback_items) ? analysis.feedback_items.length : 0;
  const currentIndex = prepFeedbackIndexByRoleId.get(roleId) ?? 0;
  if (
    feedbackButton.dataset.prepFeedback === "accept"
    || feedbackButton.dataset.prepFeedback === "ignore"
  ) {
    const feedbackItem = analysis?.feedback_items?.[currentIndex];
    if (!feedbackItem) return;
    const comment = prepCard.querySelector("[data-prep-feedback-comment]")?.value ?? "";
    const responseAction = feedbackButton.dataset.prepFeedback;
    const originalLabel = responseAction;
    feedbackButton.disabled = true;
    feedbackButton.textContent = responseAction === "accept" ? "accepting..." : "ignoring...";
    try {
      if (responseAction === "accept") {
        const payload = await acceptPrepFeedback(roleId, currentIndex, feedbackItem, comment);
        const currentJobEl = document.querySelector(`.job[data-role-id="${CSS.escape(String(roleId))}"]`);
        if (payload.role) {
          prepQueue[0] = payload.role;
          applyRoleStatusUpdate(payload.role, currentJobEl);
        }
        removePrepFeedbackItem(roleId, currentIndex, analysis);
      } else {
        await ignorePrepFeedback(roleId, currentIndex, feedbackItem, comment);
        removePrepFeedbackItem(roleId, currentIndex, analysis);
      }
    } catch {
      feedbackButton.disabled = false;
      feedbackButton.textContent = originalLabel;
    }
    return;
  }

  const direction = feedbackButton.dataset.prepFeedback === "next" ? 1 : -1;
  prepFeedbackIndexByRoleId.set(
    roleId,
    Math.max(0, Math.min(currentIndex + direction, itemCount - 1)),
  );
  prepCard.querySelector(".prep-analysis")?.replaceWith(
    htmlToElement(renderPrepAnalysis(prepQueue[0], { analysis })),
  );
});

function removePrepFeedbackItem(roleId, feedbackIndex, analysis) {
  const remainingItems = analysis.feedback_items.filter(
    (_item, itemIndex) => itemIndex !== feedbackIndex,
  );
  const nextIndex = Math.min(feedbackIndex, Math.max(remainingItems.length - 1, 0));
  const nextAnalysis = {
    ...analysis,
    feedback_items: remainingItems,
    verdict: remainingItems.length === 0 ? "ready_to_apply" : analysis.verdict,
  };
  prepFeedbackIndexByRoleId.set(roleId, nextIndex);
  prepAnalysisByRoleId.set(roleId, nextAnalysis);
  prepCard.querySelector(".prep-analysis")?.replaceWith(
    htmlToElement(renderPrepAnalysis(prepQueue[0], { analysis: nextAnalysis })),
  );
}

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !searchDialog.hidden) closeSearchDialog();
  if (event.key === "Escape" && !reviewView.hidden) closeReviewView();
  if (event.key === "Escape" && !prepView.hidden) closePrepView();
  if (event.key === "Escape" && !settingsView.hidden) closeSettingsView();
});

function statusPaneToggles() {
  return Array.from(document.querySelectorAll(".pane-toggle"));
}

function hasExpandedStatusPane() {
  return statusPaneToggles().some((toggle) => toggle.getAttribute("aria-expanded") === "true");
}

function updateToggleAllButton() {
  toggleAllButton.textContent = hasExpandedStatusPane() ? "collapse all" : "expand all";
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
  collapseEmptyButton.textContent = hideEmpty ? "show empty" : "hide empty";
  if (trackerData) renderStatuses(trackerData.statuses);
});

settingsOpenButton.addEventListener("click", openSettingsView);

settingsCloseButton.addEventListener("click", closeSettingsView);

settingsForm.addEventListener("change", (event) => {
  const control = event.target.closest('input[type="checkbox"], select');
  if (!control) return;
  saveSetting(control);
});

clearRecommendationHistoryButton.addEventListener("click", clearRecommendationHistory);

loadTracker().catch(() => {
  statusListEl.innerHTML = '<p class="empty-copy">could not load jobs.</p>';
});

loadApplicationMaterials({ applyDefaultCollapsed: true }).catch(() => {
  renderMasterResume(null, "could not load resume.");
  renderCoverLetterExamples([], "could not load cover letter examples.");
  updateMaterialsSummary();
});

loadScanStatus()
  .then(() => {
    startScanStatusPolling();
  })
  .catch(() => {
    scanStatusText.textContent = "could not load scan status";
  });
