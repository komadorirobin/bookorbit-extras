# Verification record

Assembled 2026-10-31 from the exact revisions in `compatibility.json`. This is
packaging and source validation, not a production deployment or a new claim of
physical-device acceptance.

- Both distributed device patch files are byte-identical to the pinned public
  Ereader source; SHA-256 values are checked by `python3 scripts/check.py`.
- Undo state tests pass in Lua and LuaJIT.
- Actual unmodified BookOrbit plugin source at each complete 1.5.5, 2.0.0 and
  2.1.0 profile passes the undo lifecycle, event, queue, transport and source-
  compatibility tests in both interpreters. Newer unknown source is not
  automatically accepted; the guard deliberately rejects untested profiles.
- Hardcover source `fa352e77` passes the mocked single-writer suite in Lua and
  LuaJIT: existing/default settings, automatic progress/completion/close/resume,
  deferred callbacks, menu controls, local-only linking, metadata reads,
  repeated reader instances and retained explicit manual status actions.
- Both server diffs pass `git apply --check` against separate clean exports
  of their exact pinned bases. They have NOT been combined or deployed.
- The unchanged tag API implementation `0cf7db1` passes 215 tests across the
  actual DTO/controller/service/OPDS suites under Node 24. Tests cover bounded
  mandatory parameters, safe IDs, unknown query rejection, exact parameterized
  tag lookup, authentication/no-store response and current-user access/content
  scope. Previous full typecheck/lint/format verification is recorded in the
  OrbitUI project's October 31 tag work; source has not changed here.
- Directory secret scan passes. No `.env`, account credentials, production
  library, fonts, artwork or whole third-party plugin is distributed.

The included GitHub workflow reruns byte/notice checks, device regressions
against immutable public sources, and exact-base server-application checks.
It does not deploy, make a release, mutate a remote reading record or run a
production database migration.

Outstanding: live authenticated tag API acceptance after an administrator's
separate deployment decision; any combined server rebase; current reader
fonts/touch/rotation/sleep and real end-to-end undo/Hardcover behaviour. The
included old undo guide has a separate isolated PostgreSQL smoke test. Do not
use real Hardcover records or an internet-connected production clone for it.

## Svenska

Enhetspatcharna är oförändrade kopior av angiven offentlig Ereader-revision.
Tillstånds- och pluginregressioner fungerar i båda Lua-tolkarna mot de exakta
versionerna. Båda serverpatcharna klarar tillämpningskontroll mot **var sin**
angiven bas. Tagg-API:ts 215 riktade tester fungerar; inga produktionsdata eller
konton har använts. Hemligheter eller kompletta externa plugin skickas inte med.

Detta bevisar inte funktion på en fysisk enhet eller en driftsatt server. En
kombinerad serverversion måste granskas och testas separat. Arbetsflödet här
publicerar inga releaser och driftsätter ingenting automatiskt.
