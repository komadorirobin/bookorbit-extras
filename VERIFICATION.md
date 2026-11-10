# Verification record

## BookOrbit plugin 2.2.0 compatibility and device installation, 2026-11-10

Initial offline investigation: the user reports `untested main.lua` after
updating BookOrbit, and then an absent BookOrbit menu. The existing pre-init
guard explains both: protected state
prevents an unreviewed plugin from initializing at all. At that stage no device
was connected to ADB. The implementation was initially local; publication and
the subsequently authorized closed-app installation are recorded below.

Official latest release checked through GitHub is **3.7.0**, commit
**6f8f5f4818eb737dc4d78fc5b5294fc3adb26860**, containing KOReader plugin
**2.2.0**. Its entire `koreader-plugin` tree is identical to checked main
**022f9d10206946258cc6d677778ad7e9750c8319**. The previous patch reproduces
the compatibility failure against that unmodified source. Ereader runtime
**87ebcd3670c20d2a9fe0ed6579440d7aaf98b04b**, with relative-path fixture follow-up
**431a4d11caaec0bff850524d0301350ffae27e4b**, adds one complete exact profile,
without weakening the version-independent fingerprint or pre-init state guard.
The mirrored device patch SHA-256 is
`c5b2f98e6ebcf8d5a46143c3d22371b2c23a243963dc231d901636b354b8445d`.

Compared with tested 2.1, seven protected API/sync/queue source files are
byte-identical. Only normalized main and the two menu files change: 2.2 adds
a File browser action, deferred native Home event and a return-home bypass
for that exit. The reviewed profile requires all ten matching files, never a
mix of releases. It still rejects any modified protected file before init.

- State and unmodified-source integration suites pass under Lua 5.5 and LuaJIT
  for all four complete 1.5.5/2.0.0/2.1.0/2.2.0 sources, in both patch repos.
  Existing page-turn/commit, reload, pending/offline undo, account/book isolation,
  upload exclusion/acknowledgement, queues and compatibility tests remain.
- Added 2.2 cases keep native File browser and Undo together, verify two-tick
  close/Home ordering, no provisional outbox/upload, original ID/snapshot and
  hold surviving document/widget close, successful confirmed Undo from the
  file manager, and ordinary return-home preference when no bypass is requested.
- Twelve unmodified upstream menu, lifecycle, outbox, coordinator, job-runner
  and sweep suites pass under LuaJIT. A separate attempted Lua 5.5 run exposes
  upstream fixture assumptions about Lua 5.1 `os.execute` results, then native
  `setfenv`; it is not reported as passing or used instead of the LuaJIT run.
  The patch's own integration/state suites run on both interpreters unmodified.
- The existing Hardcover single-writer tests, syntax, mirrored exact bytes and
  checksum/notice checks pass. CI includes the fourth exact-source profile.
  Tests mock UI/storage/transport; no real account, reading or Hardcover write.

Server sources, migrations, image/production installation, permissions, saved
settings/history/openings and public release assets are unchanged. Collection
0.3.0 labels still describe the existing public release, not a new release of
these bytes. Server/database suites are not rerun for this device-only change;
the server support remains exact 3.6.0, not automatically 3.7.0-compatible.
The initial local pass did not publish or install anything; update/install
required separate direction and a closed-app backup of current device state.
Private source/diff/test evidence starts at `/tmp/bookorbit-undo-compat.baw9do/`;
the exact official release plugin and retained test logs are also kept under
ignored `test-results/device-22-20261110/` in this checkout. Relative plugin
paths use a real working-directory primitive in the drawing/FS fixture; the
real stock menu path resolver remains unchanged.

