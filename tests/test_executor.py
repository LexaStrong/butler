from butler import executor


def deny_all(name, decision, args):
    return False


def approve_all(name, decision, args):
    return True


def test_unknown_tool_never_runs():
    assert "error" in executor.run_tool("rm_rf", {}, approve_all)


def test_forbidden_tool_never_runs_even_if_approved():
    assert "error" in executor.run_tool("format_drive", {"drive": "D:"}, approve_all)


def test_protected_path_blocked_before_confirmation():
    asked = []

    def spy(name, decision, args):
        asked.append(name)
        return True

    result = executor.run_tool("create_folder", {"path": r"C:\Windows\x"}, spy)
    assert "error" in result
    assert asked == []


def test_read_tool_runs_without_confirmation(tmp_path):
    assert "entries" in executor.run_tool("list_directory", {"path": str(tmp_path)}, deny_all)


def test_reversible_tool_runs_without_confirmation(tmp_path):
    assert "created" in executor.run_tool("create_folder", {"path": str(tmp_path / "made")}, deny_all)
