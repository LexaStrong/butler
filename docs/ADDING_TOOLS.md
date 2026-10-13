# Adding a tool

1. **Implement it** in `butler/tools.py` as a plain function that returns a dict.
   Return `{"error": ...}` for expected failures instead of raising.
2. **Register it** in `IMPLEMENTATIONS`.
3. **Describe it** with `_schema(...)` in `TOOL_SCHEMAS`. Use `enum` for fixed
   choices so the model cannot invent values.
4. **Assign a tier** in `butler/policy.py` (`TOOL_TIERS`). Unlisted tools are denied.
5. **Add argument rules** in `policy.argument_violation` if the tool writes to disk.
6. **Test it.** Cover the happy path, a bad argument, and a case the executor
   must refuse.
7. **Document it** in `docs/TOOLS.md` and add a line to `docs/CHANGELOG.md`.

Keep tools narrow. `open_app` with an allowlist is safer than a generic `run_command`.