Publication follow-up: the user explicitly approved pushing the fix to both
repositories and installing KOAssistant on the Bigme. Ereader **431a4d11** and
Extras **2e6dd22b** are pushed to their respective `main` branches. The public
Ereader patch blob **c64ccb77** matches the reviewed local bytes. All six jobs
in [GitHub run 42879460938](https://github.com/komadorirobin/bookorbit-extras/actions/runs/42879460938)
pass, including device/artifact checks and the five unchanged server matrices.
No new collection tag/release, old asset replacement or server operation.

ADB is now connected. The installed BookOrbit main reports **2.2.0**, and the
old device patch lacks that profile, confirming the reported mismatch. Official
KOAssistant **0.24.1**, tag commit **c014efe9**, ZIP SHA-256
`a2630b01c0f4b2642f1a9a7257f20b3ab3150580df6f29a9f115a99b3868d54e`
matches the GitHub release digest: 7,391,588 bytes, 360 regular package files,
30,077,775 expanded bytes, safe paths/CRC/types and 266 LuaJIT syntax files.
No AI request, account login or credential transfer is part of installation.

After the user confirmed KOReader was fully closed, the fresh compressed
backup passed gzip integrity plus all 465 archive-entry path/type/exclusion
checks. It includes reader preferences, settings, history, the old undo patch
and the installed BookOrbit source. The large bookinfo caches were explicitly
excluded because this installation does not change them. The private backup
and receipts remain under ignored `test-results/device-22-20261110/install/`;
they are not distributed in this repository.

- The pulled device BookOrbit plugin is byte-identical to the complete official
  2.2.0 source. The undo integration suite passes again against that actual
  device copy under both Lua and LuaJIT, with fake UI/storage/transport.
- The updated undo patch was staged, checked and renamed into the original
  patch path. Its installed SHA-256 matches `c5b2f98e...b8445d` above. The old
  `5668f969...13aa6` patch is retained inside the verified host backup.
- The unmodified official KOAssistant 0.24.1 package was staged outside the
  plugin directory, then installed at `plugins/koassistant.koplugin`. All 360
  installed regular-file hashes match the reviewed extracted package. No
  previous KOAssistant installation was present or overwritten.
- Reader preferences, history, BookOrbit sync state and statistics database
  hashes match the closed-app backup and match before/after installation.
  No existing book file, book sidecar, plugin settings, permission or sync
  account was edited. The existing guarded opening state was retained.

KOReader remains closed. Native first-start/menu acceptance and KOAssistant
setup/login are still pending with the user; neither a real-book sync/undo nor
an AI request was performed as an installation test. No claim of on-device
runtime acceptance or automatic account configuration is made here.

## Reading-status publication and requested server deployment, 2026-11-01

After OrbitUI Beta 28 publication, the user explicitly authorizes publishing
and deploying the server extension. Collection 0.3.0 exposes the unchanged
read-statuses v1 patch, retains exact official 3.6.0 compatibility and leaves
the helper's `both` default and all device/older patch bytes unchanged. CI now
covers `status` and `all` as well as `undo`, `tags` and `both`.

The existing production server has its own earlier undo extension and historical
0101 migration. Do not replace it with the generic 0132 build. The deployment
candidate reproduces that exact current source before applying status alone;
no production migration, schema or existing undo change is required. Release,
fresh tests, backup/restore, complete-source notice and deployment verification
are recorded below. The user separately approves the modified build name
**Littex**, keeping BookOrbit attribution and the complete-source offer.

**Completed:** public release **v0.3.0**, tag source
`644640a876789941b61ff88c5687a2dbac0c2cae`, published **19:52:52 UTC**.
All uploaded draft artifacts were downloaded and SHA-256 verified before
publishing. Anonymous download of the complete Littex source matches the
operated build's source archive. No older release assets or tags were changed.

- GitHub run **41341624599** passes all six jobs: device/artifact checks and
  exact-source `undo`, `tags`, `both`, `status`, `all` server combinations,
  including typecheck, full server ESLint, build and relevant tests.
- The existing installation's 2,772 tracked runtime source files and 6,008
  compiled files were compared to the original source/builder before porting.
  The Littex candidate preserves its existing custom undo patch exactly and
  changes no schema, migration, migration ledger logic or dependency lockfile.
  Old and new runtime migration directories are byte-identical.
- That exact candidate passes **1,567 server tests**, typecheck, full ESLint,
  **14 client tests**, client typecheck/lint/format and the native asset build.
  All **13 native undo PostgreSQL tests** also pass against a restored copy,
  completing the database cases skipped by the earlier unit run.
- Tests use a dedicated Docker-internal network with outbound access blocked,
  disposable PostgreSQL 16 matching production, no production filesystem mounts
  and synthetic application secrets. The native migrator leaves all **177**
  restored table fingerprints, including the ledger, unchanged.
- Authenticated status acceptance passes both on that isolated copy and after
  deployment, through loopback and public HTTPS. A 200-ID request (including
  a duplicate and missing ID) returns the expected 198 distinct rows with exact
  canonical timestamps. Authentication, unauthenticated native undo guard,
  invalid/oversized queries and no-store pass. All 12 protected reading/book/
  migration tables are unchanged across those GET-only checks. No test writes
  to real reading status or Hardcover are issued. The single HTTPS status
  request took 365 ms; this is not a physical reader/startup benchmark.
- Immediately before cutover, with only the app stopped, a fresh database dump
  was restored into another disposable database and all **177** table counts/
  hashes matched. Appdata's **2,407,864,320-byte** backup was compared against
  its stopped source. Configuration, old image/assets and backups are retained
  privately for application rollback. No production database restore occurred.
- Deployment completed **19:54:13 UTC**, image
  `littex-local:3.6.0-status-v1-20261101`, ID
  `sha256:2a1a4f9b7de2ed7b12bf550543bf1c1ca334293aeeb2955ddb08f9c42f01ce6b`.
  Health is green; database and unrelated containers remain the same instances.
  Credentials, ports, data mounts, PWA overrides and saved sync choices are
  unchanged. All 5,802 existing hashed client assets are retained alongside
  the new assets. The normal startup touches session/refresh-token cleanup
  and derived daily statistics only; the 12 protected tables, including all
  reading status/history, opening state, book files and migration ledger, match
  the stopped baseline after startup.
- The anonymous deployed UI renders **Littex**, preserved Powered by BookOrbit,
  copyright/license/additional terms, a modification notice in Swedish/English
  and a working offer of full Corresponding Source. Browser console reports
  no errors on login/Legal notices. New-commit secret scans pass. The full
  upstream tree scan's 36 generic-key findings are confined to 22 files verified
  byte-identical to official upstream; no private credentials were added.
- Both isolated test containers, their disposable volumes and internal network
  are removed after verification. Production remains healthy with zero restarts
  and no startup error log lines. Backups, complete source and the old runtime
  image/assets remain available for recovery; no production files were deleted.

Exact complete-source archives in the release:

- `littex-3.6.0-status-v1-20261101-source.tar.gz`, source commit
  `819daf512e235102c82d668ffa258ef86a43f9fa`, 34,688,481 bytes,
  SHA-256 `4f3149cf0bc3a5687019906165cad8755194360c87005b52fa97fd2a93e1d487`.
  This is the separately reviewed existing legacy-0101 installation, NOT a
  generic image/database upgrade.
- `bookorbit-3.6.0-extras-0.3.0-all-source.tar.gz`, source tree
  `78ce0355b4e1ba750763f078b2f8621df0999616`, 34,758,425 bytes,
  SHA-256 `157c5555dc0f70fea0f4314fa047303969e5584802156f4ab6b40a8027ee699e`.
  This is the portable exact-base helper output with generic migration 0132.

Private evidence: `test-results/status-release-20261101/`. Database/appdata
backups, credentials and deployment configuration stay private on the server,
not in Git or release assets. OrbitUI Beta 28 bytes remain immutable, no reader
is installed/changed, and the client importer is still OFF by default. Physical
Bigme status-import/conflict/lifecycle acceptance remains pending.

Svenska: 0.3.0 är publicerad och det godkända Littex-bygget är driftsatt med
fungerande autentiserat status-API. En färsk backup har återställningstestats;
läsdata och befintlig ångring är bevarade. Ingen databasmigrering eller verklig
testskrivning till lässtatus/Hardcover behövdes. Funktionen i läsaren aktiveras
separat, och test av själva importen på fysisk enhet återstår.

## Local reading-status API follow-up, 2026-11-01

Not published or deployed. User explicitly authorizes local implementation,
not a running server change. `status.patch` targets exact official 3.6.0
`a96ff0c85a4c25e9126dfa4c71ea87537a3baf7a`, local implementation
`6cb2feb2938d564b3bade449f649d885a91e49b1`. Patch SHA-256:
`ba588d41ee7323b5b46ff0e3603294ed7dbbcc0e46d3a56c34a58a45a8d24bbd`.

- GET-only, native KOReader auth, mandatory explicit batches of 1..200 safe
  IDs, strict extra-field rejection and no-store. Canonical status update and
  finish timestamps; missing/inaccessible/filtered rows are omitted.
- Status-only exact-source DTO/controller/service/SQL tests: **194 passing**.
  Combined undo+tags+status Koreader/OPDS suites: **1,058 passing in 44 files**.
  Server typecheck and targeted ESLint pass for standalone and combined source.
- Six source-helper integration tests pass, including status-only without
  migrations, unchanged `both`, all-three atomic composition, complete-source
  archive, dirty-checkout and existing-archive refusal. Checksums pass.
- No schema or migration change in this addition, no detail/progress/cover
  hydration, no API write or Hardcover call. No production database,
  credentials, Docker service or server image is touched.
- OrbitUI's local importer has separate synthetic 3,000-match, stale-state,
  cancellation, conflict and native payload acknowledgement tests. It is
  disabled by default. Physical Bigme latency/UI and live fixture round-trip
  remain pending because ADB is disconnected.

Local evidence is under `/tmp/orbitui-status-api.9FBdOz/`; OrbitUI's durable
local test record is `test-results/status-import-20261101/` in its checkout.
Any deployment still requires explicit approval, backup/restore verification,
an exact complete-source image and the existing licensing/source-offer steps.

## Same-cover reload fix, collection 0.2.1

Checked locally 2026-11-01. The device Undo patch and its mirrored Ereader copy
now reuse the original provisional opening when the same unchanged cover is
reloaded. Duplicate `ReaderReady` no longer commits it. A close/reopen is
accepted only after checking the saved sidecar before load and the file,
document digest, initial page and annotations at readiness. Normal reopen
summary bookkeeping may change without replacing the original unread snapshot.

- The new duplicate-readiness regression fails against the previous patch in
  both the state suite and the unmodified stock-plugin integration suite.
- Updated state and actual-source suites pass in Lua 5.5 and LuaJIT against
  complete BookOrbit 1.5.5, 2.0.0 and 2.1.0 source profiles. The same tests run
  from both patch repositories. Source fingerprints are unchanged.
- Checks cover fresh reader/plugin instances, changed page count on the cover,
  original ID/snapshot/deadline retention, one remote registration, continued
  outbox/upload holds, the native menu/sheet action, undo after reopening and
  an excluded statistics interval spanning the reloaded sessions.
- Real page turns still commit. Book changes, different digests, modified
  annotations/progress/status, missing preload evidence and expiry cannot
  revive Undo. Pending Undo remains recoverable; committed/undone openings and
  locally restored pending cleanup are never reactivated. Account isolation
  and the existing offline/conflict/Hardcover retry tests still pass.
- The unchanged Hardcover single-writer regression passes in both interpreters.
  Lua syntax checks, mirrored-byte checks and the distributable checksum/notice
  check pass. `compatibility.json` pins the updated exact Ereader revision.
- No server source, migration, compatibility profile, user history or saved
  opening state was changed. Server/database suites were not rerun for this
  device-only fix. The device is not currently connected over ADB, so this
  revision has not been installed or physically verified there. No push or
  release was performed for this local change.

Svenska: omladdning av samma oförändrade omslag behåller ångramöjligheten.
Tester mot alla tre stödda pluginversionerna fungerar i båda tolkarna, inklusive
sidvändning, bokbyte, väntande ångring och skydd mot ändrad läsdata. Rättningen
är lokal; ingen enhet, server eller befintlig läshistorik har ändrats.

Publication follow-up, 2026-11-01: the user explicitly authorized pushing and
publishing this fix. Ereader `30ded4e3f7fb1434ecc095e4feeb8ac48079d1b7` and Extras
`4c7e1b242a487982589733d892baec47cffbe870` are pushed. Annotated tag **v0.2.1**
pins that Extras source; its public release was published at **09:36:57 UTC**.
The draft download matches both uploaded artifacts byte-for-byte. The published
Undo asset SHA-256 is
`5668f9695b4d09e3faa6e1edae628754367e5834559374b9e33da26c91f13aa6`, and the
public Ereader catalogue blob matches the same local Git blob. Outgoing Gitleaks
checks pass for both repositories. No device installation or server deployment
was performed. These verification-only notes do not change the tagged artifacts.

## Official 3.6.0 port, collection 0.2.0

Checked 2026-10-31 against official release v3.6.0, published 2026-10-28,
source `a96ff0c85a4c25e9126dfa4c71ea87537a3baf7a`. This is a source port and
isolated validation, not a deployment to a user's server or an assertion of
compatibility with newer `main` commits.

- Undo port implementation: `52c0a3a18ff8058fb8adc1179e506389a17665e0`.
  Migration 0132 was generated by Drizzle Kit from the actual 3.6.0 schema;
  upstream migrations, metadata/delivery providers and reading-event modules
  were preserved. No dependency or lockfile changes.
- The preflight detects the old custom 0101 SQL hash before the native ledger
  timestamp repair can treat it as 0132 and skip official migrations. Legacy
  or unknown extension databases are refused, not silently upgraded. This
  does not constitute an upgrade plan for an old custom 3.2.0 database.
- The undo-only relevant regression passes 1,396 tests. Native HTTP/auth tests
  verify actual Fastify routes, KOReader credentials, account/permission
  rejection, strict DTO validation and response shapes. Ordinary Hardcover
  sync waits for a protected opening or pending remote cleanup; new native
  ownership conflicts do not authorize writes to another reading attempt.
- A separate loopback-only PostgreSQL 18 + pgvector container was initialized
  with all **132 official 3.6.0 migrations**, then upgraded using the patched
  native migrator. All **15 PostgreSQL integration tests** pass; repeating the
  migrator succeeds. Legacy-ledger refusal is also tested inside a rolled-back
  transaction, proving that no ledger rows were rewritten by that check.
- Both features together pass **1,611 tests across 68 files**, including those
  15 database tests, tag query/DTO/controller/service/OPDS access scoping,
  ordinary reading-status/Hardcover regressions and native HTTP validation.
  Stable tag port: `3c39bdd8e4ce68c7d10abc30d76cc03eea9bbac8`.
- Server typecheck, full ESLint, formatting of changed sources and the native
  server build are validation gates. See CI for a fresh run of undo-only,
  tags-only and combined source builds against the same exact stable release.
  The combined full ESLint run needed a 6 GiB Node heap after exhausting the
  default 4 GiB limit; this changes no application runtime setting.
- The preparation helper verifies exact source revision, checkout root,
  clean state and checksums before one atomic staged application. Its optional
  archive contains the full exact upstream source plus selected modifications.
  Existing archives or local work are not overwritten. It never operates a
  server or database.
  Its four local exact-source integration tests pass, including full archive
  contents and fail-closed behaviour for existing work, subdirectories and
  archive overwrite attempts.
- Device patch files and legacy patch bytes are unchanged. Their prior
  interpreter/source-profile results remain applicable. No production
  environment, credentials, library files or real Hardcover records are used.

Before production, an administrator still needs to review backup restoration,
any legacy database upgrade, modified-build notices/full-source hosting, image
build/deployment and live reader/API acceptance. No container image has been
published and no production migration or remote Hardcover write was performed.

Svenska: portningen gäller exakt officiella 3.6.0. Uppgradering från den normala
3.6.0-databasen och alla 15 databastester fungerar i en separat testinstans;
1 611 tester fungerar med båda funktionerna tillsammans. Gamla egna 3.2.0-
databaser stoppas och kräver en separat granskad plan. Ingenting är driftsatt
och inga riktiga läsningar har ändrats.

## Original collection 0.1.0 (historical, separate bases)

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
