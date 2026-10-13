# Tools

## Available

| Tool | Tier | Approval | What it does |
|---|---|---|---|
| `system_info` | read | none | OS, CPU, RAM, disk summary |
| `list_directory` | read | none | Lists a folder (max 200 entries) |
| `read_text_file` | read | none | Reads the first 64 KB of a text file |
| `list_processes` | read | none | Top processes by memory |
| `open_app` | reversible | none, logged | Opens notepad, calculator, explorer, or paint |
| `create_folder` | reversible | none, logged | Creates a folder outside the protected roots |

## Reserved (declared in policy, no implementation, unreachable)

| Tool | Tier | Result if requested |
|---|---|---|
| `install_package` | system | Denied: no implementation |
| `delete_path` | destructive | Denied: no implementation |
| `format_drive` | forbidden | Always denied |

## Tiers

| Tier | Decision | Examples |
|---|---|---|
| read | allow | listing, reading, system info |
| reversible | allow, logged | opening apps, creating folders |
| system | `y/N` prompt | installs, service changes |
| destructive | type `CONFIRM <tool>` | deletes |
| forbidden | deny | disk formatting, disabling the audit log |

## Protected write roots

Any `create_folder` path under these is refused, even if you would approve it:

- `C:\Windows`
- `C:\Program Files`
- `C:\Program Files (x86)`
- `C:\ProgramData`
