# Integration extras for BookOrbit and KOReader

An independent, optional patch collection by komadorirobin. Not an official
BookOrbit, KOReader or Hardcover release. No account credentials are included.
Nothing here deploys a server automatically.

**Local device follow-up, not published (2026-11-10):** the working source adds
reviewed Undo compatibility with the official KOReader plugin **2.2.0**, from
BookOrbit 3.7.0 `6f8f5f48`. All earlier tested device profiles remain supported.
The public 0.3.0 release assets have not been replaced. This is not a 3.7.0
server port: all server patches below still require their exact existing bases.
No server deployment, reading-state migration or permission change is needed
for this device compatibility change. See [verification](VERIFICATION.md).

Collection 0.3.0: `server-support/bookorbit-3.6.0/status.patch`
adds authenticated, bounded GET-only reading-status reads for OrbitUI. It
requires no database migration. Use the exact-base source helper's explicit
`--features status` or `--features all`; `both` keeps its existing meaning.
The default `both` still means undo and tags only. Server installation is
separate from an OrbitUI/device update and requires an administrator.

Version 0.3.0: `status.patch` hämtar lässtatus och ändringstid för
redan kopplade böcker, med autentisering och högst 200 ID:n per anrop. Ingen
databasmigrering krävs. Välj uttryckligen `--features status` eller `all` i
källkodshjälparen. Standardvalet `both` betyder fortfarande bara ångring och
taggar. Servern installeras separat av administratören, inte via OrbitUI.

