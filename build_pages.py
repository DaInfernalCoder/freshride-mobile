#!/usr/bin/env python3
"""Generate the city landing pages and sitemap.xml.

Run after editing CITIES:  python3 build_pages.py
Output HTML is committed — Vercel serves it statically, there is no build step.

Every city MUST carry real, city-specific content in `conditions`, `parking`, `hoods`
and `faq`. Near-duplicate location pages get treated as doorway pages and can drag
down the whole set, so a city with nothing true to say does not get a page.
"""

import json
import os

SITE = "https://freshridemobile.shop"
PHONE_DISPLAY = "+1 346-489-2266"
PHONE_HREF = "tel:+13464892266"
PHONE_SCHEMA = "+1-346-489-2266"

# Houston itself is deliberately NOT here — the homepage targets "mobile detailing Houston".
# A /houston page would carry the same title and intent and cannibalize it.
CITIES = [
    {
        "slug": "katy",
        "name": "Katy",
        "lat": 29.7858,
        "lon": -95.8244,
        "wiki": "https://en.wikipedia.org/wiki/Katy,_Texas",
        "blurb": "Cinco Ranch, Cross Creek Ranch, Grand Lakes and the Energy Corridor commute.",
        "hoods": ["Cinco Ranch", "Cross Creek Ranch", "Grand Lakes", "Seven Meadows", "Firethorne", "Falcon Ranch", "Katy Old Town"],
        "corridor": "Along I-10 and the Grand Parkway, from Old Town out to Cross Creek",
        "conditions": "Katy has two things working against clean paint. The first is construction — the area is still "
                      "being built, and fine dust from active sites settles on everything parked outside. The second is "
                      "sprinkler water. Katy's water is hard, and lawn sprinklers throwing it onto a car door leave "
                      "mineral spots that a regular wash will not lift once they've sat in the sun.",
        "parking": "Katy driveways are wide and that makes this easy. Most of our Katy work is a straightforward "
                   "driveway detail. The one thing worth checking is your HOA — some Katy neighborhoods have rules "
                   "about work vehicles or driveway water use, and it's better to know before we're parked out front.",
        "timing": "Katy runs on the Energy Corridor commute, and it shapes how people book us. Most Katy customers "
                  "leave the car at the house and have us come mid-day while they're at work, or they have us meet the "
                  "car at the office lot instead. Either works. Mid-week openings are easiest — Katy Saturdays fill "
                  "up first.",
        "faq": [
            ("Do you come out to Cinco Ranch and Cross Creek Ranch?",
             "Yes, both, along with Grand Lakes, Seven Meadows, Firethorne and the rest of Katy. Gated sections just "
             "need gate access sorted before we arrive."),
            ("Can you remove the hard water spots from my sprinklers?",
             "In most cases, yes. Sprinkler mineral spotting is one of the most common things we're called for in Katy. "
             "If it's been baking for months it can etch the clear coat, so mention it on the call and we'll set "
             "expectations honestly."),
            ("My HOA has rules about washing in the driveway. Is that a problem?",
             "Tell us the rule and we'll work with it. We bring our own setup and we're not looking to get you a letter "
             "from the HOA over a clean car."),
        ],
        "neighbors": ["cypress", "sugar-land"],
    },
    {
        "slug": "sugar-land",
        "name": "Sugar Land",
        "lat": 29.6197,
        "lon": -95.6349,
        "wiki": "https://en.wikipedia.org/wiki/Sugar_Land,_Texas",
        "blurb": "Riverstone, First Colony, Telfair, New Territory and Greatwood.",
        "hoods": ["Riverstone", "First Colony", "Telfair", "New Territory", "Greatwood", "Avalon", "Sugar Creek"],
        "corridor": "Around US-59 and Sugar Land Town Square, out through Riverstone and Greatwood",
        "conditions": "Sugar Land is manicured, and the irrigation that keeps it that way is what marks up the cars. "
                      "Hard water from sprinklers spots doors and lower panels. The mature tree cover through First "
                      "Colony and Sugar Creek adds the other half: sap, pollen, and bird droppings that etch a clear "
                      "coat if they sit through a hot week.",
        "parking": "Most Sugar Land homes have the driveway space this needs, and a good share of the neighborhoods are "
                   "gated. Gate access is the only real coordination — get us on the guest list or meet us at the gate "
                   "and the rest is routine.",
        "timing": "Sugar Land is a straight run down 59 for us and books comfortably mid-week. Weekends go first here — "
                  "if a Saturday morning is what you need, call early in the week rather than Thursday. Gated "
                  "neighborhoods need a few extra minutes at the front, so we build that into the window we give you.",
        "faq": [
            ("Do you service gated communities like Riverstone and Telfair?",
             "Yes. Gated is normal for Sugar Land. Just add us at the gate or meet us there — we can't get in without it."),
            ("Can you get tree sap off without damaging the paint?",
             "Usually. Fresh sap comes off cleanly. Sap that's sat through a Texas summer can etch into the clear coat, "
             "and at that point it's a paint correction question rather than a wash question. We'll look and tell you "
             "which one you're dealing with."),
            ("Do you detail at the office parks around Town Square?",
             "Yes, if the lot allows it. Plenty of Sugar Land customers have us come to the office instead of the house. "
             "We confirm the lot is fine with it first."),
        ],
        "neighbors": ["katy", "pearland"],
    },
    {
        "slug": "the-woodlands",
        "name": "The Woodlands",
        "lat": 30.1658,
        "lon": -95.4613,
        "wiki": "https://en.wikipedia.org/wiki/The_Woodlands,_Texas",
        "blurb": "Creekside Park, Sterling Ridge, Alden Bridge and Grogan's Mill.",
        "hoods": ["Creekside Park", "Sterling Ridge", "Alden Bridge", "Grogan's Mill", "Panther Creek", "Cochran's Crossing", "Indian Springs"],
        "corridor": "Up I-45 through Town Center, Hughes Landing and out to Creekside",
        "conditions": "The Woodlands is built under a pine canopy, and that canopy is hard on paint. Pine sap drips onto "
                      "roofs and hoods and hardens into spots that a normal wash slides right past. Needles collect in "
                      "cowls and door channels. Shaded driveways stay damp, and birds in mature trees do the rest. It's "
                      "the most tree-driven detailing market in the metro, and it needs a different approach than an "
                      "open suburban driveway.",
        "parking": "Driveways here are generous and shaded, which actually helps — we're not fighting direct sun while "
                   "we work. Several villages are gated or have narrow wooded approaches, so we confirm access when we "
                   "book.",
        "timing": "The Woodlands is the north end of our range, up I-45. We batch north-side bookings into the same "
                  "days rather than making the drive for one car, so a little flexibility on the day gets you in "
                  "noticeably sooner. Tell us which days work and we'll fit you into the next Woodlands run.",
        "faq": [
            ("Can you get pine sap off my roof and hood?",
             "Yes, that's the number one thing we're called for in The Woodlands. Fresh sap lifts cleanly. Sap that's "
             "been hardening for months may have etched the clear coat underneath, and we'll tell you what we see "
             "before we start."),
            ("Do you come out to Creekside Park and Sterling Ridge?",
             "Yes, along with Alden Bridge, Grogan's Mill, Panther Creek and the rest of the villages."),
            ("My driveway is fully shaded. Is that a problem?",
             "It's the opposite of a problem. Shade means the panels stay cool and products don't flash off before we "
             "can work them. Shaded driveways are the best case."),
        ],
        "neighbors": ["cypress", "katy"],
    },
    {
        "slug": "cypress",
        "name": "Cypress",
        "lat": 29.9691,
        "lon": -95.6972,
        "wiki": "https://en.wikipedia.org/wiki/Cypress,_Texas",
        "blurb": "Bridgeland, Towne Lake, Fairfield and Coles Crossing.",
        "hoods": ["Bridgeland", "Towne Lake", "Fairfield", "Coles Crossing", "Blackhorse Ranch", "Longwood", "Cypress Creek Lakes"],
        "corridor": "Along the 290 corridor and the Grand Parkway, through Bridgeland and Towne Lake",
        "conditions": "Cypress is still going up, and it shows on the cars. Bridgeland and the newer Grand Parkway "
                      "sections have active construction throwing fine dust that settles into a gritty film — the kind "
                      "that scratches if you wipe it dry. The lakes at Towne Lake and Bridgeland bring the other half: "
                      "bugs on the front end and a pollen load in spring that a quick rinse doesn't touch.",
        "parking": "Cypress driveways are big and the vehicles are bigger — this is three-row SUV and pickup country, "
                   "and a lot of them are hauling kids, dogs and sports gear. Interiors here take the most work in the "
                   "metro, and that's usually what people call about.",
        "timing": "Cypress pairs with our north-side days, so it shares a schedule with The Woodlands run. Mid-week "
                  "openings are the easiest to get. Heavy interiors — and Cypress has a lot of them — need a longer "
                  "window than a standard detail, so we'd rather book you the right amount of time than rush it.",
        "faq": [
            ("Do you detail in Bridgeland and Towne Lake?",
             "Yes, plus Fairfield, Coles Crossing, Blackhorse Ranch and the rest of Cypress."),
            ("My SUV interior is destroyed — kids, dogs, sports gear. Can you handle it?",
             "That's most of our Cypress work. Mention pet hair, spills, and problem spots when you call so we plan "
             "the right amount of time. Heavy interiors take longer and we'd rather quote that honestly up front."),
            ("There's construction dust all over my car constantly. Is detailing even worth it?",
             "Fair question. A detail resets it, but if you're parked next to an active site it will come back. A "
             "protective finish makes the next dust layer rinse off instead of grinding in, and that's the part that "
             "actually helps between details."),
        ],
        "neighbors": ["katy", "the-woodlands"],
    },
    {
        "slug": "pearland",
        "name": "Pearland",
        "lat": 29.5636,
        "lon": -95.2860,
        "wiki": "https://en.wikipedia.org/wiki/Pearland,_Texas",
        "blurb": "Shadow Creek Ranch, Silverlake, Pearland Parkway and the 288 corridor.",
        "hoods": ["Shadow Creek Ranch", "Silverlake", "Riverstone Ranch", "Southdown", "Pearland Parkway", "Southern Trails"],
        "corridor": "Down the 288 corridor and along Pearland Parkway, out to Shadow Creek",
        "conditions": "Pearland sits closer to the coast, and the air carries it. Salt in the humidity works on trim, "
                      "wheels and any exposed metal faster than it does further inland, and the storms coming up from "
                      "the Gulf leave a dirty film that dries into spots within hours. It's a wetter, saltier "
                      "environment than the west side of the metro and it wears cars differently.",
        "parking": "Standard suburban driveways through Shadow Creek and Silverlake, which is the easy case for us. "
                   "Plenty of Pearland customers commute up 288 to the Medical Center, so we often detail at the house "
                   "during the day while the car — and the driveway — are free.",
        "timing": "Pearland is a straight run down 288 for us, so same-week is normal and next-day is common. The thing "
                  "worth planning around here is weather — Gulf storms roll in fast, and if the forecast would "
                  "compromise the finish we'd rather move you than hand back a car we're not happy with.",
        "faq": [
            ("Do you come out to Shadow Creek Ranch and Silverlake?",
             "Yes, along with Riverstone Ranch, Southdown, Southern Trails and the rest of Pearland."),
            ("Does being closer to the coast actually affect my car?",
             "It does. Salt in the humid air works on wheels, trim and exposed metal faster here than it does out west. "
             "Rinsing the underside and wheels more often is the single most useful habit if you're parked outside in "
             "Pearland."),
            ("Can you detail at my house while I'm at work in the Medical Center?",
             "Yes, that's a common Pearland setup. Leave the car in the driveway, we handle it, you come home to it "
             "done. We'll confirm access to the vehicle when you call."),
        ],
        "neighbors": ["sugar-land", "katy"],
    },
]

