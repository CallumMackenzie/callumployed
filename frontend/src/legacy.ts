// @ts-nocheck -- Legacy controller preserved during the React/TypeScript shell migration.
export {};
const {sankey: d3Sankey, sankeyLinkHorizontal} = await import(
  /* @vite-ignore */ "/assets/d3-sankey.js"
);

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
const materialsRequiredWarning = document.querySelector("#materials-required-warning");
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
const experienceNoteMeta = document.querySelector("#experience-note-meta");
const experienceNoteUpload = document.querySelector("#experience-note-upload");
const experienceNoteUploadButton = document.querySelector("#experience-note-upload-button");
const experienceNoteList = document.querySelector("#experience-note-list");
const materialIndexButton = document.querySelector("#material-index-button");
const materialIndexWarning = document.querySelector("#material-index-warning");
const materialIndexStatus = document.querySelector("#material-index-status");
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
const preppedRolesButton = document.querySelector("#prepped-roles");
const preppedView = document.querySelector("#prepped-view");
const closePreppedButton = document.querySelector("#close-prepped");
const preppedSummary = document.querySelector("#prepped-summary");
const regenerateAllCoverLettersButton = document.querySelector("#regenerate-all-cover-letters");
const preppedBulkStatus = document.querySelector("#prepped-bulk-status");
const preppedList = document.querySelector("#prepped-list");
const preppedDetail = document.querySelector("#prepped-detail");
const scanAllButton = document.querySelector("#scan-all-button");
const manageCompaniesButton = document.querySelector("#manage-companies-button");
const scanStatusBar = document.querySelector("#scan-status-bar");
const scanStatusText = document.querySelector("#scan-status-text");
const scanLastTime = document.querySelector("#scan-last-time");
const scanFailuresOpenButton = document.querySelector("#scan-failures-open");
const scanFailuresDialog = document.querySelector("#scan-failures-dialog");
const scanFailuresBackdrop = document.querySelector("#scan-failures-backdrop");
const scanFailuresCloseButton = document.querySelector("#scan-failures-close");
const scanFailuresList = document.querySelector("#scan-failures-list");
const toggleAllButton = document.querySelector("#toggle-all");
const collapseEmptyButton = document.querySelector("#collapse-empty");
const toolbarSummary = document.querySelector("#toolbar-summary");
const settingsOpenButton = document.querySelector("#settings-open");
const settingsView = document.querySelector("#settings-view");
const settingsCloseButton = document.querySelector("#settings-close");
const settingsStatus = document.querySelector("#settings-status");
const settingsForm = document.querySelector("#settings-form");
const settingsProfileOptions = document.querySelector("#settings-profile-options");
const settingsAutoprepOptions = document.querySelector("#settings-autoprep-options");
const settingsOptions = document.querySelector("#settings-options");
const centralStoreSummary = document.querySelector("#central-store-summary");
const centralStoreSyncSummary = document.querySelector("#central-store-sync-summary");
const centralApiUrlInput = document.querySelector("#central-api-url-input");
const centralPasskeyInput = document.querySelector("#central-passkey-input");
const centralSaveButton = document.querySelector("#central-save-button");
const centralSyncButton = document.querySelector("#central-sync-button");
const recommendationHistorySummary = document.querySelector("#recommendation-history-summary");
const clearRecommendationHistoryButton = document.querySelector("#clear-recommendation-history");
const metricsOpenButton = document.querySelector("#metrics-open-button");
const metricsView = document.querySelector("#metrics-view");
const metricsCloseButton = document.querySelector("#metrics-close");
const metricsStatus = document.querySelector("#metrics-status");
const metricsOverview = document.querySelector("#metrics-overview");
const metricsSections = document.querySelector("#metrics-sections");
const metricsScanList = document.querySelector("#metrics-scan-list");
const sankeyOpenButton = document.querySelector("#sankey-open-button");
const sankeyView = document.querySelector("#sankey-view");
const sankeyCloseButton = document.querySelector("#sankey-close");
const sankeyStatus = document.querySelector("#sankey-status");
const sankeyCanvas = document.querySelector("#sankey-canvas");
const sankeyPathList = document.querySelector("#sankey-path-list");
const appUpdateButton = document.querySelector("#app-update-button");
const companiesView = document.querySelector("#companies-view");
const companiesCloseButton = document.querySelector("#companies-close");
const companiesStatus = document.querySelector("#companies-status");
const companyCreateForm = document.querySelector("#company-create-form");
const companiesList = document.querySelector("#companies-list");
const roleAddForm = document.querySelector("#role-add-form");
const roleUrlInput = document.querySelector("#role-url-input");
const roleCompanyInput = document.querySelector("#role-company-input");
const roleCompanyOptions = document.querySelector("#role-company-options");
const roleAddStatus = document.querySelector("#role-add-status");