[Collection 0.3.0 is published](https://github.com/komadorirobin/bookorbit-extras/releases/tag/v0.3.0).
Its assets include checksums and two distinct complete-source archives: the
portable exact-3.6.0 `all-source` package (generic undo migration 0132), and
the separately reviewed **Littex** build preserving one existing installation's
legacy 0101 undo history. The latter is not a generic database upgrade.
The user-approved Littex installation now serves read-statuses v1; this does
not deploy it for other users or turn on OrbitUI's importer automatically.

[Version 0.3.0 är publicerad](https://github.com/komadorirobin/bookorbit-extras/releases/tag/v0.3.0)
med kontrollsummor och full källkod. Det generella arkivet använder 0132;
Littex-arkivet bevarar en separat granskad egen 0101-historik och är inte en
allmän uppgradering. Det godkända Littex-bygget är driftsatt, men andras servrar
och läsarens avstängda standardval påverkas inte.

[Svenska](#svenska) | [Compatibility and exact sources](compatibility.json)
| [Device patches](#device-installation) | [BookOrbit 3.6.0 server extras](server-support/bookorbit-3.6.0/README.md)
| [Legacy 3.2.0 overlay](server-support/bookorbit-undo-opening/README.md)

## What needs what?

| Feature | On the reader | On your server |
| --- | --- | --- |
| Want to read [Local] / local EPUB tags | OrbitUI; ordinary local files | Nothing. No account or BookOrbit patch. |
| Want to read [BookOrbit] | Connected BookOrbit KOReader plugin and OrbitUI | Normal BookOrbit Want to Read API. No extras patch. Only matched local books appear. |
| Online BookOrbit tag matches | OrbitUI Beta 22 or newer; connected account-scoped BookOrbit plugin | Optional **tag-matches v1** patch for exact official **3.6.0**. Read-only, linked local results across profiles, batches of 200 IDs. |
| Import reading status | OrbitUI Beta 28 or newer; connected BookOrbit plugin; explicit opt-in under Integrations > BookOrbit | Optional **read-statuses v1** patch for exact official **3.6.0**. GET-only, 200 supplied IDs, canonical status/finish timestamps, no migration. |
| Undo accidental opening | `2-bookorbit-undo-opening.lua`, compatible BookOrbit plugin | **Undo-opening v1 port for official 3.6.0**, migration **0132**. Use the new complete-source build, not the old compiled overlay. |
| One automatic Hardcover writer | `2-hardcover-bookorbit-sync.lua` plus the separate Hardcover plugin, with BookOrbit as your chosen automatic writer | Enable BookOrbit's normal Hardcover integration. No extra server patch for this feature. |

The new [3.6.0 package](server-support/bookorbit-3.6.0/README.md) targets exact
official release `a96ff0c`, the latest stable checked on 2026-10-31. Undo and tags
and status can be selected individually or together on that base. This does **not** mean
3.2.0+, future releases or the moving development branch. An OrbitUI update
does not install server extensions. This repository never deploys automatically.

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
1.5.5, 2.0.0, 2.1.0 and 2.2.0; later unreviewed source can fail its guard even when a
version number looks similar. See exact commits in `compatibility.json`.

Use the patch's BookOrbit menu/gesture action to commit or undo an opening.
Resolve all protected/pending openings and pending server cleanup **before**
disabling/removing either half. Do not delete `bookorbit_openings` settings or
restore stale progress files to bypass a hold. Unsupported server routes are
not the same as tested server support; see the server guide for fallback and
reconciliation. Never test against real Hardcover reading records.

When the compatibility guard pauses initialization, BookOrbit's menu can also
be absent until the compatible patch is installed and KOReader restarted. The
guard does not remove plugin files or credentials. Do not disable the patch or
delete saved state to force the plugin to load.

**Svenska:** Den lokala kompatibilitetsuppdateringen stöder plugin 2.2.0 utan att
ändra servern eller sparad ångring. När säkerhetsspärren stoppar pluginet före
start kan BookOrbit-menyn försvinna. Behåll patchen och dess tillstånd; lösningen
är den granskade kompatibilitetsuppdateringen och därefter omstart av KOReader.

Reloading the same unchanged cover, including KOReader's close/reopen after a
font/layout change, preserves Undo and the original operation ID, unread
snapshot and 24-hour deadline. A page turn, book switch, changed reading data
or annotations still ends eligibility. The device-side reload fix needs no
server update or migration and does not reopen committed readings or rewrite
existing history.

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

Collection format **0.3.0**, updated 2026-11-01. Adds the optional read-statuses
API and exact-source helper selections `status` and `all`. The device Undo
patch still retains provisional openings across unchanged same-book reloads;
both device files and the previous undo/tag patches are unchanged. Exact Ereader source and device checksums
are pinned in `compatibility.json`. The server undo extension has been ported to
official 3.6.0 and the optional tag API rebased to that same source. The original
development-base tag implementation `0cf7db1` is retained separately. Full revisions,
component versions and SHA-256 values are in `compatibility.json`. The patch
repository does not bundle an upstream application or private configuration.
The release's explicitly named complete-source archives additionally contain
the pinned upstream application's original source/assets/notices, with the
selected modifications. No private configuration, credentials or backups are
included in those archives.

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
integration tests also use a disposable local PostgreSQL database. Those suites
alone do not validate physical reader behaviour or a production deployment;
the separately authorized Littex deployment receipt is in VERIFICATION. Run from
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
- **Hämta lässtatus** kräver OrbitUI Beta 28 eller senare, aktivering under
  Integrationer > BookOrbit och servertillägget `read-statuses v1`. Högst 200
  angivna ID:n per GET-anrop; ingen migrering, sidpositionssynk eller skrivning
  till servern. Öppna böcker, väntande ångring och nyare/osäkra lokala ändringar
  skyddas av klienten. Funktionen är avstängd som standard.
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

Omladdning av samma oförändrade omslag behåller ångramöjligheten, även när
KOReader stänger och öppnar boken igen efter en layoutändring. Ursprunglig
öppning och tidsgräns behålls; sidvändning, bokbyte eller ändrad läsposition
eller anteckningar avslutar fortfarande ångrafönstret. Rättningen i
enhetspatchen kräver ingen serveruppdatering och ändrar inte befintlig historik
eller redan bekräftade öppningar.

**Servern:** Be administratören följa rätt versionsspecifik guide, testa i en
isolerad miljö och verifiera databasbackup innan driftsättning. Den gamla
egna 3.2.0-databasen behöver en separat granskad uppgradering; den nya kontrollen
stoppar migrationskollisionen innan historiken ändras. Radera inga tabeller eller
hashar för att kringgå stoppet. 3.2.0-bilden får inte läggas ovanpå en nyare server. En OrbitUI-uppdatering
installerar aldrig serverstöd. Bevara upphovsrätt, licenser, modifieringsnotis
och fullständig källkod för den version som faktiskt körs. Inga produktionsdata
har ändrats genom att den här samlingen skapades.