BY_SLUG = {c["slug"]: c for c in CITIES}


def nav(active):
    links = "".join(
        f'<a href="/{c["slug"]}"{" aria-current=\"page\"" if c["slug"] == active else ""}>{c["name"]}</a>'
        for c in CITIES
    )
    return links


def schema(c):
    faq = [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in c["faq"]
    ]
    return json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "AutoWash",
                "@id": f"{SITE}/#business",
                "name": "Fresh Ride Mobile",
                "url": f"{SITE}/",
                "telephone": PHONE_SCHEMA,
                "image": f"{SITE}/assets/hero-car.jpg",
                "priceRange": "$$",
                # SAB: locality only, never streetAddress — a published address conflicts
                # with the hidden address on the Google Business Profile.
                "address": {"@type": "PostalAddress", "addressLocality": "Houston",
                            "addressRegion": "TX", "addressCountry": "US"},
                "geo": {"@type": "GeoCoordinates", "latitude": c["lat"], "longitude": c["lon"]},
                "areaServed": {"@type": "City", "name": c["name"],
                               **({"sameAs": c["wiki"]} if c.get("wiki") else {})},
            },
            {
                "@type": "WebPage",
                "@id": f"{SITE}/{c['slug']}#webpage",
                "url": f"{SITE}/{c['slug']}",
                "name": f"Mobile Auto Detailing in {c['name']}, TX | Fresh Ride Mobile",
                "about": {"@id": f"{SITE}/#business"},
                "isPartOf": {"@id": f"{SITE}/#website"},
            },
            {
                "@type": "FAQPage",
                "@id": f"{SITE}/{c['slug']}#faq",
                "mainEntity": faq,
            },
        ],
    }, indent=2)


