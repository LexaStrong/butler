from pathlib import Path

from butler import tools


def test_list_directory_lists_entries(tmp_path: Path):
    (tmp_path / "a.txt").write_text("hi")
    (tmp_path / "sub").mkdir()
    names = {e["name"] for e in tools.list_directory(str(tmp_path))["entries"]}
    assert names == {"a.txt", "sub"}


def test_list_directory_rejects_file(tmp_path: Path):
    f = tmp_path / "a.txt"
    f.write_text("x")
    assert "error" in tools.list_directory(str(f))


def test_read_text_file_truncates(tmp_path: Path):
    big = tmp_path / "big.txt"
    big.write_bytes(b"x" * (tools.MAX_READ_BYTES + 10))
    result = tools.read_text_file(str(big))
    assert result["truncated"] is True
    assert len(result["text"]) == tools.MAX_READ_BYTES


def test_create_folder_refuses_existing(tmp_path: Path):
    target = tmp_path / "new"
    assert "created" in tools.create_folder(str(target))
    assert "error" in tools.create_folder(str(target))


def test_open_app_rejects_unlisted_name():
    assert "error" in tools.open_app("cmd")


def test_every_schema_has_implementation():
    for schema in tools.TOOL_SCHEMAS:
        assert schema["function"]["name"] in tools.IMPLEMENTATIONS
