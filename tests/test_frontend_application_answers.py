from pathlib import Path

REPOSITORY_ROOT = Path(__file__).parents[1]
STATIC_DIRECTORY = REPOSITORY_ROOT / "src" / "callumployed" / "web" / "static"
FRONTEND_SOURCE = STATIC_DIRECTORY / "app.js"


def test_application_backend_settings_render_availability_defensively() -> None:
    source = FRONTEND_SOURCE.read_text()
    styles = (STATIC_DIRECTORY / "app.css").read_text()

    assert 'setting.key === "application_generation_backend"' in source
    assert "renderApplicationRuntimeAvailability" in source
    assert 'data-application-runtime="${escapeHtml(runtimeName)}"' in source
    assert "option.available === false" in source
    assert "option.disabled === true" in source
    assert "runtime?.reason" in source
    renderer = source[
        source.index("function renderApplicationRuntimeAvailability") : source.index(
            "function renderSettingOption"
        )
    ]
    assert "data-application-runtime-test" in renderer
    assert "/api/application-generation/backends/" in source
    assert "setting-select-application-backend" in source
    assert ".setting-select-application-backend" in styles
    assert "width: 280px" in styles
    assert 'unavailable ? " — unavailable" : ""' in source


def test_prepped_application_questions_workspace_is_persistent_and_safe() -> None:
    source = FRONTEND_SOURCE.read_text()

    endpoint = "/api/autoprep/roles/${encodeURIComponent(roleId)}/application-answers"
    assert source.count(endpoint) >= 2
    assert 'class="application-questions-workspace"' in source
    assert "normalizeApplicationAnswerRecords" in source
    assert "preppedApplicationQuestionDrafts" in source
    assert "pendingApplicationAnswerRoleIds" in source
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
    assert index.count("vanilla-20260831-1") == 2


def test_frontend_uses_direct_vanilla_assets_without_framework_shell() -> None:
    index = (STATIC_DIRECTORY / "index.html").read_text()
    source = FRONTEND_SOURCE.read_text()

    assert not (REPOSITORY_ROOT / "frontend").exists()
    assert not (STATIC_DIRECTORY / "build").exists()
    assert not (STATIC_DIRECTORY / "shell.html").exists()
    assert '<script type="module" src="/assets/app.js?v=vanilla-20260831-1"></script>' in index
    assert '<div id="root"></div>' not in index
    assert "dangerouslySetInnerHTML" not in index
    assert "dangerouslySetInnerHTML" not in source
    assert "from \"./d3-sankey.js\"" in source
