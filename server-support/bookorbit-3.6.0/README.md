# BookOrbit 3.6.0 server extras

Independent, optional modifications, 2026-10-31. Not an official BookOrbit
release. Nothing here deploys a server or changes a database automatically.

This directory targets the latest official release checked on 2026-10-31:
**BookOrbit v3.6.0**, exact source
`a96ff0c85a4c25e9126dfa4c71ea87537a3baf7a`.
It does **not** mean 3.2.0+, an arbitrary newer release or the moving `main`
branch. New upstream versions need a fresh compatibility review.

| Optional component | Purpose | Database change |
| --- | --- | --- |
| `undo.patch` | Undo an accidental unread-book opening before actual reading. Native KOReader authentication, owned reading attempt and guarded Hardcover cleanup. | Drizzle-generated **0132_undo_reading_opening** after the official 3.6.0 history. |
| `tags.patch` | Read-only exact tag matching restricted to supplied local book IDs, user libraries, present books and content filters. | None. |
| `status.patch` (experimental, collection 0.3.0) | Authenticated GET-only status and modification/finish timestamps for supplied matched IDs. OrbitUI Beta 28's optional background importer. | None. |

Use `--features status` to select status reads alone or `--features all`
to combine all three patches. The existing `both` default still means only
undo and tags; existing build commands do not silently activate a new API.

### Reading-status API v1

`GET /api/v1/koreader/plugin/catalog/read-statuses?ids=1,2` returns
`{ "version": 1, "items": [{ "id": 1, "status": "read", "updatedAt": "2026-10-31T12:00:00.000Z", "finishedAt": "2026-10-30T00:00:00.000Z" }] }`.
`finishedAt` may be null. IDs are mandatory, positive safe integers, at most
200 per request. Invalid/extra inputs are rejected. Missing statuses and
inaccessible/deleted/filtered books are omitted, not synthesized as unread.
The normal KOReader credential guard, per-user library/content scope and
`Cache-Control: no-store` apply. One bounded query selects only status fields;
no detail/cover/progress hydration, mutation, migration or remote service call.
`updatedAt` belongs to the canonical user status, not generic book metadata.
OrbitUI preserves newer local edits and ambiguous same-day local conflicts.

All three patches target the **same exact 3.6.0 base**. They can be selected
individually or together. The 3.6.0 plugin is already supported by the unchanged
device patch. No new automatic Hardcover writer is introduced. Want to read
[BookOrbit] already uses the standard API and needs neither server patch.

## Important: an old custom 3.2.0 database is not an ordinary upgrade

The old undo extension used migration **0101**. Official BookOrbit has since
used that number and added later migrations. Its SQL is also identical to the
new 0132 migration, so native migration-ledger timestamp repair could otherwise
skip official migrations. The new undo patch performs a read-only preflight
**before any migration or ledger repair** and refuses legacy/unknown extension
databases.

This package supports a fresh or normally migrated **official 3.6.0 database**.
It is **not** an automatic upgrade procedure for the old custom 3.2.0 database.
Resolve protected openings and pending Hardcover cleanup on the old server,
back up and verify restoration, then obtain a separately reviewed database
upgrade plan. Do not delete `reading_openings`, edit migration hashes/timestamps,
reset device state or drop history to bypass the safety check. Do not run
official migrations first on an old extension database to bypass the check.

The old 3.2.0 compiled Docker overlay is retained as a legacy artifact in the
sibling directory. **Never copy its compiled files or migration 0101 over 3.6.0.**

## Prepare a separate source build

Prerequisites: Git, Python 3, Node 24+ and pnpm 11+. Use a new source checkout,
not a running installation. Set `EXTRAS` to this repository's absolute path.

```sh
git clone https://github.com/bookorbit/bookorbit.git orbitui-bookorbit-3.6.0
git -C orbitui-bookorbit-3.6.0 switch --detach a96ff0c85a4c25e9126dfa4c71ea87537a3baf7a
python3 "$EXTRAS/server-support/bookorbit-3.6.0/prepare-source.py" \
  orbitui-bookorbit-3.6.0 --features both \
  --source-archive bookorbit-3.6.0-extras-source.tar.gz
cd orbitui-bookorbit-3.6.0
pnpm install --frozen-lockfile
pnpm --dir server type-check
NODE_OPTIONS=--max-old-space-size=6144 pnpm --dir server lint:check
pnpm --dir server exec vitest run src/modules/koreader src/modules/user-book-status src/modules/hardcover src/modules/opds src/scripts/opening-migration-preflight.test.ts
pnpm --dir server build
```

