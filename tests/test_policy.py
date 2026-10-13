from butler import policy


def test_read_tools_allowed():
    assert policy.decide("system_info") is policy.Decision.ALLOW
    assert policy.decide("list_directory") is policy.Decision.ALLOW


def test_unknown_tool_denied():
    assert policy.decide("run_anything") is policy.Decision.DENY


def test_forbidden_tool_denied():
    assert policy.decide("format_drive") is policy.Decision.DENY


def test_destructive_needs_typed_confirmation():
    assert policy.decide("delete_path") is policy.Decision.TYPED_CONFIRM


def test_system_needs_confirmation():
    assert policy.decide("install_package") is policy.Decision.CONFIRM


def test_create_folder_blocked_under_windows():
    assert policy.argument_violation("create_folder", {"path": r"C:\Windows\Temp\x"})


def test_create_folder_blocked_under_program_files():
    assert policy.argument_violation("create_folder", {"path": r"C:\Program Files\evil"})


def test_create_folder_allowed_in_user_space():
    assert policy.argument_violation("create_folder", {"path": r"C:\Users\demiurge\Desktop\notes"}) is None
