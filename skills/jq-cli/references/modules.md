# jq Module and Import Safety

Use this when a jq filter uses `import`, `include`, module metadata, or a
repository-provided `.jq` filter that may load other files.

## Default Stance

Treat jq modules as code, not as data. Do not run an unknown module against
sensitive input just because the top-level jq filter looks small.

## Search Path Rules That Matter

- jq modules are `.jq` files.
- `import` and `include` search module paths, and module metadata can alter the
  search path.
- `-L directory` / `--library-path directory` uses explicit module search paths;
  when `-L` is used, jq does not use the builtin default search list.
- Without `-L`, jq's default search path can include user-level locations such
  as `~/.jq`, `$ORIGIN/../lib/jq`, and `$ORIGIN/../lib`.
- If a home-directory `.jq` path exists as a file, jq can source it into the
  main program automatically.

## Safe Procedure

1. Inspect the top-level filter file before running it:

   ```bash
   rg -n '^\s*(import|include)\s+"' transform.jq
   ```

2. Inspect referenced module files and any module metadata search entries.
3. Prefer an explicit `-L` directory that contains only the expected modules:

   ```bash
   jq -L modules -f transform.jq input.json
   ```

4. Avoid unknown modules for secret-bearing, production, customer, or otherwise
   sensitive inputs.
5. Do not assume a clean machine-level or user-level jq environment. If behavior
   must be reproducible, make module paths explicit and document them.

## Red Flags

- The filter imports modules from a repository you have not inspected.
- The task asks to process secrets, credentials, customer records, production
  exports, or private logs.
- The result differs across machines or only fails in CI.
- A command works without `-L` but depends on user-level module locations.

## When Not To Use Modules

For a short one-off extraction or validation, prefer a simple inline filter or
checked temporary `-f` filter over adding module search paths.
