# Fresh Ride Mobile — SEO Plan

**Domain:** freshridemobile.shop · **Business:** mobile auto detailing, service-area business (SAB)
**Market:** Greater Houston metro · **GBP:** exists + verified · **Phone:** +1 346-489-2266

---

## 1. Where the site stands

Audited 2026-07-15. Single page, static HTML on Vercel. Design is good. SEO is near zero.

| Check | State | Impact |
|---|---|---|
| City names on page | **Zero.** Not one mention of Houston or any metro city | Fatal for local. Nothing to rank |
| Schema markup | **None.** No LocalBusiness, no FAQPage | No rich results, no entity for AI search |
| `robots.txt` | **404** | No crawler directives, no sitemap pointer |
| `sitemap.xml` | **404** | Discovery relies entirely on links |
| Canonical tag | **Missing** | Duplicate-URL risk (www, trailing slash) |
| OG / Twitter tags | **Missing** | Shared links render as a bare URL |
| Indexable pages | **1** | One page can rank for ~one thing |
| Title tag | "Auto Detailing That Comes to You" — no geo | Competes nationally, wins locally nowhere |
| Meta description | No city, no CTA | Low CTR |
| H1 | "Your car. Reset." — zero keywords | Pretty, invisible |
| Page speed | Static + Vercel CDN. Google Fonts render-blocking | Already strong, minor fix |
| Images | All have alt text | Fine |
| Accessibility | Skip link, aria labels, semantic HTML | Fine |

**The one-line diagnosis:** a mobile detailing site that never says where it details. Every other
problem is downstream of that.

## 2. Where the leads actually come from

For a SAB like detailing, the split is roughly:

1. **Map pack (GBP)** — the majority of calls. GBP is verified, so the lever here is proximity,
   reviews, categories, and posts. The website supports this; it does not replace it.
2. **Local organic** — "mobile detailing katy tx", "car detailing near me". This is what the city
   pages target, and where the site currently scores zero.
3. **AI search** (AI Overviews, ChatGPT, Perplexity) — increasingly answers "who details cars in
   Sugar Land". Fed by schema + clean, quotable facts. Currently invisible: no schema at all.

The website work below moves 2 and 3. GBP moves 1 and is tracked separately in section 7.

## 3. Keyword architecture

Head terms are metro-level; money terms are city + service. Pattern:

```
mobile detailing <city> tx        ← primary per city page
car detailing <city>              ← secondary
mobile car wash <city> tx         ← secondary
interior detailing <city>         ← service + city
mobile detailing near me          ← GBP + proximity, not a page
```

**City targets (phase 1 — six pages).** Chosen for vehicle density, driveway-heavy housing, and
household income, which is what mobile detailing converts on:

| City | Page | Why |
|---|---|---|
| Houston | `/houston` | Core metro, highest volume, hardest |
| Katy | `/katy` | Affluent, suburban, huge driveway stock |
| Sugar Land | `/sugar-land` | High income, low competition density |
| The Woodlands | `/the-woodlands` | Highest income in metro, premium detail demand |
| Cypress | `/cypress` | Fast growth, young families, two-car households |
| Pearland | `/pearland` | Dense suburb, underserved by mobile detailers |

**Phase 3 candidates** once the first six prove out: Spring, Missouri City, League City, Conroe,
Richmond, Friendswood.

Deliberately *not* building 12 pages on day one. Six real pages beat twelve thin ones — Google
treats near-duplicate location pages as doorway pages and can suppress the whole set.

## 4. Site structure

```
/                      Home — metro-wide, service hub, links to all city pages
/houston               City page
/katy                  City page
/sugar-land            City page
/the-woodlands         City page
/cypress               City page
/pearland              City page
/services/full-reset   Service page (phase 2)
/services/interior     Service page (phase 2)
/services/exterior     Service page (phase 2)
/pricing               Pricing page (phase 2) — high-intent, currently a phone-only black box
```

`cleanUrls: true` is already set in `vercel.json`, so `houston.html` serves at `/houston`. No build
step needed.

**Internal linking:** home links to all six city pages from a service-area section. Each city page
links up to home and sideways to its 2-3 nearest neighbors — real geographic adjacency, not a
mesh of every page to every page.

**Per-city differentiation (this is what keeps them out of doorway territory).** Each page must
carry at least four of these, written specific and true:

- Named neighborhoods and subdivisions served within that city
- A local landmark or corridor reference for the service radius
- City-specific conditions that affect detailing (Houston humidity and love bugs, Woodlands tree
  sap and pollen, Katy construction dust, coastal salt air toward Pearland/League City)
- Typical parking situation in that city's housing stock (HOA rules, apartment lots, driveways)
- Drive-time / scheduling note honest to that city
- FAQ answers rewritten per city, not copy-pasted