def page(c):
    title = f"Mobile Auto Detailing in {c['name']}, TX | Fresh Ride Mobile"
    desc = (f"Mobile auto detailing in {c['name']}, TX. Interior and exterior detailing at your driveway or "
            f"workplace, including {', '.join(c['hoods'][:3])}. Call {PHONE_DISPLAY}.")
    url = f"{SITE}/{c['slug']}"

    hoods = "".join(f"<span>{h}</span>" for h in c["hoods"])
    faqs = "".join(
        f"<details><summary>{q}<span>+</span></summary><p>{a}</p></details>"
        for q, a in c["faq"]
    )
    neighbors = "".join(
        f'<a class="area-card" href="/{n}"><h3>{BY_SLUG[n]["name"]}</h3>'
        f'<p>{BY_SLUG[n]["blurb"]}</p>'
        f'<span>Detailing in {BY_SLUG[n]["name"]} <i aria-hidden="true">↗</i></span></a>'
        for n in c["neighbors"]
    )

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="theme-color" content="#071722" />
    <meta name="description" content="{desc}" />
    <link rel="canonical" href="{url}" />
    <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="/styles.css" />
    <link rel="stylesheet" href="/header-contrast.css" />
    <title>{title}</title>

    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Fresh Ride Mobile" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{SITE}/assets/hero-car.jpg" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{desc}" />
    <meta name="twitter:image" content="{SITE}/assets/hero-car.jpg" />

    <script type="application/ld+json">
{schema(c)}
    </script>
  </head>
  <body>
    <a class="skip-link" href="#main">Skip to content</a>
    <header class="site-header" id="top">
      <a class="brand" href="/" aria-label="Fresh Ride Mobile home">
        <svg class="brand-mark" viewBox="0 0 46 46" aria-hidden="true"><path d="M23 3 41 13v20L23 43 5 33V13L23 3Z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M13 28c5-1 6-10 16-10 3 0 5 1 7 3-3 0-5 1-7 3-4 4-8 7-16 4Z" fill="currentColor"/><circle cx="31.5" cy="14.5" r="2.5" fill="#b97745"/></svg>
        <span>Fresh Ride <b>Mobile</b></span>
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span><span class="sr-only">Open menu</span></button>
      <nav id="site-nav" aria-label="Main navigation">
        <a href="/#services">Services</a>
        <a href="/#process">How it works</a>
        <a href="/#areas">Areas</a>
        <a href="/#faq">FAQ</a>
        <a href="https://cal.com/sumitdatta/auto-detail-service">Book online</a>
      </nav>
      <a class="button button-small header-cta button-call" href="{PHONE_HREF}">Call {PHONE_DISPLAY}</a>
    </header>

    <main id="main">
      <section class="hero hero-city">
        <div class="hero-media" role="img" aria-label="A freshly detailed car being washed in {c['name']}, Texas"></div>
        <div class="clean-pass" aria-hidden="true"></div>
        <div class="hero-shade" aria-hidden="true"></div>
        <div class="hero-content">
          <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">/</span> {c['name']}</nav>
          <p class="eyebrow"><span></span> Mobile auto detailing · {c['name']}, TX</p>
          <h1><span class="h1-geo">Mobile auto detailing in {c['name']}, TX</span>Your car.<br /><em>Reset.</em></h1>
          <p class="hero-copy">{c['blurb']} We bring professional interior and exterior detailing to your driveway or workplace — you keep your day, we bring back the shine.</p>
          <div class="hero-actions">
            <a class="button button-call" href="{PHONE_HREF}">Call {PHONE_DISPLAY} <span aria-hidden="true">↗</span></a>
            <a class="button button-book" href="https://cal.com/sumitdatta/auto-detail-service">Book online <span aria-hidden="true">↗</span></a>
            <a class="text-link" href="#local">Detailing in {c['name']} <span aria-hidden="true">↓</span></a>
          </div>
        </div>
        <div class="hero-proof" aria-label="Service highlights">
          <div><strong>01</strong><span>We come<br />to you</span></div>
          <div><strong>02</strong><span>Interior +<br />exterior</span></div>
          <div><strong>03</strong><span>Careful,<br />pro finish</span></div>
        </div>
      </section>

      <section class="intro section" id="local">
        <p class="section-kicker">Detailing in {c['name']}</p>
        <div class="intro-grid">
          <h2>What {c['name']} does to a car.</h2>
          <div>
            <p class="lead">{c['conditions']}</p>
            <div class="micro-list">{hoods}</div>
          </div>
        </div>
      </section>

      <section class="areas section">
        <div class="section-head">
          <div><p class="section-kicker">On the ground</p><h2>Where we work in {c['name']}.</h2></div>
          <p>{c['corridor']}. If you're nearby and not sure we reach you, call and ask — the answer is usually yes.</p>
        </div>
        <div class="local-notes">
          <article><h3>Parking and access</h3><p>{c['parking']}</p></article>
          <article><h3>Scheduling</h3><p>{c['timing']}</p></article>
        </div>
      </section>

      <section class="services section" id="services">
        <div class="section-head">
          <div><p class="section-kicker">Choose your reset</p><h2>Built around what your car needs.</h2></div>
          <p>Every vehicle is different. Choose a starting point and we'll shape the final quote around its size and condition.</p>
        </div>
        <div class="service-grid">
          <article class="service-card service-featured">
            <div class="service-image image-exterior"></div>
            <div class="service-body"><span class="service-tag">Most complete</span><h3>Full Reset</h3><p>A thorough interior and exterior refresh for {c['name']} vehicles that need the whole treatment.</p><ul><li>Detailed exterior wash</li><li>Wheel and tire clean</li><li>Deep interior vacuum</li><li>Surfaces and glass</li></ul><a href="{PHONE_HREF}">Call to book <span>↗</span></a></div>
          </article>
          <article class="service-card">
            <div class="service-image image-interior"></div>
            <div class="service-body"><span class="service-tag">Inside</span><h3>Interior Reset</h3><p>Dust, crumbs, daily buildup—cleared out with close attention to the spaces you use most.</p><ul><li>Thorough vacuum</li><li>Dash, console and trim</li><li>Interior glass</li><li>Spot cleaning as needed</li></ul><a href="{PHONE_HREF}">Call to book <span>↗</span></a></div>
          </article>
          <article class="service-card">
            <div class="service-image image-finish"></div>
            <div class="service-body"><span class="service-tag">Outside</span><h3>Exterior Refresh</h3><p>A careful hand wash and finish that restores gloss without the rushed tunnel-wash treatment.</p><ul><li>Hand wash and dry</li><li>Wheels and tires</li><li>Exterior glass</li><li>Finishing protection</li></ul><a href="{PHONE_HREF}">Call to book <span>↗</span></a></div>
          </article>
        </div>
        <div class="add-ons"><span>Ask about</span><p>Pet hair removal</p><i></i><p>Stain treatment</p><i></i><p>Paint enhancement</p><i></i><p>Protection options</p></div>
      </section>

      <section class="faq section" id="faq">
        <div><p class="section-kicker">Good to know</p><h2>{c['name']} questions, answered.</h2><p class="faq-intro">Anything else, bring it to the call and we'll make sure you know exactly what to expect.</p></div>
        <div class="accordion">
          {faqs}
        </div>
      </section>

      <section class="areas section" id="nearby">
        <div class="section-head">
          <div><p class="section-kicker">Nearby</p><h2>We also detail around {c['name']}.</h2></div>
          <p>Same service, same care, a short drive either way.</p>
        </div>
        <div class="area-grid">
          {neighbors}
        </div>
        <p class="area-note">See every area we cover on the <a href="/#areas">Greater Houston service map</a>.</p>
      </section>

      <section class="quote section" id="quote">
        <div class="quote-copy">
          <p class="section-kicker light">Your clean slate starts here</p>
          <h2>Call us and get the right quote fast.</h2>
          <p>Call {PHONE_DISPLAY} for pricing and quick questions, or book a time online. Either way, we'll handle the rest.</p>
          <div class="quote-note"><span>FR</span><p><strong>Not sure what you need?</strong><br />Describe the condition. We'll help you choose on the call.</p></div>
        </div>
        <div class="call-card">
          <p class="call-card-kicker">Fastest way to book in {c['name']}</p>
          <a class="button button-call call-button" href="{PHONE_HREF}">Call {PHONE_DISPLAY}</a>
          <a class="button button-book call-button" href="https://cal.com/sumitdatta/auto-detail-service">Book online</a>
          <ul class="call-points">
            <li>Get pricing without waiting for email</li>
            <li>Explain the vehicle condition in real time</li>
            <li>Book the detail while we have you on the line</li>
          </ul>
        </div>
      </section>
    </main>

    <footer>
      <a class="brand footer-brand" href="/"><svg class="brand-mark" viewBox="0 0 46 46" aria-hidden="true"><path d="M23 3 41 13v20L23 43 5 33V13L23 3Z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M13 28c5-1 6-10 16-10 3 0 5 1 7 3-3 0-5 1-7 3-4 4-8 7-16 4Z" fill="currentColor"/><circle cx="31.5" cy="14.5" r="2.5" fill="#b97745"/></svg><span>Fresh Ride <b>Mobile</b></span></a>
      <p>Professional mobile auto detailing across Greater Houston—at home, at work, on your time.</p>
      <div class="footer-links"><a href="/#services">Services</a><a href="/#process">How it works</a><a href="/#faq">FAQ</a><a href="{PHONE_HREF}">Call {PHONE_DISPLAY}</a><a href="https://cal.com/sumitdatta/auto-detail-service">Book online</a></div>
      <div class="footer-links footer-areas">{nav(c['slug'])}</div>
      <div class="footer-bottom"><span>© <span id="year"></span> Fresh Ride Mobile</span><span>freshridemobile.shop</span></div>
    </footer>
    <div class="mobile-bar"><a class="mobile-call-bar" href="{PHONE_HREF}">Call {PHONE_DISPLAY}</a><a class="mobile-book-bar" href="https://cal.com/sumitdatta/auto-detail-service">Book</a></div>
    <script src="/script.js"></script>
  </body>
