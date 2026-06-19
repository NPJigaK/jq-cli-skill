# jq Shell Quoting Reference

Use this when a jq filter contains quotes, brackets, variables, pipes, or when a
command must work in a specific shell.

## Default Strategy

Prefer `-f filter.jq` for complex filters. It removes most shell quoting risk
and makes the jq program reviewable.

```bash
jq -f transform.jq input.json
```

Use command-line filters only when they are short and easy to quote.

## POSIX Shells

Use single quotes around the jq program:

```bash
jq '.["foo"]' input.json
jq --arg name "$name" '.items[] | select(.name == $name)' input.json
```

If the filter itself must contain a single quote, switch to a filter file.

## PowerShell

Use single quotes around short jq programs, but account for native-command
argument passing differences when the program contains embedded double quotes.

For PowerShell 7.3+ with Standard/Windows native argument passing, embedded
double quotes are preserved:

```powershell
jq '.["foo"]' input.json
'{"foo":42}' | jq '.["foo"]'
jq '.["foo.bar"]' input.json
```

For Windows PowerShell 5.1 or `$PSNativeCommandArgumentPassing = "Legacy"`,
escape the embedded quotes so the native jq process receives them:

```powershell
jq '.[\"foo\"]' input.json
'{"foo":42}' | jq '.[\"foo\"]'
jq '.[\"foo.bar\"]' input.json
```

If a command must work across both modes, use `-f filter.jq` instead of an
inline filter.

For simple identifier keys, avoid inner quotes:

```powershell
jq '.foo' input.json
```

Prefer `--arg` for PowerShell variables:

```powershell
jq --arg status $status '.items[] | select(.status == $status)' input.json
```

## cmd.exe

Use double quotes around the jq program and escape inner double quotes:

```cmd
jq ".[\"foo\"]" input.json
```

For anything beyond a short filter, write a `.jq` file and use `-f`.

## Windows POSIX-Like Shells

When WSL, MSYS2, or Cygwin invokes a native Windows `jq.exe`, use
`--binary` / `-b` when exact LF output matters. This controls jq's newline
translation; it does not solve shell quoting or safe file replacement.

## Dynamic Keys and Values

Do not interpolate dynamic keys into the jq filter:

```bash
# Wrong when key comes from a user or variable.
jq ".[$key]" input.json
```

Pass the key as data:

```bash
jq --arg key "$key" '.[$key]' input.json
```

Pass JSON values only when they are intended to be parsed as JSON:

```bash
jq --argjson patch '{"enabled":true}' '.config += $patch' input.json
```

## CI YAML and Nested Shells

When a command is nested inside YAML, npm scripts, Makefiles, SSH, or another
agent prompt, quote pressure multiplies. Prefer a checked-in or temporary
filter file:

```jq
# transform.jq
.items
| map(select(.enabled == true))
| sort_by(.name)
```

```bash
jq -f transform.jq input.json
```

## Here Documents

In POSIX shells, a single-quoted heredoc delimiter avoids expansion:

```bash
cat > transform.jq <<'JQ'
.items[] | select(.status == $status)
JQ
jq --arg status active -f transform.jq input.json
```

Use PowerShell here-strings only when you verify the file content and encoding
are suitable for the target environment.