If a city page cannot honestly carry four, it does not get built. That is a hard gate.

## 5. Schema plan

| Page | Schema |
|---|---|
| Home | `AutoWash` (LocalBusiness subtype) + `areaServed` (all metro cities) + `FAQPage` + `WebSite` |
| City pages | `AutoWash` scoped to that `areaServed` city + city-specific `FAQPage` |
| Service pages (ph. 2) | `Service` with `provider` reference |

**SAB rule:** no `streetAddress` in the markup. A service-area business that publishes a home
address in schema while hiding it on GBP creates a NAP conflict. Use `areaServed` + `geo` +
`geoRadius` instead. NAP consistency across site, GBP, and citations = name, phone, city only.

## 5b. What we are deliberately NOT doing

Recording the rejections matters as much as the plan — otherwise they get re-proposed in six months.

**Programmatic SEO (PSEO) — rejected, and it would actively hurt.** PSEO generates pages at scale
from a data source. It earns its keep when the data has real variation: distinct inventory per zip,
distinct specs per product. This business has one service line and roughly twelve real cities. The
templated version — `[city] × [service] × [vehicle type]` — produces a few hundred pages that are
the same page with a word swapped. Google treats that as a doorway farm and can suppress the
**entire set**, including the good city pages. The honest ceiling here is ~12 city pages and ~4
service pages. That is a writing job, not a PSEO job.

**A /houston page — rejected.** The homepage already targets "mobile detailing Houston" with that
exact title. A second page on the same term cannibalizes it. The homepage IS the Houston page.

**More than 6 city pages before the first 5 prove out — deferred.** Impressions in Search Console
decide city 6 onward, not optimism.

**Heavy GEO investment — scoped down deliberately.** See below.

## 5c. GEO (AI search) — right-sized

Mostly already shipped, because for a local business the useful parts of GEO are the same parts as
normal technical SEO:

| Done | What it buys |
|---|---|
| `AutoWash` + `FAQPage` + `WebSite` JSON-LD | The structured facts AI engines actually parse |
| AI crawlers explicitly allowed in `robots.txt` | GPTBot, PerplexityBot, ClaudeBot, Google-Extended |
| Answer-shaped FAQ copy, question-as-heading | Passage-level citability |
| Named neighborhoods, corridors, real conditions | Specific, quotable facts a model can lift |

| Not done | Priority |
|---|---|
| `llms.txt` at the root | Low — cheap, ~15 min, do it with the next batch |
| First-party photos and named local proof | Medium — real E-E-A-T, blocked on the business |
| Brand mentions off-site (citations, directories) | Medium — feeds AI and local both |

**Honest scope:** GEO is a *small* lever for a mobile detailer. When someone asks ChatGPT "who
details cars in Katy," the answer leans on Google Maps and review counts, not this site's HTML. GEO
is worth about half an hour here. It is a major program for SaaS and B2B — not for this. Don't let
the acronym pull budget away from reviews.

## 6. Technical fixes

- `robots.txt` — allow all, explicitly allow `GPTBot`, `PerplexityBot`, `ClaudeBot`,
  `Google-Extended` (AI search visibility is opt-out; leaving it default means leaving it on, but
  being explicit prevents a future accidental block)
- `sitemap.xml` — all seven pages, referenced from robots.txt
- Canonical tag on every page, self-referencing, absolute, non-www
- OG + Twitter card tags with a real preview image
- Self-host the two Google Fonts, or `preload` them — currently two render-blocking round trips to
  a third-party origin on every page load
- Keep `X-Content-Type-Options` / `Referrer-Policy` headers already in `vercel.json`

## 7. GBP track (runs parallel, higher ROI than the site)

The site work does not touch the map pack. These do:

1. **Categories** — primary `Car detailing service`. Secondary: `Car wash`, `Auto restoration
   service`. Primary category is the single strongest map-pack ranking factor after proximity.
2. **Service area** — set to the metro cities above, not a blanket radius.
3. **Hide the address** — required for SAB. A visible address at a residence triggers suspension.
4. **Reviews** — the compounding lever. Target 1-2/week, every week, asked for on-site at handoff
   while the customer is looking at the finished car. Reply to every one within 24h. Reviews that
   name the city and the service ("detailed my truck in Katy") feed local relevance directly.
5. **Photos** — 2-3/week, geotagged, real work not stock. Before/after pairs perform best.
6. **Posts** — weekly. Low direct ranking value, real CTR value.
7. **Messaging + booking** — on, since the whole site funnels to a phone call.

## 7b. Priority order — everything not yet done, ranked by real impact

If only one thing on this list ever gets done, make it the first row.