</html>
"""


def sitemap():
    urls = [(f"{SITE}/", "1.0")] + [(f"{SITE}/{c['slug']}", "0.8") for c in CITIES]
    body = "".join(
        f"  <url>\n    <loc>{u}</loc>\n    <changefreq>monthly</changefreq>\n"
        f"    <priority>{p}</priority>\n  </url>\n"
        for u, p in urls
    )
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{body}</urlset>\n")


def check():
    """Fails loudly if a city page would ship as a doorway page."""
    seen = {}
    for c in CITIES:
        for field in ("conditions", "parking", "timing"):
            text = c[field]
            assert len(text) > 120, f"{c['slug']}: {field} too thin to justify a page"
            assert text not in seen, f"{c['slug']}: {field} duplicates {seen[text]} — doorway risk"
            seen[text] = c["slug"]
        assert len(c["faq"]) >= 3, f"{c['slug']}: needs 3+ city-specific FAQs"
        assert len(c["hoods"]) >= 5, f"{c['slug']}: needs 5+ named neighborhoods"
        for n in c["neighbors"]:
            assert n in BY_SLUG, f"{c['slug']}: unknown neighbor {n}"
        assert c["slug"] not in c["neighbors"], f"{c['slug']}: links to itself"
        json.loads(schema(c))
    print(f"check ok — {len(CITIES)} cities, no duplicate local content")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    check()
    for c in CITIES:
        path = os.path.join(here, f"{c['slug']}.html")
        with open(path, "w") as f:
            f.write(page(c))
        print(f"wrote {c['slug']}.html")
    with open(os.path.join(here, "sitemap.xml"), "w") as f:
        f.write(sitemap())
    print("wrote sitemap.xml")