const REVIEW_LATER_RECOMMENDATION_THRESHOLD = 3;
const COVER_LETTER_AUTOSAVE_DELAY_MS = 1200;
const APPLICATION_STATUSES = new Set(["applied", "OA", "interview", "rejected", "offer"]);
const STATUS_COLORS = new Map([
  ["discovered", "#4f6472"],
  ["interested", "#00897b"],
  ["disinterested", "#626970"],
  ["applied", "#2257ad"],
  ["oa", "#b36b00"],
  ["interview", "#5f2bd8"],
  ["rejected", "#b93d2d"],
  ["offer", "#137347"],
  ["closed", "#53606b"],
  ["archived", "#765b4a"],
]);
const DESCRIPTION_SECTION_HEADING_PATTERN = /^(?:about (?:the )?(?:role|team|job)|about this role|job description|job responsibilities|minimum qualifications|preferred qualifications|qualifications|requirements|responsibilities|what to expect|what (?:you'll|you’ll|you will) (?:bring|do)|what'?s in it for you|who you are|your objectives|your skills & talents):?$/i;
let hideEmpty = true;
let trackerData = null;
let masterResume = null;
let resumeResources = [];
let coverLetterExamples = [];
let experienceNotes = [];
let materialIndex = null;
let reviewQueue = [];
let prepQueue = [];
let prepAnalysisByRoleId = new Map();
let prepFeedbackIndexByRoleId = new Map();
let prepResumeByRoleId = new Map();
let prepResumeTweaksByRoleId = new Map();
let prepCoverLetterByRoleId = new Map();
let prepRoleChatByRoleId = new Map();
let prepResumeSaveStateByRoleId = new Map();
let prepCoverLetterSaveStateByRoleId = new Map();
let preppedJobs = [];
let selectedPreppedRoleId = null;
let preppedPoll = null;
let bulkCoverLetterRegenerationPending = false;
let preppedBulkMessage = "";
let preppedBulkRegeneration = null;
const preppedStatusChangeRoleIds = new Set();
const preppedCommentsByDocument = new Map();
const openPreppedPreviews = new Set();
const preppedPreviewBlobUrls = new Map();
const preppedPreviewVersions = new Map();
const preppedPreviewErrors = new Map();
const loadingPreppedPreviews = new Set();
let materialsInitialized = false;
let materialsRenderVersion = 0;
let scanStatusPoll = null;
let wasScanning = false;
let scanStatusData = null;
let settingsData = null;
let metricsData = null;
let sankeyData = null;
let companiesData = null;
let roleCompanyData = [];
const companySaveTimers = new Map();

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

function safeExternalHttpUrl(value) {
  try {
    const url = new URL(String(value || ""));
    return ["http:", "https:"].includes(url.protocol) ? url.href : "";
  } catch {
    return "";
  }
}

function findLatexCommandEnd(value, start) {
  let index = start;
  while (index < value.length && /[A-Za-z@]/.test(value[index])) {
    index += 1;
  }
  return index > start ? index : Math.min(start + 1, value.length);
}

function findLatexBraceEnd(value, start) {
  if (value[start] !== "{") return start;
  let index = start + 1;
  while (index < value.length && value[index] !== "}") {
    index += 1;
  }
  return index < value.length ? index + 1 : index;
}

function renderLatexEnvironmentToken(command, value, start) {
  const braceEnd = findLatexBraceEnd(value, start);
  if (braceEnd === start) {
    return {
      html: `<span class="latex-token-command">${escapeHtml(command)}</span>`,
      end: start,
    };
  }
  const environment = value.slice(start + 1, Math.max(start + 1, braceEnd - 1));
  return {
    html: [
      `<span class="latex-token-command">${escapeHtml(command)}</span>`,
      '<span class="latex-token-punctuation">{</span>',
      `<span class="latex-token-environment">${escapeHtml(environment)}</span>`,
      braceEnd > start + 1 ? '<span class="latex-token-punctuation">}</span>' : "",
    ].join(""),
    end: braceEnd,
  };
}

function renderLatexHighlight(value) {
  const source = String(value ?? "");
  const parts = [];
  let index = 0;

  while (index < source.length) {
    const char = source[index];
    const previous = index > 0 ? source[index - 1] : "";

    if (char === "%" && previous !== "\\") {
      const nextLine = source.indexOf("\n", index);
      const end = nextLine === -1 ? source.length : nextLine;
      parts.push(`<span class="latex-token-comment">${escapeHtml(source.slice(index, end))}</span>`);
      index = end;
      continue;
    }

    if (char === "\\") {
      const commandEnd = findLatexCommandEnd(source, index + 1);
      const command = source.slice(index, commandEnd);
      if ((command === "\\begin" || command === "\\end") && source[commandEnd] === "{") {
        const token = renderLatexEnvironmentToken(command, source, commandEnd);
        parts.push(token.html);
        index = token.end;
        continue;
      }
      parts.push(`<span class="latex-token-command">${escapeHtml(command)}</span>`);
      index = commandEnd;
      continue;
    }

    if (char === "$") {
      const delimiter = source[index + 1] === "$" ? "$$" : "$";
      const end = source.indexOf(delimiter, index + delimiter.length);
      const tokenEnd = end === -1 ? source.length : end + delimiter.length;
      parts.push(`<span class="latex-token-math">${escapeHtml(source.slice(index, tokenEnd))}</span>`);
      index = tokenEnd;
      continue;
    }

    if ("{}[]".includes(char)) {
      parts.push(`<span class="latex-token-punctuation">${escapeHtml(char)}</span>`);
      index += 1;
      continue;
    }

    let next = index + 1;
    while (next < source.length && !"%\\${}[]".includes(source[next])) {
      next += 1;
    }
    parts.push(escapeHtml(source.slice(index, next)));
    index = next;
  }

  return parts.join("") || " ";
}

function syncLatexEditorHighlight(textarea) {
  return textarea;
}

function enhanceLatexEditor(textarea) {
  return textarea;
}

function enhancePrepLatexEditors(root = prepCard) {
  root
    .querySelectorAll("[data-prep-resume-latex], [data-prep-cover-letter-latex]")
    .forEach(enhanceLatexEditor);
}

function renderLinkIcon() {
  return `
    <svg class="role-link-icon" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M7 17 17 7"></path>
      <path d="M8 7h9v9"></path>
    </svg>
  `;
}

function renderPlusIcon() {
  return `
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 5v14"></path>
      <path d="M5 12h14"></path>
    </svg>
  `;
}

function renderTrashIcon() {
  return `
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M3 6h18"></path>
      <path d="M8 6V4h8v2"></path>
      <path d="m19 6-1 14H6L5 6"></path>
      <path d="M10 11v5"></path>
      <path d="M14 11v5"></path>
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

function renderMaterialSourceItem(item, materialType, size, {binary = false} = {}) {
  const identifier = binary ? item.filename : item.id;
  return `
    <li class="material-source-item" title="${escapeUiText(item.filename)}">
      <div class="material-source-copy">
        <span>${escapeUiText(item.filename)}</span>
        <small>${escapeHtml(size)}</small>
      </div>
      <div class="material-source-actions">
        <button type="button" class="material-source-view" data-material-view="${escapeHtml(materialType)}" data-material-id="${escapeHtml(identifier)}" data-material-binary="${binary}">preview</button>
        <button type="button" class="material-source-remove" data-material-remove="${escapeHtml(materialType)}" data-material-id="${escapeHtml(identifier)}" data-material-name="${escapeUiText(item.filename)}">remove</button>
      </div>
      <div class="material-source-preview" data-material-preview-body hidden></div>
    </li>`;
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
  coverLetterList.innerHTML = coverLetterExamples
    .map((example) => renderMaterialSourceItem(example, "cover-letter-examples", formatFileSize(example.content_bytes)))
    .join("");
}

function renderExperienceNotes(notes, message = "") {
  experienceNotes = Array.isArray(notes) ? notes : [];
  experienceNoteUploadButton.textContent = experienceNotes.length > 0 ? "add" : "upload";
  if (message) {
    experienceNoteMeta.textContent = message;
  } else if (experienceNotes.length === 0) {
    experienceNoteMeta.textContent = "no notes uploaded";
  } else {
    experienceNoteMeta.textContent = `${experienceNotes.length} ${experienceNotes.length === 1 ? "note" : "notes"} stored`;
  }
  experienceNoteList.innerHTML = experienceNotes
    .map((note) => renderMaterialSourceItem(note, "experience-notes", formatFileSize(note.content_bytes)))
    .join("");
}

function renderMaterialIndex(index, message = "") {
  materialIndex = index ?? null;
  const status = materialIndex?.status ?? "missing";
  const needsIndex = status !== "ready";
  const hasNotes = experienceNotes.length > 0;
  materialIndexWarning.hidden = !needsIndex;
  materialIndexWarning.textContent = message || materialIndex?.warning || "";

  if (message) {
    materialIndexStatus.textContent = message;
  } else if (status === "ready") {
    const pageCount = Number(materialIndex?.document_count ?? 0);
    const skippedCount = Number(materialIndex?.skipped_source_count ?? 0);
    const indexedAt = formatCompactDate(materialIndex?.generated_at);
    const parts = [
      `${pageCount} indexed ${pageCount === 1 ? "page" : "pages"}`,
      skippedCount ? `${skippedCount} unreadable upload skipped` : "",
      indexedAt,
    ].filter(Boolean);
    materialIndexStatus.innerHTML = parts
      .map(
        (part) =>
          `<button type="button" class="material-index-link" data-open-material-index title="Reveal the application material index in Finder">${escapeUiText(part)}</button>`,
      )
      .join('<span aria-hidden="true"> | </span>');
  } else if (status === "stale") {
    materialIndexStatus.textContent = "index out of date";
  } else {
    materialIndexStatus.textContent = "not indexed";
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

  resumeResourceList.innerHTML = resumeResources
    .map((resource) =>
      renderMaterialSourceItem(
        resource,
        "resume-resources",
        formatFileSize(resource.bytes),
        {binary: true},
      ),
    )
    .join("");
}

function renderApplicationMaterials(payload, options = {}) {
  materialsRenderVersion += 1;
  document.querySelectorAll("[data-preview-blob-url]").forEach((preview) => {
    URL.revokeObjectURL(preview.dataset.previewBlobUrl);
  });
  renderMasterResume(payload?.master_resume ?? null);
  renderResumeResources(payload?.resume_resources ?? []);
  renderCoverLetterExamples(payload?.cover_letter_examples ?? []);
  renderExperienceNotes(payload?.experience_notes ?? []);
  renderMaterialIndex(payload?.material_index ?? null);
  updateMaterialsSummary(payload?.ui);
  if (!materialsInitialized || options.applyDefaultCollapsed) {
    setMaterialsCollapsed(Boolean(payload?.ui?.default_collapsed));
    materialsInitialized = true;
  }
}

function updateMaterialsSummary(ui = null) {
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
  const noteCount = experienceNotes.length;
  const noteText =
    noteCount === 0
      ? "no notes"
      : `${noteCount} experience ${noteCount === 1 ? "note" : "notes"}`;
  const hasMissingRequiredMaterials =
    typeof ui?.has_missing_required_materials === "boolean"
      ? ui.has_missing_required_materials
      : !masterResume || exampleCount === 0 || noteCount === 0;
  materialsRequiredWarning.hidden = !hasMissingRequiredMaterials;
  materialsSummary.textContent = `${resumeText} | ${resourceText} | ${coverText} | ${noteText}`;
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

async function fetchPdfBlobUrl(url) {
  const response = await fetch(url, {cache: "no-store"});
  if (!response.ok) throw new Error("Preview unavailable");
  const bytes = await response.arrayBuffer();
  const signature = new TextDecoder("ascii").decode(bytes.slice(0, 5));
  if (signature !== "%PDF-") throw new Error("The selected file is not a readable PDF.");
  return URL.createObjectURL(new Blob([bytes], {type: "application/pdf"}));
}

async function toggleMaterialPreview(button) {
  const item = button.closest(".material-source-item");
  const preview = item?.querySelector("[data-material-preview-body]");
  if (!preview) return;
  if (preview.dataset.loaded === "true") {
    preview.hidden = !preview.hidden;
    button.textContent = preview.hidden ? "preview" : "hide";
    return;
  }
  button.disabled = true;
  button.textContent = "loading...";
  const materialType = button.dataset.materialView;
  const identifier = button.dataset.materialId;
  const renderVersion = materialsRenderVersion;
  const url = `/api/${encodeURIComponent(materialType)}/${encodeURIComponent(identifier)}`;
  try {
    if (button.dataset.materialBinary === "true") {
      const blobUrl = await fetchPdfBlobUrl(url);
      if (!preview.isConnected || materialsRenderVersion !== renderVersion) {
        URL.revokeObjectURL(blobUrl);
        return;
      }
      preview.dataset.previewBlobUrl = blobUrl;
      preview.innerHTML = `<iframe title="${escapeUiText(identifier)} preview"></iframe>`;
      preview.querySelector("iframe").src = blobUrl;
    } else {
      const response = await fetch(url);
      if (!response.ok) throw new Error("Preview unavailable");
      const payload = await response.json();
      const pre = document.createElement("pre");
      pre.textContent = payload.content || "This source is empty.";
      preview.replaceChildren(pre);
    }
    preview.dataset.loaded = "true";
    preview.hidden = false;
    button.textContent = "hide";
  } catch (error) {
    preview.textContent = error instanceof Error ? error.message : "Preview unavailable";
    preview.hidden = false;
    button.textContent = "preview";
  } finally {
    button.disabled = false;
  }
}

async function removeApplicationMaterial(button) {
  const materialType = button.dataset.materialRemove;
  const identifier = button.dataset.materialId;
  if (button.dataset.confirmRemove !== "true") {
    button.dataset.confirmRemove = "true";
    button.textContent = "confirm remove";
    button.classList.add("danger");
    window.setTimeout(() => {
      if (!button.isConnected || button.disabled) return;
      delete button.dataset.confirmRemove;
      button.textContent = "remove";
      button.classList.remove("danger");
    }, 6_000);
    return;
  }
  button.disabled = true;
  button.textContent = "removing...";
  try {
    const response = await fetch(
      `/api/${encodeURIComponent(materialType)}/${encodeURIComponent(identifier)}`,
      {method: "DELETE"},
    );
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "Remove failed");
    renderApplicationMaterials(payload);
  } catch (error) {
    button.disabled = false;
    delete button.dataset.confirmRemove;
    button.classList.remove("danger");
    button.textContent = "remove";
    window.alert(error instanceof Error ? error.message : "Remove failed");
  }
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
          ${statusKey === "interested" && job.prep_started ? renderPrepStartedDot() : ""}
          ${statusKey === "closed" && job.updated_in_latest_scan ? renderLatestScanDot() : ""}
          ${["discovered", "interested"].includes(statusKey) && job.missing_from_latest_scan ? renderMissingLatestScanDot() : ""}
        </span>
      </summary>
      <div class="job-detail">
        ${statusKey === "discovered" ? renderDiscoveredActions(job) : ""}
        ${statusKey === "interested" ? renderInterestedActions(job) : ""}
        ${statusKey === "disinterested" ? renderDisinterestedActions(job) : ""}
        ${statusKey === "applied" ? renderAppliedActions(job) : ""}
        ${statusKey === "OA" ? renderOaActions(job) : ""}
        ${statusKey === "interview" ? renderInterviewActions(job) : ""}
        ${statusKey === "closed" ? renderClosedActions(job) : ""}
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

function renderLatestScanDot() {
  return '<span class="latest-scan-dot" title="updated in latest scan" aria-label="updated in latest scan"></span>';
}

function renderMissingLatestScanDot() {
  return '<span class="missing-latest-scan-dot" title="not seen in latest scan" aria-label="not seen in latest scan"></span>';
}

function renderPrepStartedDot() {
  return '<span class="prep-started-dot" title="application materials started" aria-label="application materials started"></span>';
}

function renderDiscoveredActions(job) {
  return `
    <div class="job-actions job-actions-nowrap" aria-label="discovered role actions">
      <button class="job-action success" type="button" data-review-role-id="${job.id}">view</button>
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

function renderDisinterestedActions(job) {
  return `
    <div class="job-actions" aria-label="disinterested role actions">
      <button class="job-action success" type="button" data-role-id="${job.id}" data-status="interested">interested</button>
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

function renderClosedActions(job) {
  return `
    <div class="job-actions" aria-label="closed role actions">
      <button class="job-action" type="button" data-role-id="${job.id}" data-status="interested">interested</button>
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
  scanStatusData = payload ?? null;
  const scanning = Boolean(payload?.scanning);
  const cancelRequested = scanning && Boolean(payload?.cancel_requested);
  const completed = Number(payload?.completed_companies ?? 0);
  const total = Number(payload?.total_companies ?? 0);
  const failed = Number(payload?.failed_companies ?? 0);
  const errorText = typeof payload?.error === "string" ? payload.error.trim() : "";
  const failures = Array.isArray(payload?.failures) ? payload.failures : [];

  scanAllButton.disabled = cancelRequested;
  scanAllButton.textContent = scanning
    ? cancelRequested
      ? "cancelling..."
      : "cancel scan"
    : "scan roles";
  scanAllButton.classList.toggle("danger", scanning && !cancelRequested);
  scanStatusBar.hidden = !scanning && !errorText && failures.length === 0;
  scanStatusBar.classList.toggle("scanning", scanning);
  scanStatusBar.classList.toggle("scan-error", (!scanning && Boolean(errorText)) || failures.length > 0);

  if (cancelRequested) {
    scanStatusText.textContent = "cancelling scan...";
  } else if (scanning) {
    const progressText = total > 0 ? ` ${completed}/${total}` : "";
    const failureText = failed > 0 ? `, ${failed} failed` : "";
    scanStatusText.textContent = `scanning roles${progressText}${failureText}`;
  } else if (failures.length > 0) {
    scanStatusText.textContent = `${failures.length} recent scan ${failures.length === 1 ? "failure" : "failures"}`;
  } else if (errorText) {
    scanStatusText.textContent = `last scan error: ${errorText}`;
  } else {
    scanStatusText.textContent = "scan idle";
  }

  if (scanFailuresOpenButton && scanFailuresList) {
    scanFailuresOpenButton.hidden = failures.length === 0;
    scanFailuresList.innerHTML = failures
      .slice(0, 5)
      .map((failure) => {
        const company = failure?.company_name || "unknown company";
        const error = failure?.error || "scan failed";
        return `
          <p>
            <span>${escapeUiText(company)}</span>
            <span>${escapeHtml(error)}</span>
          </p>
        `;
      })
      .join("");
    if (failures.length === 0) closeScanFailuresDialog();
  }

  const lastScanAt = payload?.last_scan_at;
  scanLastTime.textContent = lastScanAt ? `last scan: ${formatCompactDate(lastScanAt)}` : "last scan: never";

  if (wasScanning && !scanning) {
    loadTracker(getActiveSearchQuery()).catch(() => {});
  }
  wasScanning = scanning;
}

function openScanFailuresDialog() {
  if (scanFailuresOpenButton.hidden) return;
  scanFailuresDialog.hidden = false;
  scanFailuresCloseButton.focus();
}

function closeScanFailuresDialog() {
  scanFailuresDialog.hidden = true;
}

function renderSettings(payload, message = "") {
  settingsData = payload;
  const settings = Array.isArray(payload?.settings) ? payload.settings : [];
  const profileSettings = settings.filter((setting) => setting.key?.startsWith("applicant_"));
  const autoprepSettings = settings.filter((setting) => setting.key?.startsWith("autoprep_"));
  const filterSettings = settings.filter(
    (setting) => !setting.key?.startsWith("applicant_") && !setting.key?.startsWith("autoprep_"),
  );
  const central = payload?.central ?? {};
  settingsStatus.textContent = message;
  settingsStatus.classList.toggle("is-empty", !message);
  const historyCount = Number(payload?.recommendation_history_count ?? 0);
  recommendationHistorySummary.textContent =
    historyCount > 0
      ? `${historyCount} saved ${historyCount === 1 ? "feedback decision" : "feedback decisions"}`
      : "no saved resume feedback decisions";
  clearRecommendationHistoryButton.disabled = historyCount === 0;
  renderCentralSettings(central);
  settingsProfileOptions.innerHTML = profileSettings
    .map((setting) => renderSettingOption(setting))
    .join("");
  settingsAutoprepOptions.innerHTML = autoprepSettings
    .map((setting) => renderSettingOption(setting))
    .join("");
  settingsOptions.innerHTML = filterSettings
    .map((setting) => renderSettingOption(setting))
    .join("");
  setSettingsDisabled(false);
}

function renderCentralSettings(central) {
  const apiUrl = central?.api_url ?? "";
  centralApiUrlInput.value = apiUrl;
  centralPasskeyInput.value = "";
  const passkeyText = central?.passkey_configured ? "passkey saved" : "no passkey saved";
  centralStoreSummary.textContent = apiUrl
    ? `${formatUiText(apiUrl)} | ${passkeyText}`
    : `no api url | ${passkeyText}`;
  const linked = Number(central?.companies_linked ?? 0);
  const unlinked = Number(central?.companies_unlinked ?? 0);
  const needsReview = Number(central?.companies_needs_review ?? 0);
  const failed = Number(central?.companies_failed ?? 0);
  centralStoreSyncSummary.textContent =
    `${linked} linked | ${unlinked} unlinked | ${needsReview} review | ${failed} failed`;
  centralSyncButton.disabled = !apiUrl;
}

function renderSettingOption(setting) {
  if (setting.control === "textarea" && setting.editable !== false) {
    return renderTextareaSettingOption(setting);
  }
  if (setting.control === "text" && setting.editable !== false) {
    return renderTextSettingOption(setting);
  }
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

function renderTextSettingOption(setting) {
  const defaultText = setting.default ? `default: ${formatUiText(setting.default)}` : "optional";
  const inputType = setting.input_type ?? "text";
  const autocomplete = setting.autocomplete ?? "name";
  return `
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${escapeUiText(setting.label)}</span>
        <span class="setting-description">${escapeUiText(setting.description)}</span>
        <span class="setting-default">${escapeUiText(defaultText)}</span>
      </span>
      <input
        class="setting-text-input"
        data-setting-text
        name="${escapeHtml(setting.key)}"
        type="${escapeHtml(inputType)}"
        value="${escapeHtml(setting.value ?? "")}"
        autocomplete="${escapeHtml(autocomplete)}"
      />
    </label>
  `;
}

function renderTextareaSettingOption(setting) {
  return `
    <label class="setting-option setting-option-prompt">
      <span class="setting-copy">
        <span class="setting-label">${escapeUiText(setting.label)}</span>
        <span class="setting-description">${escapeUiText(setting.description)}</span>
      </span>
      <textarea
        class="setting-prompt-input"
        data-setting-textarea
        name="${escapeHtml(setting.key)}"
        rows="7"
        maxlength="8000"
      >${escapeUiText(setting.value ?? "")}</textarea>
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
  settingsForm.querySelectorAll("input, select, textarea").forEach((input) => {
    input.disabled = disabled;
  });
  centralSaveButton.disabled = disabled;
  centralSyncButton.disabled = disabled || !centralApiUrlInput.value.trim();
  appUpdateButton.disabled = disabled;
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

function formatMetricValue(metric) {
  const value = metric?.value;
  if (value === null || value === undefined) return "n/a";
  if (metric?.kind === "ratio") {
    return Number(value).toLocaleString(undefined, {
      maximumFractionDigits: 2,
      minimumFractionDigits: 0,
    });
  }
  if (typeof value === "number") return value.toLocaleString();
  return formatUiText(value);
}

function renderMetricCard(metric, className = "metric-card") {
  return `
    <article class="${className}">
      <span>${escapeUiText(metric?.label)}</span>
      <strong>${escapeHtml(formatMetricValue(metric))}</strong>
    </article>
  `;
}

function renderMetrics(payload, message = "") {
  metricsData = payload;
  metricsStatus.textContent = message || (payload?.updated_at ? `updated ${formatCompactDate(payload.updated_at)}` : "");
  metricsStatus.classList.toggle("is-empty", !metricsStatus.textContent);
  const overview = Array.isArray(payload?.overview) ? payload.overview : [];
  const sections = Array.isArray(payload?.sections) ? payload.sections : [];
  const recentScans = Array.isArray(payload?.recent_scans) ? payload.recent_scans : [];
  metricsOverview.innerHTML = overview.map((metric) => renderMetricCard(metric)).join("");
  metricsSections.innerHTML = sections.map(renderMetricsSection).join("");
  metricsScanList.innerHTML = recentScans.length
    ? recentScans.map(renderMetricsScan).join("")
    : '<p class="empty-copy">no scan runs recorded.</p>';
}

function renderMetricsSection(section) {
  const metrics = Array.isArray(section?.metrics) ? section.metrics : [];
  return `
    <section class="metrics-section">
      <div class="metrics-section-heading">
        <h3>${escapeUiText(section?.title)}</h3>
      </div>
      <div class="metrics-section-grid">
        ${metrics.map((metric) => renderMetricCard(metric, "metric-card metric-card-compact")).join("")}
      </div>
    </section>
  `;
}

function renderMetricsScan(scan) {
  const status = scan?.scan_status ?? "unknown";
  const started = scan?.started_at ? formatCompactDate(scan.started_at) : "not started";
  const finished = scan?.finished_at ? formatCompactDate(scan.finished_at) : "not finished";
  const error = scan?.error ? `<span>${escapeUiText(scan.error)}</span>` : "";
  return `
    <article class="metrics-scan-row">
      <div>
        <strong>${escapeUiText(scan?.company_name ?? "unknown company")}</strong>
        <span>${escapeUiText(started)} -> ${escapeUiText(finished)}</span>
        ${error}
      </div>
      <span class="metrics-status-pill">${escapeUiText(status)}</span>
    </article>
  `;
}

async function openMetricsView() {
  metricsView.hidden = false;
  document.body.classList.add("metrics-open");
  metricsCloseButton.focus();
  if (metricsData) {
    renderMetrics(metricsData);
  } else {
    metricsStatus.textContent = "loading metrics...";
    metricsStatus.classList.remove("is-empty");
    metricsOverview.innerHTML = "";
    metricsSections.innerHTML = "";
    metricsScanList.innerHTML = "";
  }
  try {
    await loadMetrics();
  } catch {
    metricsStatus.textContent = "could not load metrics.";
  }
}

function closeMetricsView() {
  metricsView.hidden = true;
  document.body.classList.remove("metrics-open");
  metricsOpenButton.focus();
}

async function loadMetrics() {
  const response = await fetch("/api/metrics");
  if (!response.ok) throw new Error("Metrics request failed");
  renderMetrics(await response.json());
}

function renderSankey(payload, message = "") {
  sankeyData = payload;
  const roleCount = Number(payload?.role_count ?? 0);
  const links = Array.isArray(payload?.links) ? payload.links : [];
  const paths = Array.isArray(payload?.paths) ? payload.paths : [];
  sankeyStatus.textContent =
    message || (payload?.updated_at ? `${roleCount.toLocaleString()} roles | updated ${formatCompactDate(payload.updated_at)}` : "");
  sankeyStatus.classList.toggle("is-empty", !sankeyStatus.textContent);
  sankeyCanvas.innerHTML = links.length
    ? renderSankeySvg(payload)
    : '<p class="empty-copy">no role transitions recorded yet.</p>';
  sankeyPathList.innerHTML = paths.length
    ? paths.map(renderSankeyPath).join("")
    : '<p class="empty-copy">no role paths recorded yet.</p>';
}

function renderSankeySvg(payload) {
  const nodes = Array.isArray(payload?.nodes) ? payload.nodes : [];
  const links = Array.isArray(payload?.links) ? payload.links : [];
  const layout = buildSankeyLayout(nodes, links);
  const flowNodes = layout.nodes;
  const linkOffsets = layout.links;
  const flowLinks = layout.flowLinks ?? links;
  const linkMarkup = flowLinks
    .map((link) => {
      const source = flowNodes.get(link.source);
      const target = flowNodes.get(link.target);
      const offsets = linkOffsets.get(link);
      if (!source || !target) return "";
      if (!offsets) return "";
      const width = offsets.width;
      const isBacktrack = target.x < source.x;
      const color = getStatusColor(link.target);
      const fillOpacity = offsets.priority ? "0.42" : isBacktrack ? "0.28" : "0.34";
      const path = offsets.path ?? buildSankeyRibbonPath({
        isBacktrack,
        sourceX: source.x + source.width,
        sourceY: offsets.sourceY,
        targetX: target.x,
        targetY: offsets.targetY,
        width,
      });
      const classes = [
        "sankey-link",
        isBacktrack ? "sankey-link-backtrack" : "",
        offsets.priority ? "sankey-link-priority" : "",
      ]
        .filter(Boolean)
        .join(" ");
      return `
        <path class="${classes}" d="${path}" fill="${offsets.path ? "none" : color}" fill-opacity="${fillOpacity}" stroke="${color}" style="stroke-width: ${offsets.path ? width : 1}px">
          <title>${escapeUiText(source.label)} to ${escapeUiText(target.label)}: ${Number(link.value ?? 0).toLocaleString()}</title>
        </path>
      `;
    })
    .join("");
  const nodeMarkup = Array.from(flowNodes.values())
    .map((node) => {
      const historyCount = Number(node.history_count ?? node.current_count ?? 0);
      const flowCount = Number(node.value ?? historyCount);
      const countText = flowCount > 0 ? flowCount.toLocaleString() : "0";
      const labelOnLeft = node.x > layout.width - 180;
      const labelX = labelOnLeft ? node.x - 8 : node.x + node.width + 8;
      const labelY = Math.max(24, node.y - node.height / 2 - 16);
      const labelAnchor = labelOnLeft ? "end" : "start";
      const color = getStatusColor(node.id);
      return `
        <g class="sankey-node" transform="translate(${node.x}, ${node.y - node.height / 2})">
          <rect width="${node.width}" height="${node.height}" rx="7" fill="${color}" stroke="${color}"></rect>
        </g>
        <g class="sankey-node-label" transform="translate(${labelX}, ${labelY})">
          <text text-anchor="${labelAnchor}">${escapeUiText(node.label)}</text>
          <text class="sankey-node-count" y="16" text-anchor="${labelAnchor}">${escapeUiText(countText)} roles</text>
        </g>
      `;
    })
    .join("");
  return `
    <svg class="sankey-svg" viewBox="0 0 ${layout.width} ${layout.height}" role="img" aria-label="role state transition sankey diagram">
      <g>${linkMarkup}</g>
      <g>${nodeMarkup}</g>
    </svg>
  `;
}

function getStatusColor(statusKey) {
  return STATUS_COLORS.get(String(statusKey).toLowerCase()) ?? "#4f6472";
}

function buildSankeyRibbonPath({
  isBacktrack,
  sourceX,
  sourceY,
  targetX,
  targetY,
  width,
}) {
  const halfWidth = width / 2;
  const sourceTop = sourceY - halfWidth;
  const sourceBottom = sourceY + halfWidth;
  const targetTop = targetY - halfWidth;
  const targetBottom = targetY + halfWidth;
  if (isBacktrack) {
    const controlGap = Math.max(80, Math.abs(sourceX - targetX) * 0.42);
    return [
      `M ${sourceX} ${sourceTop}`,
      `C ${sourceX - controlGap} ${sourceTop}, ${targetX + controlGap} ${targetTop}, ${targetX} ${targetTop}`,
      `L ${targetX} ${targetBottom}`,
      `C ${targetX + controlGap} ${targetBottom}, ${sourceX - controlGap} ${sourceBottom}, ${sourceX} ${sourceBottom}`,
      "Z",
    ].join(" ");
  }
  const controlGap = Math.max(46, (targetX - sourceX) * 0.48);
  return [
    `M ${sourceX} ${sourceTop}`,
    `C ${sourceX + controlGap} ${sourceTop}, ${targetX - controlGap} ${targetTop}, ${targetX} ${targetTop}`,
    `L ${targetX} ${targetBottom}`,
    `C ${targetX - controlGap} ${targetBottom}, ${sourceX + controlGap} ${sourceBottom}, ${sourceX} ${sourceBottom}`,
    "Z",
  ].join(" ");
}

function buildSankeyLayout(nodes, links) {
  const statusColumns = new Map([
    ["discovered", 0],
    ["interested", 1],
    ["disinterested", 2],
    ["applied", 2],
    ["oa", 3],
    ["interview", 3],
    ["rejected", 4],
    ["closed", 4],
    ["archived", 4],
  ]);
  const incoming = new Map();
  const outgoing = new Map();
  links.forEach((link) => {
    incoming.set(link.target, (incoming.get(link.target) ?? 0) + Number(link.value ?? 0));
    outgoing.set(link.source, (outgoing.get(link.source) ?? 0) + Number(link.value ?? 0));
  });
  const visibleNodes = nodes.filter((node) => {
    const count = Number(node?.history_count ?? node?.current_count ?? 0);
    return count > 0 || incoming.has(node.id) || outgoing.has(node.id);
  });
  const visibleNodeIds = new Set(visibleNodes.map((node) => node.id));
  const validLinks = links.filter((link) => {
    return (
      visibleNodeIds.has(link.source) &&
      visibleNodeIds.has(link.target) &&
      Number(link.value ?? 0) > 0
    );
  });
  const width = 1120;
  const nodeWidth = 26;
  const height = 720;
  const statusLayer = (status) => statusColumns.get(String(status).toLowerCase()) ?? 0;
  const forwardLinks = validLinks.filter((link) => statusLayer(link.target) >= statusLayer(link.source));
  const backtrackLinks = validLinks.filter((link) => statusLayer(link.target) < statusLayer(link.source));
  const graph = {
    nodes: visibleNodes.map((node) => ({
      ...node,
      fixedValue: Math.max(0, Number(node?.history_count ?? node?.current_count ?? 0)),
    })),
    links: forwardLinks.map((link) => ({...link})),
  };
  const layoutGraph = d3Sankey()
    .nodeId((node) => node.id)
    .nodeWidth(nodeWidth)
    .nodePadding(44)
    .nodeAlign((node, layerCount) => Math.min(layerCount - 1, statusLayer(node.id)))
    .extent([
      [92, 88],
      [width - 106, height - 86],
    ])
    .iterations(32)(graph);
  const flowNodes = new Map();
  layoutGraph.nodes.forEach((node) => {
    flowNodes.set(node.id, {
      ...node,
      x: node.x0,
      y: node.y0 + (node.y1 - node.y0) / 2,
      width: node.x1 - node.x0,
      height: Math.max(1.5, node.y1 - node.y0),
      value: Number(node.fixedValue ?? node.value ?? 0),
    });
  });
  const linkOffsets = new Map();
  const renderLinks = [];
  const d3LinkPath = sankeyLinkHorizontal();
  layoutGraph.links.forEach((link) => {
    const renderLink = {
      source: link.source.id,
      target: link.target.id,
      value: link.value,
    };
    renderLinks.push(renderLink);
    linkOffsets.set(renderLink, {
      path: d3LinkPath(link),
      width: Math.max(1.5, link.width),
      sourceY: link.y0,
      targetY: link.y1,
      priority: Number(link.value ?? 0) >= 20,
    });
  });
  const linkScale = Math.max(
    0.6,
    ...layoutGraph.links.map((link) => Number(link.width ?? 0) / Math.max(1, Number(link.value ?? 0))),
  );
  backtrackLinks.forEach((link) => {
    const source = flowNodes.get(link.source);
    const target = flowNodes.get(link.target);
    if (!source || !target) return;
    const width = Math.max(1.5, Number(link.value ?? 0) * linkScale);
    const renderLink = {...link};
    renderLinks.push(renderLink);
    linkOffsets.set(renderLink, {
      width,
      sourceY: source.y + source.height / 2 - width / 2,
      targetY: target.y + target.height / 2 - width / 2,
      priority: false,
    });
  });
  renderLinks.sort((firstLink, secondLink) => {
    return (
      Number(firstLink.value ?? 0) - Number(secondLink.value ?? 0)
    );
  });
  return {flowLinks: renderLinks, height, links: linkOffsets, nodes: flowNodes, width};
}

function renderSankeyPath(pathItem) {
  const path = Array.isArray(pathItem?.path) ? pathItem.path : [];
  return `
    <article class="sankey-path-row">
      <div>
        <strong>${escapeUiText(pathItem?.company_name ?? "unknown company")} / ${escapeUiText(pathItem?.title ?? "untitled role")}</strong>
        <span>${path.map((status) => escapeUiText(status)).join(" -> ")}</span>
      </div>
      <span class="metrics-status-pill">${Number(pathItem?.loops_collapsed ?? 0).toLocaleString()} loops</span>
    </article>
  `;
}

async function openSankeyView() {
  settingsView.hidden = true;
  document.body.classList.remove("settings-open");
  sankeyView.hidden = false;
  document.body.classList.add("sankey-open");
  sankeyCloseButton.focus();
  if (sankeyData) {
    renderSankey(sankeyData);
  } else {
    sankeyStatus.textContent = "loading role flow...";
    sankeyStatus.classList.remove("is-empty");
    sankeyCanvas.innerHTML = "";
    sankeyPathList.innerHTML = "";
  }
  try {
    await loadSankey();
  } catch {
    sankeyStatus.textContent = "could not load role flow.";
  }
}

function closeSankeyView() {
  sankeyView.hidden = true;
  document.body.classList.remove("sankey-open");
  settingsOpenButton.focus();
}

async function loadSankey() {
  const response = await fetch("/api/role-sankey");
  if (!response.ok) throw new Error("Role sankey request failed");
  renderSankey(await response.json());
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

async function saveCentralSettings() {
  const apiUrl = centralApiUrlInput.value.trim();
  if (!apiUrl) {
    settingsStatus.textContent = "central api url is required.";
    settingsStatus.classList.remove("is-empty");
    return;
  }
  const payload = { central_api_url: apiUrl };
  const passkey = centralPasskeyInput.value.trim();
  if (passkey) payload.central_passkey = passkey;
  setSettingsDisabled(true);
  settingsStatus.textContent = "saving central settings...";
  settingsStatus.classList.remove("is-empty");
  try {
    const response = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) throw new Error("Central settings update failed");
    renderSettings(await response.json(), "central settings saved.");
  } catch {
    settingsStatus.textContent = "could not save central settings.";
    setSettingsDisabled(false);
  }
}

async function syncCentralCompanies() {
  centralSyncButton.disabled = true;
  settingsStatus.textContent = "syncing remote company ids...";
  settingsStatus.classList.remove("is-empty");
  try {
    const response = await fetch("/api/central/resolve-companies", { method: "POST" });
    if (!response.ok) throw new Error("Central company sync failed");
    const payload = await response.json();
    const result = payload.result ?? {};
    const pulled = payload.pulled_companies;
    const pullSummary = pulled
      ? ` remote: ${Number(pulled.created ?? 0)} created, ${Number(pulled.linked ?? 0)} linked, ${Number(pulled.existing ?? 0)} existing.`
      : "";
    renderSettings(
      payload.config,
      `company sync: ${Number(result.linked ?? 0)} matched, ${Number(result.created ?? 0)} created, ${Number(result.needs_review ?? 0)} review, ${Number(result.failed ?? 0)} failed.${pullSummary}`,
    );
    if (payload.companies) {
      companiesData = payload.companies;
      renderRoleCompanyOptions(payload.companies.companies);
    }
  } catch {
    settingsStatus.textContent = "could not sync companies.";
    centralSyncButton.disabled = !centralApiUrlInput.value.trim();
  }
}

async function syncCompaniesOnPageLoad() {
  const response = await fetch("/api/central/resolve-companies", { method: "POST" });
  if (!response.ok) throw new Error("Central company sync failed");
  const payload = await response.json();
  if (payload.companies) {
    companiesData = payload.companies;
    renderRoleCompanyOptions(payload.companies.companies);
  }
}

async function loadInitialTrackerData() {
  const companySync = syncCompaniesOnPageLoad().catch(() => {});
  await Promise.all([
    loadTracker().catch(() => {
      statusListEl.innerHTML = '<p class="empty-copy">could not load jobs.</p>';
    }),
    loadRoleCompanyOptions().catch(() => {
      roleAddStatus.textContent = "could not load companies.";
    }),
  ]);
  await companySync;
}

async function updateApp() {
  const confirmed = window.confirm("Update callumployed and restart the tracker?");
  if (!confirmed) return;
  setSettingsDisabled(true);
  appUpdateButton.disabled = true;
  settingsStatus.textContent = "updating callumployed; tracker will restart shortly...";
  settingsStatus.classList.remove("is-empty");
  try {
    const response = await fetch("/api/app/update", { method: "POST" });
    if (!response.ok) throw new Error("App update failed");
    settingsStatus.textContent = "update started. reconnect in a moment.";
  } catch {
    settingsStatus.textContent = "could not start update.";
    setSettingsDisabled(false);
  }
}

function renderCompanies(payload, message = "") {
  companiesData = payload;
  const companies = Array.isArray(payload?.companies) ? payload.companies : [];
  renderRoleCompanyOptions(companies);
  companiesStatus.textContent = message || `${companies.length} ${companies.length === 1 ? "company" : "companies"} stored`;
  companiesStatus.classList.toggle("is-empty", companies.length === 0 && !message);
  if (companies.length === 0) {
    companiesList.innerHTML = '<p class="empty-copy">no companies yet.</p>';
    return;
  }
  companiesList.innerHTML = companies.map((company) => renderCompanyAccordion(company)).join("");
}

function renderRoleCompanyOptions(companies) {
  roleCompanyData = Array.isArray(companies) ? companies : [];
  roleCompanyOptions.innerHTML = roleCompanyData
    .map((company) => `<option value="${escapeHtml(company.name)}"></option>`)
    .join("");
}

function renderCompanyAccordion(company) {
  const careerPages = Array.isArray(company.career_pages) ? company.career_pages : [];
  const updated = formatCompactDate(company.updated_at);
  const tierClass = renderCompanyTierClass(company.prestige_tier);
  const scanCount = Number(company.scan_count ?? 0);
  const discoveredRoleCount = Number(company.discovered_role_count ?? 0);
  const discoveryStatus = scanCount > 0 && discoveredRoleCount === 0
    ? '<span class="company-discovery-status">Discovered 0 potential roles</span>'
    : "";
  return `
    <details class="company-panel ${tierClass}" data-company-id="${company.id}">
      <summary class="company-summary">
        <span class="company-chevron">></span>
        <span class="company-summary-main">
          <span class="company-name">${escapeUiText(company.name)}</span>
          <span class="company-summary-meta">${careerPages.length} ${careerPages.length === 1 ? "link" : "links"}${updated ? ` | updated ${escapeUiText(updated)}` : ""}</span>
          ${discoveryStatus}
        </span>
      </summary>
      <div class="company-body">
        <div class="company-info">
          <label class="company-notes-field">
            <span>notes</span>
            <textarea data-company-notes="${company.id}" rows="3">${escapeHtml(company.notes ?? "")}</textarea>
          </label>
          <label>
            <span>tier</span>
            <select data-company-tier="${company.id}">
              ${renderCompanyTierOptions(company.prestige_tier)}
            </select>
          </label>
          <div>
            <span>browser wait</span>
            <strong>${Number(company.browser_extra_wait_ms ?? 0)}ms</strong>
          </div>
        </div>
        <div class="company-links">
          ${careerPages.length > 0 ? careerPages.map((page) => renderCompanyLink(page)).join("") : '<p class="company-empty-links">no career links yet.</p>'}
        </div>
        <section class="company-link-panel" aria-label="add career link">
          <form class="company-link-form" data-company-link-form="${company.id}">
            <input name="label" type="text" placeholder="label" aria-label="career link label" />
            <input name="url" type="url" placeholder="https://..." aria-label="career link url" required />
            <button class="company-link-add" type="submit" aria-label="add career link" title="add career link">
              ${renderPlusIcon()}
            </button>
          </form>
        </section>
        <div class="company-danger-row">
          <button class="company-delete-button" type="button" data-delete-company="${company.id}">
            ${renderTrashIcon()}
            <span>deactivate company</span>
          </button>
        </div>
      </div>
    </details>
  `;
}

function renderCompanyTierClass(currentTier) {
  const normalizedTier = String(currentTier ?? "");
  return ["0", "1", "2", "3", "4"].includes(normalizedTier)
    ? `company-tier-${normalizedTier}`
    : "company-tier-unset";
}

function renderCompanyTierOptions(currentTier) {
  const normalizedCurrent = String(currentTier ?? "");
  return ["", "0", "1", "2", "3", "4"]
    .map((value) => {
      const label = value ? `tier ${value}` : "not set";
      const selected = value === normalizedCurrent ? " selected" : "";
      return `<option value="${escapeHtml(value)}"${selected}>${escapeUiText(label)}</option>`;
    })
    .join("");
}

function renderCompanyLink(page) {
  const label = page.label ? escapeUiText(page.label) : "career page";
  const url = escapeHtml(page.url);
  return `
    <div class="company-link-row" data-career-page-id="${page.id}">
      <a class="company-link-url" href="${url}" target="_blank" rel="noreferrer">
        <span class="company-link-label">${label}</span>
        <span class="company-link-text">${escapeHtml(page.url)}</span>
      </a>
      <button class="company-link-delete" type="button" data-delete-career-page="${page.id}" aria-label="delete ${label} link" title="delete link">
        ${renderTrashIcon()}
      </button>
    </div>
  `;
}

async function openCompaniesView() {
  companiesView.hidden = false;
  document.body.classList.add("companies-open");
  companiesCloseButton.focus();
  if (companiesData) {
    renderCompanies(companiesData);
  } else {
    companiesStatus.textContent = "loading companies...";
    companiesStatus.classList.remove("is-empty");
    companiesList.innerHTML = "";
  }
  try {
    await loadCompanies();
  } catch {
    companiesStatus.textContent = "could not load companies.";
  }
}

function closeCompaniesView() {
  companiesView.hidden = true;
  document.body.classList.remove("companies-open");
  manageCompaniesButton.focus();
}

async function loadCompanies(message = "") {
  const response = await fetch("/api/companies");
  if (!response.ok) throw new Error("Companies request failed");
  renderCompanies(await response.json(), message);
}

async function loadRoleCompanyOptions() {
  const response = await fetch("/api/companies");
  if (!response.ok) throw new Error("Companies request failed");
  const payload = await response.json();
  renderRoleCompanyOptions(payload.companies);
}

async function createCompany(form) {
  const formData = new FormData(form);
  const payload = {
    name: String(formData.get("name") ?? ""),
    career_url: String(formData.get("career_url") ?? ""),
    notes: String(formData.get("notes") ?? ""),
  };
  companiesStatus.textContent = "adding company...";
  const response = await fetch("/api/companies", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("Company create failed");
  form.reset();
  renderCompanies(await response.json(), "company added.");
  loadTracker(getActiveSearchQuery()).catch(() => {});
}

async function addCompanyCareerPage(form) {
  const companyId = form.dataset.companyLinkForm;
  if (!companyId) return;
  const formData = new FormData(form);
  const payload = {
    label: String(formData.get("label") ?? ""),
    url: String(formData.get("url") ?? ""),
  };
  companiesStatus.textContent = "adding link...";
  const response = await fetch(`/api/companies/${encodeURIComponent(companyId)}/career-pages`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("Career page create failed");
  form.reset();
  renderCompanies(await response.json(), "link added.");
}

async function deleteCompanyCareerPage(careerPageId) {
  companiesStatus.textContent = "deleting link...";
  const response = await fetch(`/api/company-career-pages/${encodeURIComponent(careerPageId)}`, {
    method: "DELETE",
  });
  if (!response.ok) throw new Error("Career page delete failed");
  renderCompanies(await response.json(), "link deleted.");
}

async function deactivateCompany(companyId) {
  companiesStatus.textContent = "deactivating company...";
  const response = await fetch(`/api/companies/${encodeURIComponent(companyId)}`, {
    method: "DELETE",
  });
  if (!response.ok) throw new Error("Company deactivate failed");
  renderCompanies(await response.json(), "company deactivated.");
  loadTracker(getActiveSearchQuery()).catch(() => {});
}

function selectedRoleCompany() {
  const selectedName = roleCompanyInput.value.trim().toLocaleLowerCase();
  return roleCompanyData.find((company) => company.name.toLocaleLowerCase() === selectedName);
}

async function createRole(form) {
  const company = selectedRoleCompany();
  if (!company?.id) {
    roleAddStatus.textContent = "pick a saved company.";
    return;
  }
  const formData = new FormData(form);
  const payload = {
    company_id: company.id,
    role_url: String(formData.get("role_url") ?? ""),
  };
  roleAddStatus.textContent = "adding role...";
  const response = await fetch("/api/roles", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("Role create failed");
  const result = await response.json();
  if (result.tracker) {
    render(result.tracker);
  } else {
    await loadTracker(getActiveSearchQuery());
  }
  roleUrlInput.value = "";
  const roleTitle = result.role?.title ? formatUiText(result.role.title) : "role";
  roleAddStatus.textContent = result.scan_error
    ? `${roleTitle} added; scan could not finish.`
    : `${roleTitle} added.`;
}

function companyById(companyId) {
  const companies = Array.isArray(companiesData?.companies) ? companiesData.companies : [];
  return companies.find((company) => String(company.id) === String(companyId));
}

function setCompanySaveStatus(message) {
  companiesStatus.textContent = message;
  companiesStatus.classList.remove("is-empty");
}

function scheduleCompanyAutosave(companyId) {
  window.clearTimeout(companySaveTimers.get(companyId));
  companySaveTimers.set(
    companyId,
    window.setTimeout(() => {
      saveCompanyEdits(companyId).catch(() => {
        setCompanySaveStatus("could not save company.");
      });
    }, 700),
  );
}

async function saveCompanyEdits(companyId) {
  const panel = companiesList.querySelector(`[data-company-id="${CSS.escape(String(companyId))}"]`);
  if (!panel) return;
  const notesControl = panel.querySelector(`[data-company-notes="${CSS.escape(String(companyId))}"]`);
  const tierControl = panel.querySelector(`[data-company-tier="${CSS.escape(String(companyId))}"]`);
  const company = companyById(companyId);
  const payload = {
    notes: notesControl?.value ?? company?.notes ?? "",
    prestige_tier: tierControl?.value ?? company?.prestige_tier ?? "",
  };
  if (company) {
    company.notes = payload.notes;
    company.prestige_tier = payload.prestige_tier;
  }
  applyCompanyTierClass(panel, payload.prestige_tier);
  setCompanySaveStatus("saving company...");
  const response = await fetch(`/api/companies/${encodeURIComponent(companyId)}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("Company update failed");
  companiesData = await response.json();
  setCompanySaveStatus("company saved.");
  renderToolbarCompanyMeta(companyId);
}

function applyCompanyTierClass(panel, tier) {
  panel.classList.remove(
    "company-tier-unset",
    "company-tier-0",
    "company-tier-1",
    "company-tier-2",
    "company-tier-3",
    "company-tier-4",
  );
  panel.classList.add(renderCompanyTierClass(tier));
}

function renderToolbarCompanyMeta(companyId) {
  const panel = companiesList.querySelector(`[data-company-id="${CSS.escape(String(companyId))}"]`);
  const company = companyById(companyId);
  if (!panel || !company) return;
  const careerPages = Array.isArray(company.career_pages) ? company.career_pages : [];
  const updated = formatCompactDate(company.updated_at);
  const meta = panel.querySelector(".company-summary-meta");
  if (meta) {
    meta.textContent = `${careerPages.length} ${careerPages.length === 1 ? "link" : "links"}${updated ? ` | updated ${updated}` : ""}`;
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
  scanAllButton.textContent = "starting...";
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

async function cancelScanAll() {
  scanAllButton.disabled = true;
  scanAllButton.textContent = "cancelling...";
  try {
    const response = await fetch("/api/scan/cancel", { method: "POST" });
    if (response.status === 404) {
      scanAllButton.disabled = true;
      scanAllButton.textContent = "scan roles";
      scanStatusBar.hidden = true;
      scanStatusBar.classList.add("scan-error");
      scanStatusText.textContent = "restart server to enable scanning";
      return;
    }
    if (!response.ok && response.status !== 409) throw new Error("Scan cancel failed");
    renderScanStatus(await response.json());
    startScanStatusPolling();
  } catch {
    scanAllButton.disabled = false;
    scanAllButton.textContent = "cancel scan";
    scanStatusBar.hidden = false;
    scanStatusBar.classList.add("scan-error");
    scanStatusText.textContent = "could not cancel scan";
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

async function loadExperienceNotes() {
  const response = await fetch("/api/experience-notes");
  if (!response.ok) throw new Error("Experience notes request failed");
  const payload = await response.json();
  renderExperienceNotes(payload.experience_notes);
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
      if ([".pdf", ".docx"].some((suffix) => file.name.toLowerCase().endsWith(suffix))) {
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

async function uploadExperienceNotes(files) {
  const selectedFiles = Array.from(files ?? []);
  if (selectedFiles.length === 0) return;

  experienceNoteUploadButton.disabled = true;
  renderExperienceNotes(
    experienceNotes,
    `uploading ${selectedFiles.length} ${selectedFiles.length === 1 ? "note" : "notes"}...`,
  );
  try {
    for (const file of selectedFiles) {
      const suffix = file.name.toLowerCase();
      const payload = { filename: file.name };
      if (suffix.endsWith(".pdf") || suffix.endsWith(".docx")) {
        payload.content_base64 = await readFileAsBase64(file);
      } else {
        payload.content = await file.text();
      }
      const response = await fetch("/api/experience-notes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!response.ok) throw new Error("Experience note upload failed");
    }
    prepAnalysisByRoleId.clear();
    await loadApplicationMaterials();
  } catch {
    renderExperienceNotes(experienceNotes, "could not save every note.");
    updateMaterialsSummary();
  } finally {
    experienceNoteUpload.value = "";
    experienceNoteUploadButton.disabled = false;
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

experienceNoteUploadButton.addEventListener("click", () => {
  experienceNoteUpload.click();
});

experienceNoteUpload.addEventListener("change", () => {
  uploadExperienceNotes(experienceNoteUpload.files);
});


materialsToggle.addEventListener("click", () => {
  setMaterialsCollapsed(materialsToggle.getAttribute("aria-expanded") === "true");
});

async function openApplicationMaterialIndex(button) {
  button.disabled = true;
  const originalText = button.textContent;
  button.textContent = "opening...";
  try {
    const response = await fetch("/api/application-materials/index/open", {method: "POST"});
    if (!response.ok) throw new Error("Could not open the application material index.");
  } catch (error) {
    materialIndexWarning.hidden = false;
    materialIndexWarning.textContent =
      error instanceof Error ? error.message : "Could not open the application material index.";
  } finally {
    button.disabled = false;
    button.textContent = originalText;
  }
}

materialsBody.addEventListener("click", (event) => {
  const indexButton = event.target.closest("[data-open-material-index]");
  if (indexButton) {
    openApplicationMaterialIndex(indexButton);
    return;
  }
  const previewButton = event.target.closest("[data-material-view]");
  if (previewButton) {
    toggleMaterialPreview(previewButton);
    return;
  }
  const removeButton = event.target.closest("[data-material-remove]");
  if (removeButton) removeApplicationMaterial(removeButton);
});

scanAllButton.addEventListener("click", () => {
  if (scanStatusData?.scanning) {
    cancelScanAll();
    return;
  }
  startScanAll();
});

statusListEl.addEventListener("click", (event) => {
  const reviewAction = event.target.closest("[data-review-role-id]");
  if (reviewAction) {
    openReviewView(reviewAction.dataset.reviewRoleId);
    return;
  }

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

function mergeRoleIntoTrackerData(updatedRole) {
  if (!updatedRole || !trackerData) return null;
  let mergedRole = null;
  trackerData.statuses.forEach((status) => {
    const index = status.jobs.findIndex((job) => String(job.id) === String(updatedRole.id));
    if (index === -1) return;
    mergedRole = { ...status.jobs[index], ...updatedRole };
    status.jobs[index] = mergedRole;
  });
  updateReviewButton(trackerData.statuses);
  updatePrepButton(trackerData.statuses);
  return mergedRole;
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

function openReviewView(focusedRoleId = null) {
  const discoveredJobs = [...getDiscoveredJobs()];
  const focusedId = focusedRoleId == null ? null : String(focusedRoleId);
  if (focusedId) {
    const focusedIndex = discoveredJobs.findIndex((role) => String(role.id) === focusedId);
    if (focusedIndex > 0) {
      const [focusedRole] = discoveredJobs.splice(focusedIndex, 1);
      discoveredJobs.unshift(focusedRole);
    }
  }
  reviewQueue = discoveredJobs;
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
  const interestedJobs = [...getInterestedJobs()].sort(
    (left, right) => Number(Boolean(right.prep_started)) - Number(Boolean(left.prep_started)),
  );
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
  const decodedValue = decodeHtmlEntities(String(value)).replace(/\u00a0/g, " ");
  if (looksLikeHtmlDescription(decodedValue)) {
    return renderHtmlDescription(decodedValue);
  }

  const lines = decodedValue
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

    if (isKnownDescriptionHeading(line)) {
      flushList();
      blocks.push(`<h3>${escapeUiText(line.replace(/:$/, ""))}</h3>`);
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

function decodeHtmlEntities(value) {
  const textarea = document.createElement("textarea");
  textarea.innerHTML = value;
  return textarea.value;
}

function looksLikeHtmlDescription(value) {
  return /<\/?(?:a|br|div|em|h[1-6]|li|ol|p|span|strong|ul)\b/i.test(value);
}

function renderHtmlDescription(value) {
  const template = document.createElement("template");
  template.innerHTML = value;
  const blocks = [];
  renderDescriptionNodes(template.content.childNodes, blocks);
  return blocks.join("");
}

function renderDescriptionNodes(nodes, blocks) {
  nodes.forEach((node) => {
    if (node.nodeType === Node.TEXT_NODE) {
      const text = normalizeDescriptionText(node.textContent);
      if (text) blocks.push(`<p>${escapeUiText(text)}</p>`);
      return;
    }

    if (node.nodeType !== Node.ELEMENT_NODE) return;
    const element = node;
    const tagName = element.tagName.toLowerCase();
    if (tagName === "script" || tagName === "style") return;
    if (tagName === "br") return;

    if (/^h[1-6]$/.test(tagName)) {
      appendDescriptionHeading(blocks, element.textContent);
      return;
    }

    if (tagName === "ul" || tagName === "ol") {
      const list = renderDescriptionList(element);
      if (list) blocks.push(list);
      return;
    }

    if (tagName === "p") {
      renderDescriptionParagraph(element, blocks);
      return;
    }

    const hasBlockChildren = Array.from(element.children).some((child) =>
      ["DIV", "H1", "H2", "H3", "H4", "H5", "H6", "OL", "P", "UL"].includes(child.tagName),
    );
    if (["article", "div", "section"].includes(tagName) && hasBlockChildren) {
      renderDescriptionNodes(element.childNodes, blocks);
      return;
    }

    const childLists = Array.from(element.children).filter((child) =>
      ["UL", "OL"].includes(child.tagName),
    );
    const text = normalizeDescriptionText(textWithoutChildLists(element));
    if (text) {
      if (isDescriptionHeading(text, element)) {
        appendDescriptionHeading(blocks, text);
      } else {
        blocks.push(`<p>${escapeUiText(text)}</p>`);
      }
    }

    if (childLists.length > 0) {
      childLists.forEach((listElement) => {
        const list = renderDescriptionList(listElement);
        if (list) blocks.push(list);
      });
      return;
    }

    if (!text && hasBlockChildren) {
      renderDescriptionNodes(element.childNodes, blocks);
    }
  });
}

function renderDescriptionParagraph(element, blocks) {
  if (!element.querySelector("br")) {
    const text = normalizeDescriptionText(textWithoutChildLists(element));
    if (!text) return;
    if (isDescriptionHeading(text, element)) {
      appendDescriptionHeading(blocks, text);
    } else {
      blocks.push(`<p>${escapeUiText(text)}</p>`);
    }
    return;
  }

  let segment = "";
  const flushSegment = () => {
    const text = normalizeDescriptionText(segment);
    segment = "";
    if (!text) return;
    if (isDescriptionHeading(text, element)) {
      appendDescriptionHeading(blocks, text);
    } else {
      blocks.push(`<p>${escapeUiText(text)}</p>`);
    }
  };

  element.childNodes.forEach((child) => {
    if (child.nodeType === Node.ELEMENT_NODE && child.tagName.toLowerCase() === "br") {
      flushSegment();
      return;
    }
    segment += ` ${child.textContent ?? ""}`;
  });
  flushSegment();
}

function appendDescriptionHeading(blocks, value) {
  const text = normalizeDescriptionText(value).replace(/:$/, "");
  if (text) blocks.push(`<h3>${escapeUiText(text)}</h3>`);
}

function renderDescriptionList(listElement) {
  const items = Array.from(listElement.children)
    .filter((child) => child.tagName === "LI")
    .map((item) => {
      const text = normalizeDescriptionText(textWithoutChildLists(item));
      const nestedLists = Array.from(item.children)
        .filter((child) => ["UL", "OL"].includes(child.tagName))
        .map((childList) => renderDescriptionList(childList))
        .filter(Boolean)
        .join("");
      return text || nestedLists ? `<li>${escapeUiText(text)}${nestedLists}</li>` : "";
    })
    .filter(Boolean);
  return items.length > 0 ? `<ul>${items.join("")}</ul>` : "";
}

function textWithoutChildLists(element) {
  const clone = element.cloneNode(true);
  clone.querySelectorAll("ul, ol").forEach((list) => {
    list.remove();
  });
  return clone.textContent;
}

function normalizeDescriptionText(value) {
  return String(value ?? "").replace(/\s+/g, " ").trim();
}

function isDescriptionHeading(text, element) {
  const normalized = text.replace(/:$/, "").trim();
  if (!normalized || normalized.length > 90) return false;
  if (isKnownDescriptionHeading(normalized)) return true;
  if (/:$/.test(text)) return true;
  if (/[.!?]$/.test(normalized)) return false;
  if (normalized.split(/\s+/).length > 10) return false;
  if (element.querySelector("strong, b, u")) return true;
  return isKnownDescriptionHeading(normalized);
}

function isKnownDescriptionHeading(value) {
  return DESCRIPTION_SECTION_HEADING_PATTERN.test(String(value).trim());
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
      const updatedRole = await recordRoleReviewLater(current.id);
      reviewQueue.shift();
      mergeRoleIntoTrackerData(updatedRole);
      renderReviewRole("moved out of this review pass.");
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
    <section class="prep-role-hero" aria-label="role overview">
      <div class="review-title-row">
        <div class="prep-role-eyebrow">
          <p class="review-company">${escapeUiText(current.company_name)}</p>
          <span>application workspace</span>
        </div>
        ${renderRoleTitle(current.title, current.role_url, "review-role-title")}
      </div>
      <dl class="review-details review-primary-details">
        ${renderReviewDetail("location", current.location, false, "review-location-detail")}
        ${renderReviewDetail("last", formatCompactDate(current.last_seen_at))}
        ${renderReviewDetail("updated", formatCompactDate(current.updated_at))}
      </dl>
      <nav class="prep-workspace-nav" aria-label="prep sections">
        <button type="button" data-prep-section-target="prep-resume-${current.id}">
          <span>01</span> resume
        </button>
        <button type="button" data-prep-section-target="prep-cover-letter-${current.id}">
          <span>02</span> cover letter
        </button>
        <button type="button" data-prep-section-target="prep-description-${current.id}">
          <span>03</span> role details
        </button>
        <button type="button" data-prep-section-target="prep-chat-${current.id}">
          <span>04</span> role chat
        </button>
      </nav>
    </section>
    <div class="prep-workspace">
      ${renderPrepResume(current)}
      ${renderPrepCoverLetter(current)}
      ${renderPrepDescription(current.id, current.description)}
      ${renderPrepRoleChat(current)}
    </div>
  `;
  enhancePrepLatexEditors();

  loadPrepResume(current.id)
    .then((resume) => {
      if (!resume || prepQueue[0]?.id !== current.id) return;
      prepResumeByRoleId.set(current.id, resume);
      prepCard.querySelector(".prep-resume")?.replaceWith(
        htmlToElement(renderPrepResume(current, { resume })),
      );
      enhancePrepLatexEditors();
    })
    .catch(() => {});

  loadPrepCoverLetter(current.id)
    .then((coverLetter) => {
      if (!coverLetter || prepQueue[0]?.id !== current.id) return;
      prepCoverLetterByRoleId.set(current.id, coverLetter);
      prepCard.querySelector(".prep-cover-letter")?.replaceWith(
        htmlToElement(renderPrepCoverLetter(current, { coverLetter })),
      );
      enhancePrepLatexEditors();
    })
    .catch(() => {});
}

function renderPrepResume(role, state = {}) {
  const savedResume = prepResumeByRoleId.get(role.id);
  const resume = state.resume ?? savedResume;
  const tweaks = state.tweaks ?? prepResumeTweaksByRoleId.get(role.id) ?? "";
  const pdfUrl = `/api/roles/${encodeURIComponent(role.id)}/resume.pdf`;
  if (state.loading) {
    return `
      <details class="prep-panel prep-resume" id="prep-resume-${role.id}" open>
        <summary class="prep-analysis-header">
          <span class="prep-accordion-icon" aria-hidden="true"></span>
          <h3>resume</h3>
          <span>regenerating</span>
        </summary>
        <div class="prep-fit-loading" aria-label="regenerating resume">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <p>regenerating resume with tweaks...</p>
        </div>
      </details>
    `;
  }
  if (!resume) {
    return `
      <details class="prep-panel prep-resume" id="prep-resume-${role.id}" open>
        <summary class="prep-analysis-header">
          <span class="prep-accordion-icon" aria-hidden="true"></span>
          <h3>resume</h3>
          <span>loading</span>
        </summary>
        <div class="prep-fit-loading" aria-label="loading resume">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <p>loading role resume...</p>
        </div>
      </details>
    `;
  }
  return `
    <details class="prep-panel prep-resume" id="prep-resume-${role.id}" open>
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>resume</h3>
        <div class="prep-summary-actions">
          <span>${resume.pdf_base64 ? "preview ready" : "latex ready"}</span>
          ${
            resume.pdf_base64
              ? `<a class="prep-summary-action prep-cover-pdf-link" href="${escapeHtml(pdfUrl)}" target="_blank" rel="noreferrer">view</a>`
              : ""
          }
        </div>
      </summary>
      <p class="prep-overview">${escapeUiText(resume.summary ?? "Saved resume for this role.")}</p>
      ${renderPrepAnalysis(role)}
      <section class="prep-generation-controls" aria-label="resume refinement">
        <div class="prep-control-heading">
          <span>refine this version</span>
          <p>Describe a focused change, then regenerate without losing the saved source.</p>
        </div>
        <label class="prep-cover-tweaks prep-resume-tweaks">
          <span>tweak instructions</span>
          <textarea
            data-prep-resume-tweaks="${role.id}"
            rows="4"
            placeholder="paste or write a resume tweak prompt..."
          >${escapeHtml(tweaks)}</textarea>
        </label>
        <div class="prep-cover-actions">
          <button type="button" data-prep-resume-regenerate="${role.id}">
            regenerate with tweaks
          </button>
        </div>
      </section>
      <div class="prep-document-workspace">
        <label class="prep-cover-latex prep-document-source">
          <span>LaTeX source</span>
          <textarea
            data-prep-resume-latex="${role.id}"
            spellcheck="false"
          >${escapeHtml(resume.latex ?? "")}</textarea>
        </label>
        <section class="prep-document-preview" aria-label="resume preview">
          <div class="prep-preview-heading">
            <span>document preview</span>
            <p>Updates automatically after the source is saved.</p>
          </div>
          ${
            resume.pdf_base64
              ? `
                <iframe class="prep-cover-pdf" title="resume PDF preview" src="${escapeHtml(pdfUrl)}"></iframe>
              `
              : '<p class="prep-cover-path">PDF preview unavailable.</p>'
          }
        </section>
      </div>
    </details>
  `;
}

function renderPrepDescription(roleId, description) {
  return `
    <details class="prep-panel prep-description-panel" id="prep-description-${roleId}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>description</h3>
      </summary>
      ${renderReviewDescription(description)}
    </details>
  `;
}

function renderPrepRoleChat(role, state = {}) {
  const messages = state.messages ?? prepRoleChatByRoleId.get(role.id) ?? [];
  const loading = Boolean(state.loading);
  return `
    <details class="prep-panel prep-role-chat" id="prep-chat-${role.id}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>chat about this role</h3>
        <span>${messages.length ? `${messages.length} messages` : "ready"}</span>
      </summary>
      <div class="prep-role-chat-log" aria-live="polite">
        ${
          messages.length
            ? messages.map(renderPrepRoleChatMessage).join("")
            : '<p class="prep-role-chat-empty">ask about fit, risks, resume emphasis, or cover letter angle.</p>'
        }
        ${
          loading
            ? '<p class="prep-role-chat-loading">thinking...</p>'
            : ""
        }
      </div>
      <form class="prep-role-chat-form" data-prep-role-chat-form="${role.id}">
        <textarea
          data-prep-role-chat-input="${role.id}"
          rows="3"
          placeholder="ask about this role..."
        ></textarea>
        <button type="submit" ${loading ? "disabled" : ""}>send</button>
      </form>
    </details>
  `;
}

function renderPrepRoleChatMessage(message) {
  const role = message?.role === "assistant" ? "assistant" : "user";
  return `
    <article class="prep-role-chat-message prep-role-chat-message-${role}">
      <span>${role}</span>
      <p>${escapeUiText(message?.content ?? "")}</p>
    </article>
  `;
}

function renderPrepCoverLetter(role, state = {}) {
  const savedDraft = prepCoverLetterByRoleId.get(role.id);
  const draft = state.coverLetter ?? savedDraft;
  const tweaks = state.tweaks ?? draft?.tweaks ?? "";
  const pdfUrl = `/api/roles/${encodeURIComponent(role.id)}/cover-letter.pdf`;
  if (state.loading) {
    return `
      <details class="prep-panel prep-cover-letter" id="prep-cover-letter-${role.id}" open>
        <summary class="prep-analysis-header">
          <span class="prep-accordion-icon" aria-hidden="true"></span>
          <h3>cover letter</h3>
          <span>generating</span>
        </summary>
        <div class="prep-fit-loading" aria-label="generating cover letter">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <p>generating latex cover letter...</p>
        </div>
      </details>
    `;
  }
  return `
    <details class="prep-panel prep-cover-letter" id="prep-cover-letter-${role.id}" open>
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>cover letter</h3>
        <div class="prep-summary-actions">
          <span>${draft?.pdf_base64 ? "preview ready" : draft ? "latex ready" : "not generated"}</span>
          ${
            draft?.pdf_base64
              ? `<a class="prep-summary-action prep-cover-pdf-link" href="${escapeHtml(pdfUrl)}" target="_blank" rel="noreferrer">view</a>`
              : ""
          }
        </div>
      </summary>
      ${
        draft
          ? `<p class="prep-overview">${escapeUiText(draft.summary ?? "cover letter generated")}</p>`
          : '<p class="prep-overview">generate a LaTeX cover letter from the resume, posting, and stored examples.</p>'
      }
      <section class="prep-generation-controls" aria-label="cover letter generation">
        <div class="prep-control-heading">
          <span>${draft ? "refine this version" : "create a tailored draft"}</span>
          <p>Use the role, resume, and saved examples to shape the letter.</p>
        </div>
        ${
          draft
            ? `
              <label class="prep-cover-tweaks">
                <span>tweak instructions</span>
                <textarea
                  data-prep-cover-letter-tweaks="${role.id}"
                  rows="3"
                  placeholder="make it warmer, cut a paragraph, emphasize systems work..."
                >${escapeHtml(tweaks)}</textarea>
              </label>
            `
            : ""
        }
        <div class="prep-cover-actions">
          <button type="button" data-prep-cover-letter="${role.id}">
            ${draft ? "regenerate" : "generate cover letter"}
          </button>
        </div>
      </section>
      ${
        draft
          ? `
            <div class="prep-document-workspace">
              <label class="prep-cover-latex prep-document-source">
                <span>LaTeX source</span>
                <textarea
                  data-prep-cover-letter-latex="${role.id}"
                  spellcheck="false"
                >${escapeHtml(draft.latex ?? "")}</textarea>
              </label>
              <section class="prep-document-preview" aria-label="cover letter preview">
                <div class="prep-preview-heading">
                  <span>document preview</span>
                  <p>Updates automatically after the source is saved.</p>
                </div>
                ${
                  draft.pdf_base64
                    ? `
                      <iframe class="prep-cover-pdf" title="cover letter PDF preview" src="${escapeHtml(pdfUrl)}"></iframe>
                    `
                    : '<p class="prep-cover-path">PDF preview unavailable.</p>'
                }
              </section>
            </div>
          `
          : ""
      }
    </details>
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
              ${renderPrepTweakPrompt(item)}
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
                <button type="button" data-prep-feedback="accept" ${item.tweak_prompt ? "" : "disabled"}>
                  add tweak
                </button>
              </div>
            </div>
          `
          : '<p class="prep-overview">ready to apply with the current resume.</p>'
      }
    </section>
  `;
}

function renderPrepTweakPrompt(item) {
  if (!item?.tweak_prompt) {
    return `
      <div class="prep-proposed-edit">
        <p class="prep-proposed-label">feedback only</p>
        <p>not enough information to turn this into a safe resume tweak.</p>
      </div>
    `;
  }
  return `
    <div class="prep-proposed-edit">
      <p class="prep-proposed-label">tweak prompt</p>
      <p>${escapeUiText(item.tweak_prompt)}</p>
    </div>
  `;
}

async function loadPrepAnalysis(roleId, options = {}) {
  if (!options.force && prepAnalysisByRoleId.has(roleId)) {
    return prepAnalysisByRoleId.get(roleId);
  }
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

async function loadPrepResume(roleId, { force = false } = {}) {
  if (!force && prepResumeByRoleId.has(roleId)) return prepResumeByRoleId.get(roleId);
  const response = await fetch(`/api/roles/${encodeURIComponent(roleId)}/resume`);
  if (!response.ok) throw new Error("Resume request failed");
  const payload = await response.json();
  if (payload.resume) {
    prepResumeByRoleId.set(roleId, payload.resume);
  }
  return payload.resume;
}

async function savePrepResume(roleId, latex) {
  const response = await fetch(`/api/roles/${encodeURIComponent(roleId)}/resume/save`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ latex }),
  });
  if (!response.ok) throw new Error("Resume save failed");
  return response.json();
}

async function generatePrepResume(roleId, tweaks, previousLatex) {
  const response = await fetch(`/api/roles/${encodeURIComponent(roleId)}/resume`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tweaks, previous_latex: previousLatex }),
  });
  if (!response.ok) throw new Error("Resume generation failed");
  return response.json();
}

async function sendPrepRoleChat(roleId, messages) {
  const response = await fetch(`/api/roles/${encodeURIComponent(roleId)}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages }),
  });
  if (!response.ok) throw new Error("Role chat failed");
  return response.json();
}

function queuePrepResumeAutosave(roleId, latex, delay = COVER_LETTER_AUTOSAVE_DELAY_MS) {
  const state = prepResumeSaveStateByRoleId.get(roleId) ?? {
    timer: null,
    saving: false,
    version: 0,
    latex: "",
  };
  state.version += 1;
  state.latex = latex;
  if (state.timer) {
    clearTimeout(state.timer);
  }
  state.timer = setTimeout(() => {
    state.timer = null;
    void runPrepResumeAutosave(roleId);
  }, delay);
  prepResumeSaveStateByRoleId.set(roleId, state);
}

async function runPrepResumeAutosave(roleId) {
  const state = prepResumeSaveStateByRoleId.get(roleId);
  if (!state || state.saving) return;
  state.saving = true;
  const saveVersion = state.version;
  const latex = state.latex;
  try {
    const payload = await savePrepResume(roleId, latex);
    if (state.version === saveVersion) {
      prepResumeByRoleId.set(roleId, payload.resume);
      updatePrepPdfPreview("resume", roleId, payload.resume);
    }
  } catch {
    // Keep editing uninterrupted; a later edit or blur will retry.
  } finally {
    state.saving = false;
    if (state.version !== saveVersion) {
      queuePrepResumeAutosave(roleId, state.latex, 0);
    }
  }
}

function updatePrepPdfPreview(kind, roleId, payload) {
  if (!payload?.pdf_base64) return;
  const selector =
    kind === "resume"
      ? `[data-prep-resume-latex="${roleId}"]`
      : `[data-prep-cover-letter-latex="${roleId}"]`;
  const editor = prepCard.querySelector(selector);
  const panel = editor?.closest(".prep-panel");
  const iframe = panel?.querySelector(".prep-cover-pdf");
  const link = panel?.querySelector(".prep-cover-pdf-link");
  const pdfUrl =
    kind === "resume"
      ? `/api/roles/${encodeURIComponent(roleId)}/resume.pdf`
      : `/api/roles/${encodeURIComponent(roleId)}/cover-letter.pdf`;
  if (iframe) {
    iframe.src = `${pdfUrl}?v=${Date.now()}`;
  }
  if (link) {
    link.href = pdfUrl;
  }
}

async function generatePrepCoverLetter(roleId, tweaks = "", previousLatex = "") {
  const response = await fetch(`/api/roles/${encodeURIComponent(roleId)}/cover-letter`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tweaks, previous_latex: previousLatex }),
  });
  if (!response.ok) throw new Error("Cover letter generation failed");
  return response.json();
}

async function savePrepCoverLetter(roleId, latex) {
  const response = await fetch(`/api/roles/${encodeURIComponent(roleId)}/cover-letter/save`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ latex }),
  });
  if (!response.ok) throw new Error("Cover letter save failed");
  return response.json();
}

function queuePrepCoverLetterAutosave(roleId, latex, tweaks = "", delay = COVER_LETTER_AUTOSAVE_DELAY_MS) {
  const state = prepCoverLetterSaveStateByRoleId.get(roleId) ?? {
    timer: null,
    saving: false,
    version: 0,
    latex: "",
    tweaks: "",
  };
  state.version += 1;
  state.latex = latex;
  state.tweaks = tweaks;
  if (state.timer) {
    clearTimeout(state.timer);
  }
  state.timer = setTimeout(() => {
    state.timer = null;
    void runPrepCoverLetterAutosave(roleId);
  }, delay);
  prepCoverLetterSaveStateByRoleId.set(roleId, state);
}

async function runPrepCoverLetterAutosave(roleId) {
  const state = prepCoverLetterSaveStateByRoleId.get(roleId);
  if (!state || state.saving) return;
  state.saving = true;
  const saveVersion = state.version;
  const latex = state.latex;
  const tweaks = state.tweaks;
  try {
    const payload = await savePrepCoverLetter(roleId, latex);
    if (state.version === saveVersion) {
      prepCoverLetterByRoleId.set(roleId, { ...payload.cover_letter, tweaks });
      updatePrepPdfPreview("coverLetter", roleId, payload.cover_letter);
    }
  } catch {
    // Keep the editor uninterrupted; the next edit will retry autosave.
  } finally {
    state.saving = false;
    if (state.version !== saveVersion) {
      queuePrepCoverLetterAutosave(roleId, state.latex, state.tweaks, 0);
    }
  }
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
  const payload = await response.json();
  return payload.role;
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

function autoprepActionKey(prefix) {
  const suffix = globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random()}`;
  return `${prefix}-${suffix}`;
}

function setWorkspaceHash(hash) {
  if (window.location.hash === hash) return;
  window.history.pushState({}, "", hash || `${window.location.pathname}${window.location.search}`);
}

async function openPreppedView({seedJobs = null} = {}) {
  preppedView.hidden = false;
  document.body.classList.add("prepped-open");
  setWorkspaceHash("#prepped-roles");
  if (seedJobs) {
    preppedJobs = seedJobs;
    selectedPreppedRoleId = selectedPreppedRoleId ?? preppedJobs[0]?.role_id ?? null;
    renderPreppedRoles();
  } else if (preppedJobs.length === 0) {
    preppedSummary.textContent = "loading prepared roles...";
  }
  await refreshPreppedRoles();
  startPreppedPolling();
}

function closePreppedView({clearHash = true} = {}) {
  preppedView.hidden = true;
  document.body.classList.remove("prepped-open");
  stopPreppedPolling();
  openPreppedPreviews.clear();
  preppedPreviewBlobUrls.forEach((blobUrl) => URL.revokeObjectURL(blobUrl));
  preppedPreviewBlobUrls.clear();
  preppedPreviewVersions.clear();
  preppedPreviewErrors.clear();
  if (clearHash && window.location.hash === "#prepped-roles") setWorkspaceHash("");
}

window.addEventListener("pagehide", () => {
  document.querySelectorAll("[data-preview-blob-url]").forEach((preview) => {
    URL.revokeObjectURL(preview.dataset.previewBlobUrl);
  });
  preppedPreviewBlobUrls.forEach((blobUrl) => URL.revokeObjectURL(blobUrl));
  preppedPreviewBlobUrls.clear();
  preppedPreviewVersions.clear();
});

async function refreshPreppedRoles() {
  try {
    const response = await fetch("/api/autoprep/jobs");
    if (!response.ok) throw new Error("Prepped roles request failed");
    const payload = await response.json();
    preppedJobs = payload.jobs ?? [];
    const latestBulk = payload.bulk_cover_letter_regeneration;
    if (latestBulk) {
      const bulkJobs = Array.isArray(latestBulk.jobs) ? latestBulk.jobs : [];
      preppedBulkRegeneration = {
        idempotencyKey: latestBulk.idempotency_key,
        roleIds: bulkJobs.map((job) => Number(job.role_id)),
        jobs: bulkJobs,
        skipped: Array.isArray(latestBulk.skipped) ? latestBulk.skipped : [],
      };
    }
    if (!preppedJobs.some((job) => Number(job.role_id) === Number(selectedPreppedRoleId))) {
      selectedPreppedRoleId = preppedJobs[0]?.role_id ?? null;
    }
    renderPreppedRoles();
  } catch {
    preppedSummary.textContent = "could not refresh preparation progress.";
  }
}

function startPreppedPolling() {
  stopPreppedPolling();
  if (!preppedJobs.some(autoprepJobIsActive)) return;
  preppedPoll = window.setInterval(refreshPreppedRoles, 2000);
}

function stopPreppedPolling() {
  if (preppedPoll !== null) window.clearInterval(preppedPoll);
  preppedPoll = null;
}

function autoprepJobIsActive(job) {
  return ["queued", "generating_resume_tweaks", "regenerating_resume", "generating_cover_letter"].includes(job.overall_status);
}

function autoprepJobHasGenerationFailure(job) {
  return [job.resume_status, job.cover_letter_status].some(
    (status) => ["failed", "interrupted"].includes(status),
  );
}

function autoprepStatusLabel(status) {
  return ({
    queued: "Queued", generating_resume_tweaks: "Generating resume tweaks", regenerating_resume: "Regenerating resume",
    generating_cover_letter: "Generating cover letter", partially_complete: "Partially complete", ready: "Ready",
    failed: "Failed", interrupted: "Interrupted", generating_tweaks: "Generating tweaks", regenerating: "Regenerating",
    generating: "Generating",
  })[status] ?? formatUiText(status);
}

function preppedPreviewVersion(job, documentKind) {
  const fieldKind = documentKind === "cover-letter" ? "cover_letter" : "resume";
  return `${job.updated_at || ""}:${job[`${fieldKind}_artifact_path`] || ""}`;
}

function discardPreppedPreview(key, {close = false} = {}) {
  const blobUrl = preppedPreviewBlobUrls.get(key);
  if (blobUrl) URL.revokeObjectURL(blobUrl);
  preppedPreviewBlobUrls.delete(key);
  preppedPreviewVersions.delete(key);
  preppedPreviewErrors.delete(key);
  if (close) openPreppedPreviews.delete(key);
}

function discardStalePreppedPreviews() {
  preppedPreviewVersions.forEach((version, key) => {
    const [roleId, documentKind] = key.split(":");
    const job = preppedJobs.find((item) => Number(item.role_id) === Number(roleId));
    if (!job || preppedPreviewVersion(job, documentKind) !== version) {
      discardPreppedPreview(key, {close: true});
    }
  });
}

function updatePreppedBulkRegenerationMessage() {
  if (!preppedBulkRegeneration) return;
  const currentBulkJobs = preppedBulkRegeneration.jobs || preppedJobs;
  const jobsByRoleId = new Map(
    currentBulkJobs.map((job) => [Number(job.role_id), job]),
  );
  const trackedJobs = preppedBulkRegeneration.roleIds.map(
    (roleId) => jobsByRoleId.get(Number(roleId)),
  );
  const completedCount = trackedJobs.filter(
    (job) => job?.worker_state === "idle" && job.cover_letter_status === "ready",
  ).length;
  const failedJobs = trackedJobs.filter(
    (job) => !job || (
      job.worker_state === "idle"
      && ["failed", "interrupted"].includes(job.cover_letter_status)
    ),
  );
  const remainingCount = trackedJobs.length - completedCount - failedJobs.length;
  const skippedDetails = preppedBulkRegeneration.skipped.length
    ? ` Skipped before queueing: ${preppedBulkRegeneration.skipped
      .map((item) => `${item.company_name} — ${item.title}: ${item.reason}`)
      .join(" · ")}`
    : "";
  const failureDetails = failedJobs.length
    ? ` Queued regeneration failures: ${failedJobs.map((job) => (
      job
        ? `${job.company_name} — ${job.title}: ${job.cover_letter_error || "generation failed"}`
        : "A role left the Prepped queue before regeneration completed"
    )).join(" · ")}`
    : "";
  if (!trackedJobs.length) {
    preppedBulkMessage = `No cover letters were queued.${skippedDetails}`;
  } else if (remainingCount > 0) {
    preppedBulkMessage = `Cover-letter regeneration in progress: ${completedCount} of ${trackedJobs.length} complete · ${remainingCount} remaining.${skippedDetails}${failureDetails}`;
  } else {
    preppedBulkMessage = `Cover-letter regeneration complete: ${completedCount} succeeded, ${failedJobs.length} failed.${skippedDetails}${failureDetails}`;
  }
}

function renderPreppedRoles() {
  discardStalePreppedPreviews();
  updatePreppedBulkRegenerationMessage();
  const activeCount = preppedJobs.filter(autoprepJobIsActive).length;
  const regeneratableCount = preppedJobs.filter(
    (job) => job.worker_state === "idle" && job.cover_letter_status === "ready",
  ).length;
  preppedSummary.textContent = preppedJobs.length
    ? `${preppedJobs.length} prepped ${preppedJobs.length === 1 ? "role" : "roles"}${activeCount ? ` · ${activeCount} in progress` : ""}`
    : "No queued or prepared roles.";
  regenerateAllCoverLettersButton.disabled = (
    bulkCoverLetterRegenerationPending || regeneratableCount === 0
  );
  regenerateAllCoverLettersButton.setAttribute(
    "aria-busy",
    bulkCoverLetterRegenerationPending ? "true" : "false",
  );
  regenerateAllCoverLettersButton.textContent = bulkCoverLetterRegenerationPending
    ? "queuing cover letters..."
    : "regenerate all cover letters";
  preppedBulkStatus.textContent = preppedBulkMessage;
  preppedList.innerHTML = preppedJobs.map((job) => {
    const hasGenerationFailure = autoprepJobHasGenerationFailure(job);
    const activeClass = Number(job.role_id) === Number(selectedPreppedRoleId) ? " is-active" : "";
    return `
      <button type="button" class="prepped-list-item${hasGenerationFailure ? " has-generation-failure" : ""}${activeClass}" data-prepped-role="${job.role_id}">
        <strong>${escapeUiText(job.company_name)}</strong><span>${escapeUiText(job.title)}</span>
        <small class="status-${escapeHtml(job.overall_status)}">${escapeHtml(autoprepStatusLabel(job.overall_status))}</small>
      </button>`;
  }).join("");
  renderPreppedDetail();
  startPreppedPolling();
}

function renderPreppedDetail() {
  const currentIndex = preppedJobs.findIndex((job) => Number(job.role_id) === Number(selectedPreppedRoleId));
  const job = preppedJobs[currentIndex];
  if (!job) {
    preppedDetail.innerHTML = '<div class="prepped-empty"><h3>nothing prepped yet.</h3><p>Queue Interested roles from Autoprep Interested.</p></div>';
    return;
  }
  const jobTitle = escapeUiText(job.title);
  const safeRoleUrl = safeExternalHttpUrl(job.role_url);
  const roleLink = safeRoleUrl
    ? `<a class="prepped-role-link" href="${escapeHtml(safeRoleUrl)}" target="_blank" rel="noopener noreferrer">${jobTitle}<span aria-hidden="true">↗</span></a>`
    : jobTitle;
  const roleFacts = [
    ["Location", job.location || "Unavailable"],
    ["Added", formatCompactDate(job.date_added || job.created_at) || "Unavailable"],
    ["Last seen", formatCompactDate(job.last_seen_at) || "Unavailable"],
    ["Posting ID", job.posting_id || "Unavailable"],
  ];
  const movingToDisinterested = preppedStatusChangeRoleIds.has(Number(job.role_id));
  const disinterestedUnavailable = movingToDisinterested || autoprepJobIsActive(job);
  preppedDetail.innerHTML = `
    <header class="prepped-detail-heading">
      <div><p class="eyebrow">${escapeUiText(job.company_name)}</p><h3>${roleLink}</h3></div>
      <span class="prepped-status status-${escapeHtml(job.overall_status)}">${escapeHtml(autoprepStatusLabel(job.overall_status))}</span>
    </header>
    <dl class="prepped-role-facts">${roleFacts.map(([label, value]) => `<div><dt>${escapeHtml(label)}</dt><dd>${escapeUiText(value)}</dd></div>`).join("")}</dl>
    <details class="prepped-role-description">
      <summary>Job description</summary>
      <div class="prepped-description-copy">${escapeUiText(job.description || "No job description was saved.").replaceAll("\n", "<br>")}</div>
    </details>
    ${job.notes ? `<details class="prepped-role-description"><summary>Role notes</summary><div class="prepped-description-copy">${escapeUiText(job.notes).replaceAll("\n", "<br>")}</div></details>` : ""}
    <div class="prepped-document-grid">
      ${renderPreppedDocument(job, "resume", "Resume")}
      ${renderPreppedDocument(job, "cover-letter", "Cover letter")}
    </div>
    <div class="prepped-detail-actions">
      <button type="button" data-prepped-nav="previous" ${currentIndex <= 0 ? "disabled" : ""}>Previous</button>
      <button type="button" data-prepped-nav="next" ${currentIndex >= preppedJobs.length - 1 ? "disabled" : ""}>Next</button>
      <button type="button" data-autoprep-open-folder ${job.artifact_directory ? "" : "disabled"}>Open Documents Folder</button>
      <button class="prepped-disinterested" type="button" data-autoprep-disinterested aria-busy="${movingToDisinterested ? "true" : "false"}" ${disinterestedUnavailable ? "disabled" : ""} title="${autoprepJobIsActive(job) ? "Wait for preparation to finish before moving this role" : "Move this role out of Prepped"}">${movingToDisinterested ? "Moving to Disinterested..." : "Move to Disinterested"}</button>
      <button class="success" type="button" data-autoprep-applied ${job.overall_status === "ready" ? "" : "disabled"}>Applied</button>
    </div>
    <p class="prepped-safety-note">Autoprep prepares files only. It never submits an application.</p>`;
}

async function loadPreppedPdfPreview(job, documentKind) {
  const key = `${job.role_id}:${documentKind}`;
  const version = preppedPreviewVersion(job, documentKind);
  if (
    preppedPreviewVersions.get(key) === version
    || loadingPreppedPreviews.has(key)
  ) return;
  discardPreppedPreview(key);
  loadingPreppedPreviews.add(key);
  preppedPreviewErrors.delete(key);
  renderPreppedDetail();
  try {
    const url = `/api/autoprep/roles/${encodeURIComponent(job.role_id)}/documents/${documentKind}.pdf?v=${encodeURIComponent(job.updated_at || "")}`;
    const blobUrl = await fetchPdfBlobUrl(url);
    const currentJob = preppedJobs.find((item) => Number(item.role_id) === Number(job.role_id));
    if (
      !openPreppedPreviews.has(key)
      || !currentJob
      || preppedPreviewVersion(currentJob, documentKind) !== version
    ) {
      URL.revokeObjectURL(blobUrl);
      openPreppedPreviews.delete(key);
      return;
    }
    preppedPreviewBlobUrls.set(key, blobUrl);
    preppedPreviewVersions.set(key, version);
  } catch (error) {
    preppedPreviewErrors.set(
      key,
      error instanceof Error ? error.message : "PDF preview unavailable",
    );
  } finally {
    loadingPreppedPreviews.delete(key);
    if (Number(selectedPreppedRoleId) === Number(job.role_id)) renderPreppedDetail();
  }
}

function renderPreppedDocument(job, documentKind, label) {
  const fieldKind = documentKind === "cover-letter" ? "cover_letter" : "resume";
  const status = job[`${fieldKind}_status`];
  const artifactPath = job[`${fieldKind}_artifact_path`];
  const filename = artifactPath?.split("/").pop() ?? "Not available";
  const error = job[`${fieldKind}_error`];
  const instruction = job[`${fieldKind}_instruction`] || "";
  const key = `${job.role_id}:${documentKind}`;
  const comments = preppedCommentsByDocument.get(key) ?? instruction;
  const commentsLabel = documentKind === "cover-letter" ? "Optional comments for the next version" : "Comments for the next version";
  const commentsPlaceholder = documentKind === "cover-letter"
    ? "Optionally describe specific, truthful changes..."
    : "Describe specific, truthful changes...";
  const retryingFailedDocument = ["failed", "interrupted"].includes(status);
  const active = job.worker_state !== "idle" || ["queued", "generating", "generating_tweaks", "regenerating"].includes(status);
  const canRegenerate = !active
    && (status === "ready" || retryingFailedDocument)
    && (retryingFailedDocument || documentKind === "cover-letter" || String(comments).trim());
  const previewOpen = openPreppedPreviews.has(key);
  const previewUrl = `/api/autoprep/roles/${encodeURIComponent(job.role_id)}/documents/${documentKind}.pdf?v=${encodeURIComponent(job.updated_at || "")}`;
  const previewBlobUrl = preppedPreviewBlobUrls.get(key);
  const previewError = preppedPreviewErrors.get(key);
  const previewLoading = loadingPreppedPreviews.has(key);
  const viewLink = artifactPath
    ? `<a class="prep-cover-pdf-link" data-autoprep-view="${documentKind}" href="${escapeHtml(previewUrl)}" target="_blank" rel="noreferrer" aria-label="View ${escapeHtml(label.toLowerCase())} PDF in browser">View PDF</a>`
    : "";
  return `
    <section class="prepped-document${previewOpen ? " has-open-preview" : ""} status-${escapeHtml(status)}">
      <div class="prepped-document-heading"><h4>${escapeHtml(label)}</h4><span>${escapeHtml(autoprepStatusLabel(status))}</span></div>
      <p class="prepped-filename">${escapeHtml(filename)}</p>
      ${error ? `<p class="prepped-error">${escapeHtml(error)}</p>` : ""}
      <div class="prepped-document-actions">
        <button type="button" data-autoprep-preview="${documentKind}" ${artifactPath ? "" : "disabled"}>${previewOpen ? "Hide preview" : "Preview PDF"}</button>
        ${viewLink}
      </div>
      <div class="prepped-pdf-preview" data-autoprep-preview-panel="${documentKind}" ${previewOpen && artifactPath ? "" : "hidden"}>
        ${previewOpen && previewBlobUrl ? `<iframe title="${escapeHtml(label)} PDF preview" src="${escapeHtml(previewBlobUrl)}"></iframe>` : ""}
        ${previewOpen && previewLoading ? `<p>Loading PDF preview...</p>` : ""}
        ${previewOpen && previewError ? `<p class="prepped-error">${escapeUiText(previewError)}</p>` : ""}
      </div>
      <label class="prepped-comments-label" for="prepped-comments-${escapeHtml(key)}">${commentsLabel}</label>
      <textarea id="prepped-comments-${escapeHtml(key)}" data-autoprep-comments="${documentKind}" rows="4" placeholder="${commentsPlaceholder}" ${active ? "disabled" : ""}>${escapeUiText(comments)}</textarea>
      <button class="prepped-regenerate" type="button" data-autoprep-regenerate="${documentKind}" ${canRegenerate ? "" : "disabled"}>${active ? "Regenerating..." : `Regenerate ${escapeHtml(label)}`}</button>
    </section>`;
}

async function regenerateAutoprepDocument(job, documentKind, button) {
  if (button.disabled) return;
  const key = `${job.role_id}:${documentKind}`;
  const fieldKind = documentKind === "cover-letter" ? "cover_letter" : "resume";
  const status = job[`${fieldKind}_status`];
  const retryingFailedDocument = ["failed", "interrupted"].includes(status);
  const textarea = preppedDetail.querySelector(`[data-autoprep-comments="${documentKind}"]`);
  const comments = String(textarea?.value || preppedCommentsByDocument.get(key) || "").trim();
  if (!comments && documentKind !== "cover-letter" && !retryingFailedDocument) {
    textarea?.focus();
    return;
  }
  button.disabled = true;
  button.textContent = "Queuing regeneration...";
  try {
    const response = await fetch(
      `/api/autoprep/roles/${encodeURIComponent(job.role_id)}/${retryingFailedDocument ? "retry" : "regenerate"}/${documentKind}`,
      {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(retryingFailedDocument
          ? {idempotency_key: autoprepActionKey(`retry-${documentKind}`)}
          : {
              comments,
              idempotency_key: autoprepActionKey(`regenerate-${documentKind}`),
            }),
      },
    );
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "Regeneration request failed");
    preppedCommentsByDocument.delete(key);
    discardPreppedPreview(key, {close: true});
    const index = preppedJobs.findIndex((item) => Number(item.role_id) === Number(job.role_id));
    if (index >= 0) preppedJobs[index] = payload.job;
    renderPreppedRoles();
  } catch (error) {
    window.alert(error instanceof Error ? error.message : "Regeneration request failed");
    await refreshPreppedRoles();
  }
}

async function regenerateAllPreppedCoverLetters() {
  if (bulkCoverLetterRegenerationPending) return;
  bulkCoverLetterRegenerationPending = true;
  preppedBulkRegeneration = null;
  preppedBulkMessage = "Queuing eligible cover letters...";
  renderPreppedRoles();
  try {
    const response = await fetch("/api/autoprep/cover-letters/regenerate", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        idempotency_key: autoprepActionKey("regenerate-all-cover-letters"),
      }),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "Bulk regeneration request failed");
    const queuedCount = Number(payload.queued_count || 0);
    const skipped = Array.isArray(payload.skipped) ? payload.skipped : [];
    preppedBulkRegeneration = {
      roleIds: (payload.jobs || []).map((job) => Number(job.role_id)),
      jobs: payload.jobs || [],
      skipped,
    };
    if (!queuedCount && !skipped.length) {
      preppedBulkRegeneration = null;
      preppedBulkMessage = "No prepped roles are available to regenerate.";
    }
    (payload.jobs || []).forEach((updatedJob) => {
      const index = preppedJobs.findIndex(
        (job) => Number(job.role_id) === Number(updatedJob.role_id),
      );
      if (index >= 0) preppedJobs[index] = updatedJob;
      discardPreppedPreview(`${updatedJob.role_id}:cover-letter`, {close: true});
    });
    await refreshPreppedRoles();
    startPreppedPolling();
  } catch (error) {
    preppedBulkRegeneration = null;
    preppedBulkMessage = error instanceof Error
      ? error.message
      : "Bulk regeneration request failed";
  } finally {
    bulkCoverLetterRegenerationPending = false;
    renderPreppedRoles();
  }
}

async function markPreppedRoleDisinterested(roleId, button) {
  const numericRoleId = Number(roleId);
  if (preppedStatusChangeRoleIds.has(numericRoleId)) return;
  preppedStatusChangeRoleIds.add(numericRoleId);
  button.disabled = true;
  button.setAttribute("aria-busy", "true");
  button.textContent = "Moving to Disinterested...";
  const currentIndex = preppedJobs.findIndex(
    (job) => Number(job.role_id) === numericRoleId,
  );
  try {
    await updateRoleStatusById(roleId, "disinterested");
    discardPreppedPreview(`${roleId}:resume`, {close: true});
    discardPreppedPreview(`${roleId}:cover-letter`, {close: true});
    if (currentIndex >= 0) preppedJobs.splice(currentIndex, 1);
    selectedPreppedRoleId = preppedJobs[
      Math.min(currentIndex, preppedJobs.length - 1)
    ]?.role_id ?? null;
    preppedBulkMessage = "Role moved to Disinterested.";
    renderPreppedRoles();
    loadInitialTrackerData();
  } catch (error) {
    preppedBulkMessage = error instanceof Error
      ? error.message
      : "Could not move this role to Disinterested.";
    await refreshPreppedRoles();
  } finally {
    preppedStatusChangeRoleIds.delete(numericRoleId);
    if (preppedJobs.some((job) => Number(job.role_id) === numericRoleId)) {
      renderPreppedRoles();
    }
  }
}

async function markPreppedRoleApplied(roleId, button) {
  if (button.disabled) return;
  button.disabled = true;
  button.textContent = "Moving to Applied...";
  const currentIndex = preppedJobs.findIndex((job) => Number(job.role_id) === Number(roleId));
  try {
    const response = await fetch(`/api/autoprep/roles/${encodeURIComponent(roleId)}/applied`, {method: "POST"});
    if (!response.ok) throw new Error("Applied update failed");
    discardPreppedPreview(`${roleId}:resume`, {close: true});
    discardPreppedPreview(`${roleId}:cover-letter`, {close: true});
    preppedJobs.splice(currentIndex, 1);
    selectedPreppedRoleId = preppedJobs[Math.min(currentIndex, preppedJobs.length - 1)]?.role_id ?? null;
    renderPreppedRoles();
    loadInitialTrackerData();
  } catch { await refreshPreppedRoles(); }
}

reviewDiscoveredButton.addEventListener("click", openReviewView);

closeReviewButton.addEventListener("click", closeReviewView);

prepInterestedButton.addEventListener("click", openPrepView);

preppedRolesButton.addEventListener("click", () => openPreppedView());

closePreppedButton.addEventListener("click", closePreppedView);

regenerateAllCoverLettersButton.addEventListener("click", regenerateAllPreppedCoverLetters);

preppedList.addEventListener("click", (event) => {
  const roleButton = event.target.closest("[data-prepped-role]");
  if (!roleButton) return;
  selectedPreppedRoleId = Number(roleButton.dataset.preppedRole);
  renderPreppedRoles();
});

preppedDetail.addEventListener("input", (event) => {
  const comments = event.target.closest("[data-autoprep-comments]");
  if (!comments) return;
  const key = `${selectedPreppedRoleId}:${comments.dataset.autoprepComments}`;
  preppedCommentsByDocument.set(key, comments.value);
  const regenerateButton = preppedDetail.querySelector(
    `[data-autoprep-regenerate="${comments.dataset.autoprepComments}"]`,
  );
  const job = preppedJobs.find((item) => Number(item.role_id) === Number(selectedPreppedRoleId));
  const fieldKind = comments.dataset.autoprepComments === "cover-letter" ? "cover_letter" : "resume";
  const status = job?.[`${fieldKind}_status`];
  const retryingFailedDocument = ["failed", "interrupted"].includes(status);
  if (regenerateButton) {
    regenerateButton.disabled = job?.worker_state !== "idle"
      || !["ready", "failed", "interrupted"].includes(status)
      || (!retryingFailedDocument && comments.dataset.autoprepComments !== "cover-letter" && !comments.value.trim());
  }
});

preppedDetail.addEventListener("click", async (event) => {
  const job = preppedJobs.find((item) => Number(item.role_id) === Number(selectedPreppedRoleId));
  if (!job) return;
  const navButton = event.target.closest("[data-prepped-nav]");
  if (navButton) {
    const currentIndex = preppedJobs.indexOf(job);
    const offset = navButton.dataset.preppedNav === "next" ? 1 : -1;
    selectedPreppedRoleId = preppedJobs[currentIndex + offset]?.role_id ?? job.role_id;
    renderPreppedRoles();
    return;
  }
  const previewButton = event.target.closest("[data-autoprep-preview]");
  if (previewButton) {
    const documentKind = previewButton.dataset.autoprepPreview;
    const key = `${job.role_id}:${documentKind}`;
    if (openPreppedPreviews.has(key)) {
      openPreppedPreviews.delete(key);
      renderPreppedDetail();
    } else {
      openPreppedPreviews.add(key);
      renderPreppedDetail();
      loadPreppedPdfPreview(job, documentKind);
    }
    return;
  }
  const regenerateButton = event.target.closest("[data-autoprep-regenerate]");
  if (regenerateButton) {
    regenerateAutoprepDocument(job, regenerateButton.dataset.autoprepRegenerate, regenerateButton);
    return;
  }

  const folderButton = event.target.closest("[data-autoprep-open-folder]");
  if (folderButton && !folderButton.disabled) {
    folderButton.disabled = true;
    folderButton.textContent = "Opening...";
    try {
      const response = await fetch(`/api/autoprep/roles/${encodeURIComponent(job.role_id)}/open-folder`, {method: "POST"});
      if (!response.ok) throw new Error("Could not open the documents folder.");
      folderButton.textContent = "Opened in Finder";
      window.setTimeout(() => {
        if (!folderButton.isConnected) return;
        folderButton.textContent = "Open Documents Folder";
        folderButton.disabled = false;
      }, 1_500);
    } catch (error) {
      folderButton.textContent = error instanceof Error ? error.message : "Could not open folder";
      folderButton.disabled = false;
    }
    return;
  }
  const disinterestedButton = event.target.closest("[data-autoprep-disinterested]");
  if (disinterestedButton) {
    markPreppedRoleDisinterested(job.role_id, disinterestedButton);
    return;
  }
  const appliedButton = event.target.closest("[data-autoprep-applied]");
  if (appliedButton) markPreppedRoleApplied(job.role_id, appliedButton);
});

closePrepButton.addEventListener("click", closePrepView);

reviewView.addEventListener("click", (event) => {
  const button = event.target.closest("[data-review-action]");
  if (!button) return;
  handleReviewAction(button.dataset.reviewAction);
});

prepView.addEventListener("click", (event) => {
  if (event.target.closest(".prep-summary-action")) {
    event.stopPropagation();
  }
});

prepView.addEventListener("input", (event) => {
  const resumeTweaks = event.target.closest("[data-prep-resume-tweaks]");
  if (resumeTweaks) {
    const roleId = Number(resumeTweaks.dataset.prepResumeTweaks);
    if (Number.isFinite(roleId)) {
      prepResumeTweaksByRoleId.set(roleId, resumeTweaks.value);
    }
    return;
  }

  const resumeEditor = event.target.closest("[data-prep-resume-latex]");
  if (resumeEditor) {
    syncLatexEditorHighlight(resumeEditor);
    const roleId = Number(resumeEditor.dataset.prepResumeLatex);
    if (!Number.isFinite(roleId)) return;
    queuePrepResumeAutosave(roleId, resumeEditor.value);
    return;
  }

  const latexEditor = event.target.closest("[data-prep-cover-letter-latex]");
  if (!latexEditor) return;
  syncLatexEditorHighlight(latexEditor);
  const roleId = Number(latexEditor.dataset.prepCoverLetterLatex);
  if (!Number.isFinite(roleId)) return;
  const coverSection = latexEditor.closest(".prep-cover-letter");
  const tweaks =
    coverSection?.querySelector(`[data-prep-cover-letter-tweaks="${roleId}"]`)?.value ?? "";
  queuePrepCoverLetterAutosave(roleId, latexEditor.value, tweaks);
});

prepView.addEventListener(
  "scroll",
  (event) => {
    const latexEditor = event.target.closest(
      "[data-prep-resume-latex], [data-prep-cover-letter-latex]",
    );
    if (latexEditor) syncLatexEditorHighlight(latexEditor);
  },
  true,
);

prepView.addEventListener("focusout", (event) => {
  const resumeEditor = event.target.closest("[data-prep-resume-latex]");
  if (resumeEditor) {
    const roleId = Number(resumeEditor.dataset.prepResumeLatex);
    if (!Number.isFinite(roleId)) return;
    queuePrepResumeAutosave(roleId, resumeEditor.value, 0);
    return;
  }

  const latexEditor = event.target.closest("[data-prep-cover-letter-latex]");
  if (!latexEditor) return;
  const roleId = Number(latexEditor.dataset.prepCoverLetterLatex);
  if (!Number.isFinite(roleId)) return;
  const coverSection = latexEditor.closest(".prep-cover-letter");
  const tweaks =
    coverSection?.querySelector(`[data-prep-cover-letter-tweaks="${roleId}"]`)?.value ?? "";
  queuePrepCoverLetterAutosave(roleId, latexEditor.value, tweaks, 0);
});

prepView.addEventListener("submit", async (event) => {
  const form = event.target.closest("[data-prep-role-chat-form]");
  if (!form || !prepQueue[0]) return;
  event.preventDefault();
  const roleId = Number(form.dataset.prepRoleChatForm);
  if (!Number.isFinite(roleId)) return;
  const input = form.querySelector(`[data-prep-role-chat-input="${roleId}"]`);
  const content = input?.value?.trim() ?? "";
  if (!content) {
    input?.focus();
    return;
  }
  const currentMessages = prepRoleChatByRoleId.get(roleId) ?? [];
  const nextMessages = [...currentMessages, { role: "user", content }];
  prepRoleChatByRoleId.set(roleId, nextMessages);
  prepCard.querySelector(".prep-role-chat")?.replaceWith(
    htmlToElement(renderPrepRoleChat(prepQueue[0], { messages: nextMessages, loading: true })),
  );
  try {
    const payload = await sendPrepRoleChat(roleId, nextMessages);
    const updatedMessages = [...nextMessages, payload.message];
    prepRoleChatByRoleId.set(roleId, updatedMessages);
    prepCard.querySelector(".prep-role-chat")?.replaceWith(
      htmlToElement(renderPrepRoleChat(prepQueue[0], { messages: updatedMessages })),
    );
  } catch {
    const failedMessages = [
      ...nextMessages,
      { role: "assistant", content: "could not answer right now." },
    ];
    prepRoleChatByRoleId.set(roleId, failedMessages);
    prepCard.querySelector(".prep-role-chat")?.replaceWith(
      htmlToElement(renderPrepRoleChat(prepQueue[0], { messages: failedMessages })),
    );
  }
});

prepView.addEventListener("click", async (event) => {
  const sectionButton = event.target.closest("[data-prep-section-target]");
  if (sectionButton) {
    const targetId = sectionButton.dataset.prepSectionTarget;
    const targetPanel = targetId ? document.getElementById(targetId) : null;
    if (targetPanel instanceof HTMLDetailsElement) {
      targetPanel.open = true;
      targetPanel.scrollIntoView({ behavior: "smooth", block: "start" });
      const summary = targetPanel.querySelector("summary");
      summary?.setAttribute("tabindex", "-1");
      summary?.focus({ preventScroll: true });
    }
    return;
  }

  const analysisButton = event.target.closest("[data-prep-analysis]");
  if (analysisButton && prepQueue[0]) {
    const roleId = prepQueue[0].id;
    prepCard.querySelector(".prep-analysis")?.replaceWith(
      htmlToElement(renderPrepAnalysis(prepQueue[0], { loading: true })),
    );
    try {
      const analysis = await loadPrepAnalysis(roleId, { force: true });
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

  const resumeRegenerateButton = event.target.closest("[data-prep-resume-regenerate]");
  if (resumeRegenerateButton && prepQueue[0]) {
    const roleId = prepQueue[0].id;
    const resumeSection = prepCard.querySelector(".prep-resume");
    const tweaks =
      resumeSection?.querySelector(`[data-prep-resume-tweaks="${roleId}"]`)?.value ?? "";
    const previousLatex =
      resumeSection?.querySelector(`[data-prep-resume-latex="${roleId}"]`)?.value ?? "";
    if (!tweaks.trim()) {
      resumeSection?.querySelector(`[data-prep-resume-tweaks="${roleId}"]`)?.focus();
      return;
    }
    prepResumeTweaksByRoleId.set(roleId, tweaks);
    resumeSection?.replaceWith(htmlToElement(renderPrepResume(prepQueue[0], { loading: true })));
    try {
      const payload = await generatePrepResume(roleId, tweaks, previousLatex);
      prepResumeByRoleId.set(roleId, payload.resume);
      prepCard.querySelector(".prep-resume")?.replaceWith(
        htmlToElement(renderPrepResume(prepQueue[0], { resume: payload.resume })),
      );
      enhancePrepLatexEditors();
    } catch {
      prepCard.querySelector(".prep-resume")?.replaceWith(
        htmlToElement(
          renderPrepResume(prepQueue[0], {
            resume: prepResumeByRoleId.get(roleId),
            tweaks,
          }),
        ),
      );
      enhancePrepLatexEditors();
    }
    return;
  }

  const coverLetterButton = event.target.closest("[data-prep-cover-letter]");
  if (coverLetterButton && prepQueue[0]) {
    const roleId = prepQueue[0].id;
    const coverSection = prepCard.querySelector(".prep-cover-letter");
    const tweaks =
      coverSection?.querySelector(`[data-prep-cover-letter-tweaks="${roleId}"]`)?.value ?? "";
    const previousLatex =
      tweaks.trim()
        ? coverSection?.querySelector(`[data-prep-cover-letter-latex="${roleId}"]`)?.value ?? ""
        : "";
    coverSection?.replaceWith(htmlToElement(renderPrepCoverLetter(prepQueue[0], { loading: true })));
    try {
      const payload = await generatePrepCoverLetter(roleId, tweaks, previousLatex);
      prepCoverLetterByRoleId.set(roleId, payload.cover_letter);
      prepCard.querySelector(".prep-cover-letter")?.replaceWith(
        htmlToElement(renderPrepCoverLetter(prepQueue[0], { coverLetter: payload.cover_letter })),
      );
      enhancePrepLatexEditors();
    } catch {
      prepCard.querySelector(".prep-cover-letter")?.replaceWith(
        htmlToElement(
          renderPrepCoverLetter(prepQueue[0], {
            coverLetter: prepCoverLetterByRoleId.get(roleId),
            tweaks,
          }),
        ),
      );
      enhancePrepLatexEditors();
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
    feedbackButton.textContent = responseAction === "accept" ? "adding..." : "ignoring...";
    try {
      if (responseAction === "accept") {
        const payload = await acceptPrepFeedback(roleId, currentIndex, feedbackItem, comment);
        const currentJobEl = document.querySelector(`.job[data-role-id="${CSS.escape(String(roleId))}"]`);
        if (payload.role) {
          prepQueue[0] = payload.role;
          applyRoleStatusUpdate(payload.role, currentJobEl);
        }
        appendPrepResumeTweak(roleId, payload.tweak_prompt ?? feedbackItem.tweak_prompt ?? "");
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

function appendPrepResumeTweak(roleId, tweakPrompt) {
  const prompt = String(tweakPrompt || "").trim();
  if (!prompt) return;
  const existing = prepResumeTweaksByRoleId.get(roleId)?.trim() ?? "";
  const next = existing ? `${existing}\n\n${prompt}` : prompt;
  prepResumeTweaksByRoleId.set(roleId, next);
  const tweaksBox = prepCard.querySelector(`[data-prep-resume-tweaks="${roleId}"]`);
  if (tweaksBox) {
    tweaksBox.value = next;
    tweaksBox.focus();
  }
}

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !scanFailuresDialog.hidden) closeScanFailuresDialog();
  if (event.key === "Escape" && !searchDialog.hidden) closeSearchDialog();
  if (event.key === "Escape" && !reviewView.hidden) closeReviewView();
  if (event.key === "Escape" && !prepView.hidden) closePrepView();
  if (event.key === "Escape" && !preppedView.hidden) closePreppedView();
  if (event.key === "Escape" && !settingsView.hidden) closeSettingsView();
  if (event.key === "Escape" && !metricsView.hidden) closeMetricsView();
  if (event.key === "Escape" && !sankeyView.hidden) closeSankeyView();
  if (event.key === "Escape" && !companiesView.hidden) closeCompaniesView();
});

scanFailuresOpenButton.addEventListener("click", openScanFailuresDialog);

scanFailuresCloseButton.addEventListener("click", closeScanFailuresDialog);

scanFailuresBackdrop.addEventListener("click", closeScanFailuresDialog);

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

metricsOpenButton.addEventListener("click", openMetricsView);

metricsCloseButton.addEventListener("click", closeMetricsView);

sankeyOpenButton.addEventListener("click", openSankeyView);

sankeyCloseButton.addEventListener("click", closeSankeyView);

manageCompaniesButton.addEventListener("click", openCompaniesView);

companiesCloseButton.addEventListener("click", closeCompaniesView);

companyCreateForm.addEventListener("submit", (event) => {
  event.preventDefault();
  createCompany(companyCreateForm).catch(() => {
    companiesStatus.textContent = "could not add company.";
  });
});

roleAddForm.addEventListener("submit", (event) => {
  event.preventDefault();
  createRole(roleAddForm).catch(() => {
    roleAddStatus.textContent = "could not add role.";
  });
});

companiesList.addEventListener("submit", (event) => {
  const form = event.target.closest("[data-company-link-form]");
  if (!form) return;
  event.preventDefault();
  addCompanyCareerPage(form).catch(() => {
    companiesStatus.textContent = "could not add link.";
  });
});

companiesList.addEventListener("input", (event) => {
  const notesControl = event.target.closest("[data-company-notes]");
  if (!notesControl) return;
  scheduleCompanyAutosave(notesControl.dataset.companyNotes);
});

companiesList.addEventListener("change", (event) => {
  const tierControl = event.target.closest("[data-company-tier]");
  if (!tierControl) return;
  const panel = tierControl.closest(".company-panel");
  if (panel) applyCompanyTierClass(panel, tierControl.value);
  window.clearTimeout(companySaveTimers.get(tierControl.dataset.companyTier));
  saveCompanyEdits(tierControl.dataset.companyTier).catch(() => {
    setCompanySaveStatus("could not save company.");
  });
});

companiesList.addEventListener("click", (event) => {
  const companyDeleteButton = event.target.closest("[data-delete-company]");
  if (companyDeleteButton) {
    const company = companyById(companyDeleteButton.dataset.deleteCompany);
    const name = company?.name ? formatUiText(company.name) : "this company";
    const confirmed = window.confirm(
      `Deactivate ${name}? It will be hidden from company counts and skipped during scans.`,
    );
    if (!confirmed) return;
    companyDeleteButton.disabled = true;
    deactivateCompany(companyDeleteButton.dataset.deleteCompany).catch(() => {
      companiesStatus.textContent = "could not deactivate company.";
      companyDeleteButton.disabled = false;
    });
    return;
  }
  const deleteButton = event.target.closest("[data-delete-career-page]");
  if (!deleteButton) return;
  const linkRow = deleteButton.closest(".company-link-row");
  const linkText = linkRow?.querySelector(".company-link-text")?.textContent?.trim();
  const confirmed = window.confirm(`Delete ${linkText || "this career link"}?`);
  if (!confirmed) return;
  deleteButton.disabled = true;
  deleteCompanyCareerPage(deleteButton.dataset.deleteCareerPage).catch(() => {
    companiesStatus.textContent = "could not delete link.";
    deleteButton.disabled = false;
  });
});

settingsForm.addEventListener("change", (event) => {
  const control = event.target.closest(
    'input[type="checkbox"], select, input[data-setting-text], textarea[data-setting-textarea]',
  );
  if (!control) return;
  saveSetting(control);
});

settingsForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const submitButton = settingsForm.querySelector('button[type="submit"]');
  const controls = settingsForm.querySelectorAll(
    'input[type="checkbox"][name], select[name], input[data-setting-text][name], textarea[data-setting-textarea][name]',
  );
  const payload = {};
  controls.forEach((control) => {
    const key = control.name;
    if (!key) return;
    payload[key] = control.type === "checkbox" ? control.checked : control.value;
  });

  submitButton.disabled = true;
  submitButton.textContent = "saving...";
  try {
    settingsStatus.textContent = "saving settings...";
    const response = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) throw new Error("Config update failed");
    renderSettings(await response.json(), "settings saved.");
  } catch (error) {
    settingsStatus.textContent = "could not save settings.";
    settingsStatus.classList.remove("is-empty");
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "save settings";
  }
});

centralApiUrlInput.addEventListener("input", () => {
  centralSyncButton.disabled = !centralApiUrlInput.value.trim();
});

centralSaveButton.addEventListener("click", saveCentralSettings);

centralSyncButton.addEventListener("click", syncCentralCompanies);

clearRecommendationHistoryButton.addEventListener("click", clearRecommendationHistory);

appUpdateButton.addEventListener("click", updateApp);

function syncWorkspaceRoute() {
  if (window.location.hash === "#prepped-roles") {
    openPreppedView();
    return;
  }
  closePreppedView({clearHash: false});
}

window.addEventListener("popstate", syncWorkspaceRoute);

loadInitialTrackerData();

if (window.location.hash === "#prepped-roles") {
  syncWorkspaceRoute();
}

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
