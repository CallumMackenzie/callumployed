from pathlib import Path

from callumployed.services.material_index import (
    build_material_index,
    get_material_index_status,
    retrieve_indexed_materials,
    split_experience_note,
)


def _note(*, note_id: int = 1, filename: str = "history.md", content: str) -> dict[str, object]:
    return {
        "id": note_id,
        "filename": filename,
        "content": content,
        "content_sha256": f"sha-{note_id}-{len(content)}",
        "updated_at": "2026-08-28T10:00:00",
    }


def test_split_experience_note_creates_markdown_pages_from_sections() -> None:
    sections = split_experience_note(
        _note(
            content="""# Employment
## Platform Engineer
Built Kubernetes deployment tooling with Python and PostgreSQL.
Reduced deployment time by 45% and mentored two engineers.

# Projects
## Computer Vision Lab
Trained PyTorch image classifiers and evaluated model accuracy.
"""
        )
    )

    assert [section.title for section in sections] == [
        "Employment",
        "Platform Engineer",
        "Projects",
        "Computer Vision Lab",
    ]
    assert "Kubernetes deployment tooling" in sections[1].content
    assert sections[1].tools == ("Kubernetes", "PostgreSQL", "Python")
    assert "leadership" in sections[1].attributes
    assert "performance" in sections[1].attributes


def test_build_material_index_writes_index_and_tracks_freshness(tmp_path: Path) -> None:
    root = tmp_path / "application-material-index"
    notes = [
        _note(
            content="""# Projects
## Scheduler
Built a Kubernetes scheduler in Go and measured a 30% latency reduction.
"""
        ),
        _note(
            note_id=2,
            filename="broken-upload.pdf",
            content="%PDF-1.7\x00\ufffd\ufffd binary stream",
        ),
    ]

    result = build_material_index(notes, root=root)

    assert result["status"] == "ready"
    assert result["document_count"] == 2
    assert result["source_count"] == 2
    assert result["indexed_source_count"] == 1
    assert result["skipped_source_count"] == 1
    assert result["needs_index"] is False
    assert (root / "index.md").is_file()
    assert "## Scheduler" in (root / "index.md").read_text()
    section_files = sorted((root / "sections").glob("*.md"))
    assert len(section_files) == 2
    assert get_material_index_status(notes, root=root)["status"] == "ready"

    changed_notes = [
        _note(content="# Projects\n## Scheduler\nAdded a Rust service after indexing.")
    ]
    stale = get_material_index_status(changed_notes, root=root)
    assert stale["status"] == "stale"
    assert stale["needs_index"] is True


def test_retrieve_indexed_materials_uses_index_to_load_only_relevant_pages(
    tmp_path: Path,
) -> None:
    root = tmp_path / "application-material-index"
    notes = [
        _note(
            content="""# Employment
## Platform Engineer
Built Kubernetes controllers in Go and Python. Operated PostgreSQL services.

## Community Coordinator
Organized public events, newsletters, and volunteer outreach.

# Projects
## Vision Pipeline
Built PyTorch computer-vision training and evaluation pipelines.
"""
        )
    ]
    build_material_index(notes, root=root)

    matches = retrieve_indexed_materials(
        notes,
        root=root,
        query="backend platform engineer building Kubernetes services with Python",
        limit=2,
        total_content_limit=2_000,
    )

    assert matches
    assert matches[0]["title"] == "Platform Engineer"
    assert "Kubernetes controllers" in str(matches[0]["content"])
    assert all("Community Coordinator" not in str(item["content"]) for item in matches)
    assert sum(len(str(item["content"])) for item in matches) <= 2_000


def test_rebuild_atomically_removes_pages_for_deleted_sources(tmp_path: Path) -> None:
    root = tmp_path / "application-material-index"
    first_notes = [
        _note(content="# Projects\n## First Project\nBuilt with Python."),
        _note(note_id=2, filename="older.md", content="# Employment\n## Old Role\nUsed Java."),
    ]
    build_material_index(first_notes, root=root)
    assert len(list((root / "sections").glob("*.md"))) == 4

    build_material_index(first_notes[:1], root=root)

    assert len(list((root / "sections").glob("*.md"))) == 2
    assert "Old Role" not in (root / "index.md").read_text()