| # | Lever | Impact | Who | Effort |
|---|---|---|---|---|
| 1 | **Reviews — 1-2/week, every week, forever** | Huge. Drives the map pack, which is most of the leads | **Sumit only** | Ask at every handoff |
| 2 | Pricing page (ranges, not "call for pricing") | High. Recovers visitors who want a number before dialing | Claude | ~1 hr |
| 3 | First-party before/after photos | High. E-E-A-T + GBP. Stock cannot fake it | Sumit shoots, Claude places | Ongoing |
| 4 | GBP categories + service area + hidden address | High, one-time, suspension-critical | Sumit | 15 min |
| 5 | Citations: Yelp, Apple Business Connect, Bing Places | Medium. NAP consistency feeds local + AI | Claude preps, Sumit submits | ~1 hr |
| 6 | 3 service pages (`Service` schema) | Medium | Claude | ~1 hr |
| 7 | `llms.txt` + GEO polish | Low-medium | Claude | 15 min |
| 8 | Self-host fonts | Low. Removes 2 render-blocking third-party requests | Claude | 20 min |
| 9 | Cities 6-12 | Low until the first 5 show impressions | Claude | Later |
| — | PSEO | **Negative.** See 5b | — | Don't |

Rows 1, 3, 4 are the highest-impact items on the page and none of them are code. That is the honest
shape of local SEO for a service business: the website is table stakes, the profile and the reviews
are the engine.

## 8. Roadmap

**Phase 1 — Foundation — SHIPPED 2026-07-15, live in production**
- [x] Homepage geo signals: title, meta, H1 keyword line, service-area section (0 → 13 city mentions)
- [x] AutoWash + WebSite + FAQPage schema, canonical, OG/Twitter tags
- [x] `robots.txt` + `sitemap.xml` (both were 404)
- [x] Five city pages with differentiated content, gated by `build_pages.py::check()`
- [x] Sitemap submitted in Search Console 2026-07-15 (property verified same day)

**Phase 2 — Conversion + depth (weeks 2-6)**
- Pricing page — the biggest conversion gap. "Call for pricing" loses every visitor who wants a
  number before they dial. Ranges beat silence.
- Three service pages with `Service` schema
- Review engine running: ask at every handoff, reply within 24h
- Real before/after gallery replacing stock imagery — first-party photos are the E-E-A-T signal
  that stock cannot fake
- Self-host fonts

**Phase 3 — Scale (weeks 7-16)**
- Cities 7-12 if the first six show impressions in Search Console
- Local content: "how often to detail in Houston humidity", "protecting paint from Texas sun" —
  targets informational queries and feeds AI citations
- Citation build: Yelp, Apple Business Connect, Bing Places, Nextdoor, local directories. NAP
  identical everywhere.
- Fleet / commercial page if that's a segment worth pursuing

**Phase 4 — Authority (months 5-12)**
- Geo-grid rank tracking to see where the map pack actually shows the business
- Partnerships: apartment complexes, dealerships, office parks — links and referrals in one
- Expand the city set based on what's ranking, not what's hoped

## 9. KPIs

Baseline is 2026-07-15, effectively zero — the property was verified today and the site has never
been crawlable in a meaningful way.

| Metric | Baseline | 3 mo | 6 mo | 12 mo |
|---|---|---|---|---|
| Indexed pages | 1 | 7 | 12 | 20+ |
| Organic clicks / mo | ~0 | 40-80 | 150-300 | 400-800 |
| Ranking keywords | ~0 | 25-50 | 80-150 | 200-400 |
| City pages in top 10 | 0 | 2-3 | 4-5 | 6+ |
| GBP reviews | TBD | +20 | +50 | +100 |
| Map pack top 3 (home city) | TBD | 1-2 cities | 3-4 cities | 5+ cities |
| Core Web Vitals | passing | passing | passing | passing |

Ranges are ranges on purpose. Anyone quoting a single number for month-3 organic traffic on a
3-day-old domain is guessing with false precision. Domain age is the constraint nothing accelerates.

**Honest expectation setting:** the domain registered ~3 days ago. New domains do not rank fast
regardless of execution. Months 1-3 are GBP and reviews carrying the leads while the site builds
crawl history. The site work compounds from month 4 on. Anyone promising page 1 in 30 days on a
new domain is selling something.

## 10. Risks

| Risk | Mitigation |
|---|---|
| Six city pages read as doorway pages | The four-signal differentiation gate in section 4. No gate pass, no page |
| GBP suspension (SAB with visible address) | Address hidden, no `streetAddress` in schema, NAP is name/phone/city only |
| New domain, slow start | GBP + reviews carry months 1-3. Site compounds after |
| Stock imagery undercuts trust and E-E-A-T | Replace with first-party before/after in phase 2 |
| "Call for pricing" leaks high-intent traffic | Pricing page with ranges, phase 2 |
| Thin content if the business can't supply local detail | Pages get written from real service history, not invented. Fewer real pages > more fake ones |
