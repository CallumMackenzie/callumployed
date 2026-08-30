from pathlib import Path

REPOSITORY_ROOT = Path(__file__).parents[1]
FRONTEND_SOURCE = REPOSITORY_ROOT / "frontend" / "src" / "legacy.ts"
STATIC_DIRECTORY = REPOSITORY_ROOT / "src" / "callumployed" / "web" / "static"


def test_application_backend_settings_render_availability_defensively() -> None:
    source = FRONTEND_SOURCE.read_text()

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
    assert 'document.execCommand("copy")' in source
    assert "escapeUiText(record.question" in source
    assert "escapeUiText(record.answer" in source
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
    assert "react-ts-20260829-17" in index
    assert "react-ts-20260829-23" in index
