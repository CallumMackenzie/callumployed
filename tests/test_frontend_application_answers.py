from pathlib import Path

REPOSITORY_ROOT = Path(__file__).parents[1]
STATIC_DIRECTORY = REPOSITORY_ROOT / "src" / "callumployed" / "web" / "static"
FRONTEND_SOURCE = STATIC_DIRECTORY / "app.js"


def test_application_generation_has_no_external_runtime_harness_ui() -> None:
    source = FRONTEND_SOURCE.read_text()
    styles = (STATIC_DIRECTORY / "app.css").read_text()

    assert "application_generation_backend" not in source
    assert "renderApplicationRuntimeAvailability" not in source
    assert "data-application-runtime" not in source
    assert "/api/application-generation/backends/" not in source
    assert "setting-select-application-backend" not in source
    assert ".setting-select-application-backend" not in styles
    assert ".application-runtime-status" not in styles
    assert not (REPOSITORY_ROOT / "src/callumployed/services/hermes_generation.py").exists()


def test_prepped_application_questions_workspace_is_persistent_and_safe() -> None:
    source = FRONTEND_SOURCE.read_text()

    endpoint = "/api/autoprep/roles/${encodeURIComponent(roleId)}/application-answers"
    assert source.count(endpoint) >= 2
    assert 'class="application-questions-workspace"' in source
    assert "normalizeApplicationAnswerRecords" in source
    assert "preppedApplicationQuestionDrafts" in source
    assert "pendingApplicationAnswerRoleIds" in source
    assert 'record?.status === "completed" && record?.answer' in source
    assert "${savedCount} saved" in source
    assert "${records.length} saved" not in source
    assert "data-application-question-draft" in source
    assert "data-application-question-submit" in source
    assert "data-application-answer-copy" in source
    assert "data-application-answer-regenerate" in source
    assert "data-application-answer-delete" in source
    assert "Confirm delete" in source
    assert 'method: "DELETE"' in source
    assert "/regenerate`" in source
    assert 'document.execCommand("copy")' in source
    assert "escapeHtml(record.question" in source
    assert "escapeHtml(record.answer" in source
    assert "${escapeHtml(draft)}</textarea>" in source
    assert "${escapeUiText(draft)}</textarea>" not in source
    assert "escapeUiText(record.error" in source
    assert 'method: "POST"' in source
    submitter = source[
        source.index("async function submitApplicationQuestion") : source.index(
            "async function regenerateAutoprepDocument"
        )
    ]
    assert "updateRoleStatusById" not in submitter


def test_application_questions_styles_and_cache_keys_are_versioned() -> None:
    styles = (STATIC_DIRECTORY / "app.css").read_text()
    index = (STATIC_DIRECTORY / "index.html").read_text()

    assert ".application-questions-workspace" in styles
    assert ".application-answer-record" in styles
    assert ".application-question-composer" in styles
    assert ".application-question-composer textarea" in styles
    assert ".application-question-submit" in styles
    assert "padding-top: 20px" in styles
    assert "#close-prepped" in styles
    assert "text-transform: none" in styles
    assert '<link rel="stylesheet" href="/assets/app.css?v=vanilla-20260903-6" />' in index
    assert '<script type="module" src="/assets/app.js?v=vanilla-20260903-6"></script>' in index


def test_currently_applying_folder_ui_is_explained_and_selection_driven() -> None:
    source = FRONTEND_SOURCE.read_text()
    styles = (STATIC_DIRECTORY / "app.css").read_text()
    index = (STATIC_DIRECTORY / "index.html").read_text()

    assert 'class="currently-applying-guide"' in source
    assert "Currently Applying folder" in source
    assert "The original files stay in the role's documents folder." in source
    assert "data-currently-applying-open" in source
    assert "Open Currently Applying Folder" in source
    assert "queueCurrentlyApplyingSync" in source
    assert "selectPreppedRole" in source
    assert "/currently-applying" in source
    assert "/currently-applying/open" in source
    assert ".currently-applying-guide" in styles
    assert '<link rel="stylesheet" href="/assets/app.css?v=vanilla-20260903-6" />' in index
    assert '<script type="module" src="/assets/app.js?v=vanilla-20260903-6"></script>' in index


def test_every_prepped_role_transition_refreshes_currently_applying_folder() -> None:
    source = FRONTEND_SOURCE.read_text()

    disinterested_transition = source[
        source.index("async function markPreppedRoleDisinterested") : source.index(
            "async function markPreppedRoleApplied"
        )
    ]
    applied_transition = source[
        source.index("async function markPreppedRoleApplied") : source.index(
            'reviewDiscoveredButton.addEventListener("click"'
        )
    ]
    navigation_transition = source[
        source.index('const navButton = event.target.closest("[data-prepped-nav]")') :
        source.index('const currentlyApplyingButton = event.target.closest')
    ]

    assert "selectPreppedRole(" in disinterested_transition
    assert "selectPreppedRole(" in applied_transition
    assert "selectPreppedRole(" in navigation_transition


def test_frontend_uses_direct_vanilla_assets_without_framework_shell() -> None:
    index = (STATIC_DIRECTORY / "index.html").read_text()
    source = FRONTEND_SOURCE.read_text()

    assert not (REPOSITORY_ROOT / "frontend").exists()
    assert not (STATIC_DIRECTORY / "build").exists()
    assert not (STATIC_DIRECTORY / "shell.html").exists()
    assert '<script type="module" src="/assets/app.js?v=vanilla-20260903-6"></script>' in index
    assert '<div id="root"></div>' not in index
    assert "dangerouslySetInnerHTML" not in index
    assert "dangerouslySetInnerHTML" not in source
    assert "from \"./d3-sankey.js\"" in source
