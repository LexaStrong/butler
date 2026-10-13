# Security model

## What you chose, and what it costs

Butler runs elevated, as you asked. Anything the model can reach through a tool
runs with administrator rights. The main risk is not the model deciding to
misbehave. It is **prompt injection**: a web page, PDF, email, or filename that
contains text trying to steer the model. Read-only tools return file contents to
the model, so a poisoned file could try to make it call a write tool.

### Controls in this version

1. **No shell tool.** The model cannot run arbitrary PowerShell or cmd.
2. **Fixed allowlists.** Apps and tool names are fixed lists.
3. **Tiers.** Side effects beyond reversible actions require your approval;
   destructive actions require typing a phrase.
4. **Protected roots.** Writes under Windows system folders are refused even when
   approved.
5. **Audit log.** Every proposal is recorded, including ones that were blocked.

### Known gaps

- `read_text_file` and `list_directory` can read any path the admin account can
  read: other users' files, and possibly secrets stored in plain text. Add a
  path allowlist if that matters to you.
- The audit log is a plain file the same account can edit. It is a record, not
  tamper-evident evidence.
- Approval prompts appear in the same console as the model's output. Read the
  whole prompt before answering.
- Small local models follow safety and tool-use instructions less reliably than
  large hosted ones. Treat the model as untrusted input.
- Butler does not sandbox `open_app`. The app runs as you, elevated.

## Recommendations

- Prefer a separate admin account for Butler if you can. Keep banking, email,
  and client data out of its reach.
- Keep Windows Defender and Windows Firewall on. Butler does not change them.
- Review `audit.jsonl` regularly, especially at the start.
- Test on throwaway folders before pointing Butler at anything important.

## Reporting

If the model acts outside its tier, check the audit log and note the matching
lines. Remove any secrets before sharing them.
