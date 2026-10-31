# Integration extras for BookOrbit and KOReader

An independent, optional patch collection by komadorirobin. Not an official
BookOrbit, KOReader or Hardcover release. No account credentials are included.
Nothing here deploys a server automatically.

[Svenska](#svenska) | [Compatibility and exact sources](compatibility.json)
| [Device patches](#device-installation) | [BookOrbit 3.6.0 server extras](server-support/bookorbit-3.6.0/README.md)
| [Legacy 3.2.0 overlay](server-support/bookorbit-undo-opening/README.md)

## What needs what?

| Feature | On the reader | On your server |
| --- | --- | --- |
| Want to read [Local] / local EPUB tags | OrbitUI; ordinary local files | Nothing. No account or BookOrbit patch. |
| Want to read [BookOrbit] | Connected BookOrbit KOReader plugin and OrbitUI | Normal BookOrbit Want to Read API. No extras patch. Only matched local books appear. |
| Online BookOrbit tag matches | OrbitUI Beta 22 or newer; connected account-scoped BookOrbit plugin | Optional **tag-matches v1** patch for exact official **3.6.0**. Read-only, linked local results across profiles, batches of 200 IDs. |
| Undo accidental opening | `2-bookorbit-undo-opening.lua`, compatible BookOrbit plugin | **Undo-opening v1 port for official 3.6.0**, migration **0132**. Use the new complete-source build, not the old compiled overlay. |
| One automatic Hardcover writer | `2-hardcover-bookorbit-sync.lua` plus the separate Hardcover plugin, with BookOrbit as your chosen automatic writer | Enable BookOrbit's normal Hardcover integration. No extra server patch for this feature. |

The new [3.6.0 package](server-support/bookorbit-3.6.0/README.md) targets exact
official release `a96ff0c`, the latest stable checked on 2026-10-31. Undo and tags
can be selected individually or together on that base. This does **not** mean
3.2.0+, future releases or the moving development branch. An OrbitUI update
does not install server extensions. Nothing has been deployed to your server.

**Already running the old custom 3.2.0 undo database?** Stop and read the
[upgrade warning](server-support/bookorbit-3.6.0/README.md#important-an-old-custom-320-database-is-not-an-ordinary-upgrade).
Its migration 0101 collides with later upstream history. The new preflight
refuses legacy/unknown extension databases before migration-ledger repair.
That database needs a separately reviewed upgrade, not a blind image change.
Never delete opening state or rewrite migration history to bypass the guard.
The original 3.2.0 overlay and original development-base tag diff remain as
**legacy artifacts**; do not stack those older artifacts or apply them to 3.6.0.

## Device installation

Back up KOReader settings, book sidecars and working patches. Fully exit KOReader
before copying a patch. Install only the features you actually want:

- [Download the undo-opening device patch](https://raw.githubusercontent.com/komadorirobin/bookorbit-extras/main/2-bookorbit-undo-opening.lua)
- [Download the Hardcover single-writer device patch](https://raw.githubusercontent.com/komadorirobin/bookorbit-extras/main/2-hardcover-bookorbit-sync.lua)

Save the chosen file with its exact `.lua` filename in your actual KOReader
`patches/` directory, then restart KOReader. These are userpatches, not folders
to install under `plugins/`. Keep only one enabled copy of each filename.

Already using [Ereader Patch Manager](https://github.com/komadorirobin/ereader-patch-manager.koplugin)?
The same tested device files remain in its existing
[Ereader catalogue](https://github.com/komadorirobin/Ereader). Sync them there;
do not add a duplicate copy from this repository. Packaging here does not change
that catalogue or automatically enable new patches.

### Undo opening: read before enabling or removing

Install and verify the compatible server extension first. This protects an
accidentally opened **unread** book until the first actual page turn, within
24 hours. It is not general-purpose undo for reading history. The current
device patch fingerprints complete source profiles for BookOrbit plugins
1.5.5, 2.0.0 and 2.1.0; later unreviewed source can fail its guard even when a
version number looks similar. See exact commits in `compatibility.json`.

Use the patch's BookOrbit menu/gesture action to commit or undo an opening.
Resolve all protected/pending openings and pending server cleanup **before**
disabling/removing either half. Do not delete `bookorbit_openings` settings or
restore stale progress files to bypass a hold. Unsupported server routes are
not the same as tested server support; see the server guide for fallback and
reconciliation. Never test against real Hardcover reading records.

### Hardcover single-writer patch

Use this only if **BookOrbit is meant to own automatic Hardcover reading
status/progress updates**. Keep KOReader-to-BookOrbit sync enabled. The separate
[Hardcover plugin by Billiam](https://github.com/Billiam/hardcoverapp.koplugin)
stays installed for linking, edition selection, metadata and explicit manual
actions. The patch suppresses that plugin's automatic tracking and makes its
link operation local-only; it does not remove existing duplicates or edit saved
tracking preferences. Manual Hardcover actions can still write to Hardcover.

To restore the plugin's own automatic sync, disable this patch and restart,
after deciding which service should own automatic writes. Avoid two automatic
writers. This patch does nothing when the Hardcover plugin is absent/disabled.

## Server installation is an administrator task

Use the feature-specific guide, a clean checkout of its **exact pinned base**,
`git apply --check`, frozen dependencies and the included tests/typecheck/lint.
Back up the database, verify restoration into an isolated test instance, and
review source/migration/image compatibility before deployment. Never copy a
production `.env`, tokens or library into a public test environment. Do not
change a running server just to try a reader UI feature.

The API patch is deliberately ID-only and authenticated. It narrows the
provided device IDs by the current user's accessible libraries, present books
and content filters. It never enumerates the whole remote library or changes
reading state. Embedded EPUB tags do not need this API.

## Sources, licensing and verification

Collection format **0.2.0**, assembled 2026-10-31. Device patch bytes remain
unchanged from Ereader `6c05155c`. The server undo extension has been ported to
official 3.6.0 and the optional tag API rebased to that same source. The original
development-base tag implementation `0cf7db1` is retained separately. Full revisions,
component versions and SHA-256 values are in `compatibility.json`. No fonts,
artwork, private configuration or complete upstream plugin is bundled.

The collection's original code is AGPL-3.0-only; see [LICENSE](LICENSE).
BookOrbit-derived server changes retain the upstream
[license, attribution notice and additional terms](licenses/bookorbit/).
Powered by [BookOrbit](https://github.com/bookorbit/bookorbit), copyright
(C) 2025-2026 neon and the respective contributors. This is a modified source
patch distribution, not an official or endorsed BookOrbit release. Preserve
the required About/Legal Notices, modified-version notice and an offer of the
complete Corresponding Source for the exact operated version, including
upstream source plus applied patches, if you deploy it. A link to this diff
alone is not the complete source. Do not remove upstream notices or branding
restrictions when building a modified server.

Device and Hardcover transport tests mock storage/network/credentials. Server
integration tests also use a disposable local PostgreSQL database. These do
not validate physical reader behaviour or a production deployment. Run from
this repository root:

```sh
luajit tests/bookorbit_undo_state_test.lua
luajit tests/bookorbit_undo_patch_test.lua /path/to/bookorbit.koplugin
luajit tests/hardcover_bookorbit_sync_test.lua /path/to/hardcoverapp.koplugin
```

Server unit validation and exact-base application checks are documented in
[VERIFICATION.md](VERIFICATION.md). No production credentials or server writes
are needed for those checks.

## Svenska

Det här är en **fristående, inofficiell samling valfria patchar**. Den ersätter
inte BookOrbit, KOReader eller Hardcover-pluginet. Inget driftsätts automatiskt.

- **Vill läsa [Lokalt] och EPUB-taggar** fungerar utan BookOrbit eller serverpatch.
- **Vill läsa [BookOrbit]** använder den vanliga anslutna BookOrbit-klienten och
  visar matchade böcker som redan finns på enheten. Ingen extra patch behövs.
- **Taggar via nätet** kräver det valfria server-API:t i
  [3.6.0-guiden](server-support/bookorbit-3.6.0/README.md). Det söker bara bland
  angivna, kopplade lokala böcker i alla profiler. Taggar och genrer blandas inte.
- **Ångra öppning** kräver både enhetspatchen och en kompatibel serverutökning.
  Det nya paketet gäller **exakt officiella BookOrbit 3.6.0** och kan kombineras
  med tagg-API:t på samma bas. Det är inte en universell patch för 3.2.0 eller
  senare. Det gamla kompilerade 3.2.0-överlägget är separat och får inte användas.
- **Hardcover-patchen** låter BookOrbit vara den enda automatiska skrivaren.
  Länkning, editioner, metadata och uttryckliga manuella val finns kvar i det
  separata Hardcover-pluginet. Gamla dubbla läsningar tas inte bort.

**Installera på enheten:** Säkerhetskopiera först. Avsluta KOReader, spara den
valda `.lua`-filen från länkarna ovan i KOReaders `patches/`-mapp och starta om.
Har du redan Ereader Patch Manager använder du dess vanliga katalog i stället.
Installera inte en andra kopia och ändra inte filnamnen.

**Viktigt för Ångra öppning:** Stöd finns bara för de granskade pluginversionerna
i kompatibilitetsfilen. Hantera alla skyddade/väntande öppningar och eventuell
serverstädning med patchen **innan** du tar bort eller stänger av något stöd.
Radera aldrig patchens sparade tillstånd för att kringgå ett stopp. Funktionen
gäller en oläst bok före första sidvändningen, inom 24 timmar, inte all läshistorik.

**Servern:** Be administratören följa rätt versionsspecifik guide, testa i en
isolerad miljö och verifiera databasbackup innan driftsättning. Den gamla
egna 3.2.0-databasen behöver en separat granskad uppgradering; den nya kontrollen
stoppar migrationskollisionen innan historiken ändras. Radera inga tabeller eller
hashar för att kringgå stoppet. 3.2.0-bilden får inte läggas ovanpå en nyare server. En OrbitUI-uppdatering
installerar aldrig serverstöd. Bevara upphovsrätt, licenser, modifieringsnotis
och fullständig källkod för den version som faktiskt körs. Inga produktionsdata
har ändrats genom att den här samlingen skapades.
