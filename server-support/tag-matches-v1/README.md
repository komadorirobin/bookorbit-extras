# Exact local-ID tag matching, API addition v1

**Original development-base artifact. For official BookOrbit 3.6.0, including
the supported combination with undo-opening, use the
[version-specific package](../bookorbit-3.6.0/README.md).**

Experimental, read-only BookOrbit server patch. Modified 2026-10-31; not an
official BookOrbit release. **Not deployed by OrbitUI or this repository.**

- Exact upstream base: `ba315c77182f0f28030140e342d93294cc512637`.
- Local implementation: `0cf7db16f1059049820f36dc0fe4022ea52a630b`.
- No schema change, dependency update or migration.
- Normal KOReader authentication and existing plugin client methods.

`GET /api/v1/koreader/plugin/catalog/tag-matches?ids=1,2&tag=...` accepts
1..200 positive safe-integer IDs and a literal 1..200-character tag. Invalid,
missing and unknown parameters fail validation. It returns `{ "bookIds": [1] }`
with `Cache-Control: no-store`. Exact case-sensitive matching is narrowed by
the caller's IDs, present books, accessible libraries and user content filters.
No cover/detail download, book metadata write or new sync owner. Device callers
must supply only current-account locally matched IDs and recheck actual files.

## Build and verify before deciding to deploy

Use a separate clean checkout, not your running installation. Set `EXTRAS` to
this collection's absolute directory. Node 24+ and pnpm 9+ are required by the
upstream project. The commands below do not deploy or run a database migration.

```sh
git clone https://github.com/bookorbit/bookorbit.git orbitui-tags-source
cd orbitui-tags-source
git switch --detach ba315c77182f0f28030140e342d93294cc512637
git status --short
git apply --check "$EXTRAS/server-support/tag-matches-v1/server.patch"
git apply "$EXTRAS/server-support/tag-matches-v1/server.patch"
pnpm install --frozen-lockfile
pnpm --dir server exec vitest run src/modules/koreader/dto/koreader-catalog-query.dto.test.ts src/modules/koreader/koreader-catalog.controller.test.ts src/modules/koreader/koreader-catalog.service.test.ts src/modules/opds/__tests__/opds-book.service.test.ts
pnpm --dir server type-check
pnpm --dir server lint:check
pnpm --dir server build
```

Inspect the diff and use the upstream build instructions to build a matching
server image from this complete patched source. Keep its existing volumes,
secrets, security settings, licenses and About page. Clearly identify the
modified version/date and make the complete source for your operated build
available as required by the upstream license/terms. See the root README.

Before production: verify backup restoration in a non-public test instance,
test authenticated access isolation, malformed query rejection, exact Unicode
tags, a linked local result and an inaccessible-library negative case. Do not
send real Hardcover writes during tests. Keep the previous known-working image
for an image-only rollback; there is no new migration to reverse here. Never
overwrite newer reading data with an old backup to undo a UI/API feature.

**Do not apply the old undo-opening 3.2.0 Docker overlay to this base.** That
overlay replaces compiled modules from a different version. A combined build
requires a separate reviewed rebase, source/migration audit and tests. Unknown
future versions are not automatically compatible even if `git apply` succeeds.

## Svenska

Det här är ett experimentellt, skrivskyddat API-tillägg på **exakt basrevisionen
ovan**, inte en allmän patch för senaste BookOrbit. Inga migrationer eller nya
beroenden behövs. Servern avgränsar angivna bok-ID:n med användarens bibliotek,
befintliga filer och innehållsfilter. Den kan inte själv bevisa vilka filer som
finns på läsplattan; klienten måste matcha och kontrollera dem.

Låt administratören använda en separat ren utcheckning, kontrollera `git apply
--check`, köra tester/typkontroll/lint/bygge och sedan testa en egen matchande
bild isolerat. Säkerhetskopiera och verifiera återställning före eventuell
driftsättning. Bevara licenser, Om-sida, modifieringsnotis och fullständig
källkod. Det här arbetet driftsätter ingenting. Använd **inte** det gamla
3.2.0-överlägget för Ångra öppning på den här versionen. Lokala EPUB-taggar i
OrbitUI kräver inget av detta.