Use `--features undo` or `--features tags` instead of `both` if desired. The
helper verifies the exact base, a clean checkout and patch checksums before
applying one atomic, staged diff. It does not install dependencies, connect to
a database, start containers, build an image or deploy anything. The optional
archive contains the full tracked source plus the selected modifications, not
just patch files. It refuses to overwrite an existing archive.

Build with upstream's complete Dockerfile from the patched checkout. Keep the
matching dependencies, migrations, server and client together. Do not create
a compiled-file overlay on top of a different image. Review and run the
isolated checks below before a separate deployment decision.

### Isolated database tests

Use an empty, disposable PostgreSQL 18 + pgvector instance bound to loopback,
with no production data, mounts, credentials or outgoing Hardcover account.
The database must be named `bookorbit_undo_test` on `127.0.0.1`; the integration
suite deliberately refuses other targets. For an upgrade test, migrate the
unmodified official 3.6.0 source first, then run the patched native migrator.
Set only the test connection URL, never your production `DATABASE_URL`:

```sh
DATABASE_URL="$OPENING_TEST_DATABASE_URL" pnpm --dir server exec tsx src/scripts/migrate.ts
pnpm --dir server exec vitest run src/modules/user-book-status/reading-opening.repository.integration.test.ts
```

The suite creates unique fixtures, checks idempotency, history/progress/bookmark
protection, ownership, concurrency, pending remote cleanup and legacy-ledger
refusal. It never truncates the library. Other tests mock Hardcover transport;
do not substitute real reading records. CI uses a separate disposable database
and also verifies upgrading from official 3.6.0 and repeating the migration.

### Before operating a modified server

Back up and test restoration first. Verify a compatible image against an
isolated copy, authentication, reader start/commit/undo and any selected tag API.
Resolve every protected opening and pending cleanup before removing the undo
extension. A migrated database is not automatically safe for an image-only
downgrade. Never restore an old backup over newer reading activity.

Preserve BookOrbit's license, attribution, About/Legal Notices and upstream
links. Clearly identify the modified version and modification date in the
running UI and provide the full corresponding source for the exact operated
build. The helper's archive is a starting point, not a hosted source offer;
make it accessible to users and include any further modifications. A link to
this patch repository alone does not provide the complete server source. The
operator must finish these presentation/source-offer steps before deployment.

## Svenska

**Version 0.3.0:** `status.patch` lägger till ett separat läsande
API för status, ändringstid och slutdatum, högst 200 kopplade bok-ID:n per
anrop. Bara den inloggade användarens tillgängliga böcker ingår. Ingen
migrering, metadata-/omslagshämtning eller skrivning sker. `--features status`
väljer bara detta tillägg; `all` kombinerar det med taggar och ångring.
Det gamla standardvalet `both` är oförändrat. Ingen server driftsätts automatiskt.

Det här är en **versionslåst portning till officiella BookOrbit 3.6.0**, inte
stöd för alla versioner sedan 3.2.0. Ångra öppning och tagg-API:t har nu samma
bas och kan väljas var för sig eller tillsammans. Enhetspatchen behöver inte
ändras för pluginet som ingår i 3.6.0. Vill läsa [BookOrbit] behöver inget av
dessa servertillägg.

**Viktigt:** En databas med den gamla egna 3.2.0-migrationen 0101 kräver en
separat granskad uppgradering. Den nya patchen stoppar den kombinationen innan
den ändrar migrationshistoriken. Radera inte tabeller, hashar, tidsstämplar
eller enhetens sparade öppningar för att ta dig förbi kontrollen. Slutför
väntande öppningar/fjärrstädning på gamla servern och verifiera backup först.
Paketet gäller en ren eller normalt uppgraderad officiell 3.6.0-databas.

Använd en separat ren utcheckning och kommandona ovan. Hjälpskriptet kontrollerar
bas och kontrollsummor, förbereder källkoden och kan skapa ett komplett
källkodsarkiv. Inget installeras på en server och ingen databas ändras av det.
Bygg en komplett matchande server, använd aldrig det gamla 3.2.0-överlägget.
Bevara licenser och Om-sida, ange modifiering/datum i körande gränssnitt och
gör hela den faktiskt använda källkoden tillgänglig före driftsättning.
Serverinstallation, återställningstest och aktivering kräver ett separat beslut.
