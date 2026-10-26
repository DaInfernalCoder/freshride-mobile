#!/usr/bin/env python3
"""Generate service and pricing pages for the static Fresh Ride site.

The output is committed so Vercel can serve clean static URLs without a build step.
Content intentionally avoids invented prices, durations, guarantees, or portfolio claims.
"""

import html
import json
import os

SITE = "https://sugarlandcardetailing.shop"
PHONE_DISPLAY = "+1 346-489-2266"
PHONE_HREF = "tel:+13464892266"
PHONE_SCHEMA = "+1-346-489-2266"
BOOK_URL = "https://cal.com/sumitdatta/auto-detail-service"

SERVICES = [
    {
        "slug": "full-reset",
        "name": "Full Reset",
        "title": "Full-Service Mobile Car Detailing Houston | Fresh Ride",
        "description": "Full-service mobile car detailing across Greater Houston. Fresh Ride handles the interior and exterior at your driveway or workplace. Call for a clear vehicle-specific quote.",
        "eyebrow": "Interior + exterior · Greater Houston",
        "h1": "A complete reset, inside and out.",
        "lead": (
            "Fresh Ride's Full Reset is the most complete starting point for a vehicle that needs attention inside "
            "and out. We bring mobile detailing to a suitable driveway, workplace, or approved parking location "
            "across Greater Houston, then work through the exterior, wheels, tires, cabin, surfaces, and glass. "
            "Because vehicle size and condition change the amount of work, we confirm the scope and quote before "
            "the visit rather than publishing a price that may not fit your car. Tell us about pet hair, stains, "
            "odors, paint concerns, or heavy buildup when you call. We will explain what fits the standard service, "
            "what may need an add-on, and what result is realistic before you book. That up-front review keeps the "
            "visit focused and lets us bring the right setup for the work you actually want at your location."
        ),
        "image": "/assets/service-full.jpg",
        "image_alt": "Representative image of a complete interior and exterior vehicle detail",
        "included": [
            "Detailed exterior wash and dry",
            "Wheel and tire cleaning",
            "Exterior glass",
            "Thorough interior vacuum",
            "Dash, console, trim, and interior glass",
            "Finishing protection appropriate to the service",
        ],
        "best_for": [
            "Seasonal or overdue vehicle resets",
            "Daily drivers needing both cabin and exterior care",
            "Vehicles being prepared for a trip, sale, or return",
        ],
        "quote_factors": ["Vehicle size", "Interior and exterior condition", "Pet hair or stain treatment", "Requested protection or paint enhancement"],
        "faqs": [
            ("What is included in a Full Reset?", "The Full Reset combines the core exterior wash, wheels and tires, exterior glass, interior vacuum, cabin surfaces, trim, and interior glass. We confirm the exact checklist and any optional treatment before the appointment."),
            ("How much does a Full Reset cost?", "The quote depends on vehicle size, condition, and requested add-ons. Call or book a time to describe the vehicle, and we will confirm the scope and price before the visit."),
            ("Can you handle pet hair, stains, or odors?", "In many cases, yes. These can change the time and treatment required, so mention every problem area when you call. We will set expectations before booking."),
            ("Where can you perform the detail?", "At a suitable driveway, workplace, or other approved parking location across Greater Houston. We confirm parking and any site-specific access needs before arrival."),
        ],
    },
    {
        "slug": "interior",
        "name": "Interior Reset",
        "title": "Mobile Interior Car Detailing Houston | Fresh Ride",
        "description": "Mobile interior car detailing across Greater Houston. Fresh Ride vacuums and details cabin surfaces, trim, and glass at your driveway or workplace. Call for a quote.",
        "eyebrow": "Cabin care · Greater Houston",
        "h1": "Make the inside feel calm again.",
        "lead": (
            "Fresh Ride's Interior Reset is mobile cabin detailing for the dust, crumbs, glass film, and daily "
            "buildup that collect around the places you use most. We come to a suitable driveway, workplace, or "
            "approved parking location across Greater Houston and work through the seats and floors with a thorough "
            "vacuum, then clean the dash, console, trim, and interior glass included in the confirmed service. "
            "Every interior is different, so the quote reflects the vehicle's size and condition. Pet hair, embedded "
            "stains, odors, and heavy buildup may need extra time or a different treatment. Describe those areas "
            "when you call and we will explain what can be addressed, what changes the quote, and what result is "
            "realistic before the appointment is booked. That up-front condition check helps us prepare the right "
            "approach and keeps the visit focused on the areas you care about most."
        ),
        "image": "/assets/service-interior.jpg",
        "image_alt": "Representative image of a freshly cleaned modern vehicle interior",
        "included": [
            "Thorough cabin and cargo-area vacuum",
            "Dash and center console cleaning",
            "Door panels and accessible trim",
            "Interior glass",
            "Attention to common touchpoints and crevices",
            "A condition review before work begins",
        ],
        "best_for": [
            "Busy family and commuter vehicles",
            "Dust, crumbs, smudges, and everyday buildup",
            "Drivers who care most about the space they sit in",
        ],
        "quote_factors": ["Vehicle and cabin size", "Amount of buildup", "Pet hair", "Stains, odors, and requested spot treatment"],
        "faqs": [
            ("What does the Interior Reset include?", "It starts with a thorough vacuum and includes the dash, center console, accessible trim, door panels, and interior glass. We confirm the exact checklist for your vehicle before the visit."),
            ("Can you remove every stain or odor?", "No detailer can honestly promise that without inspecting the material and cause. Tell us where the stain or odor is and how long it has been present so we can set a realistic expectation."),
            ("Do pet hair and heavy buildup cost more?", "They can, because they change the time and tools required. Mention them on the call so the quote reflects the actual condition instead of surprising you on arrival."),
            ("Can you detail while I am at work?", "Often, yes, if the parking location allows the service and vehicle access is arranged. We confirm the location and access details before booking."),
        ],
    },
    {
        "slug": "exterior",
        "name": "Exterior Refresh",
        "title": "Mobile Exterior Car Detailing Houston | Fresh Ride",
        "description": "Mobile exterior car detailing across Greater Houston. Fresh Ride brings a careful wash, wheels, tires, glass, and finish to your driveway or workplace. Call for a quote.",
        "eyebrow": "Paint, glass, wheels · Greater Houston",
        "h1": "Bring back the finish—without the detour.",
        "lead": (
            "Fresh Ride's Exterior Refresh brings careful mobile exterior detailing to a suitable driveway, "
            "workplace, or approved parking location across Greater Houston. The confirmed service covers a hand "
            "wash and dry, wheels and tires, exterior glass, and the finishing step selected for the vehicle. We do "
            "not treat every paint issue as something a wash can solve. Tree sap, mineral spots, bonded contamination, "
            "scratches, and neglected paint may require a different process or paint enhancement. Describe the "
            "condition when you call, especially any problem areas that have been sitting in the Texas sun. We will "
            "confirm what is included, explain any optional treatment, and give you a vehicle-specific quote before "
            "the appointment rather than changing the scope after we arrive. That condition check keeps the booked "
            "work clear and helps us plan the right setup for the result you actually want."
        ),
        "image": "/assets/service-exterior.jpg",
        "image_alt": "Representative image of a freshly detailed vehicle exterior and wheel",
        "included": [
            "Careful exterior wash and dry",
            "Wheel and tire cleaning",
            "Exterior glass",
            "Attention to visible exterior buildup",
            "A confirmed finishing protection step",
            "Condition review before work begins",
        ],
        "best_for": [
            "Routine exterior maintenance",
            "Road film, dust, and everyday grime",
            "Drivers who want a careful alternative to a rushed tunnel wash",
        ],
        "quote_factors": ["Vehicle size", "Paint and wheel condition", "Sap, water spots, or bonded contamination", "Requested protection or paint enhancement"],
        "faqs": [
            ("What is included in the Exterior Refresh?", "The confirmed service includes a careful exterior wash and dry, wheels and tires, exterior glass, and the selected finishing protection. We review the vehicle condition before work begins."),
            ("Can a wash remove scratches or etched water spots?", "Not always. Some defects sit in or below the paint surface and may require paint enhancement or correction. Describe the issue on the call and we will separate wash work from correction work honestly."),
            ("What happens if the weather changes?", "If weather makes the work unsafe or would compromise the finish, we coordinate a better time rather than hand back a result we are not comfortable with."),
            ("Do you service trucks and SUVs?", "Yes. Vehicle size affects the scope and quote, so tell us the year, make, model, and condition when you call or book online."),
        ],
    },
]


def brand(mark_link="/"):
    return f'''<a class="brand" href="{mark_link}" aria-label="Fresh Ride Mobile home">
        <svg class="brand-mark" viewBox="0 0 46 46" aria-hidden="true"><path d="M23 3 41 13v20L23 43 5 33V13L23 3Z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M13 28c5-1 6-10 16-10 3 0 5 1 7 3-3 0-5 1-7 3-4 4-8 7-16 4Z" fill="currentColor"/><circle cx="31.5" cy="14.5" r="2.5" fill="#b97745"/></svg>
        <span>Fresh Ride <b>Mobile</b></span>
      </a>'''


def header(active=""):
    def current(name):
        return ' aria-current="page"' if active == name else ""
    return f'''<header class="site-header" id="top">
      {brand()}
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span><span class="sr-only">Open menu</span></button>
      <nav id="site-nav" aria-label="Main navigation">
        <a href="/services/full-reset">Services</a>
        <a href="/pricing"{current("pricing")}>Pricing</a>
        <a href="/#areas">Areas</a>
        <a href="/#faq">FAQ</a>
        <a href="{BOOK_URL}">Book online</a>
      </nav>
      <a class="button button-small header-cta button-call" href="{PHONE_HREF}">Call {PHONE_DISPLAY}</a>
    </header>'''


def footer():
    return f'''<footer>
      <div class="footer-brand-wrap">{brand()}</div>
      <p>Professional mobile auto detailing across Greater Houston—at home, at work, on your time.</p>
      <p>18726 University Blvd, Sugar Land, TX 77479</p>
      <div class="footer-links"><a href="/services/full-reset">Full Reset</a><a href="/services/interior">Interior</a><a href="/services/exterior">Exterior</a><a href="/pricing">Pricing</a><a href="{PHONE_HREF}">Call</a><a href="{BOOK_URL}">Book online</a></div>
      <div class="footer-links footer-areas"><a href="/katy">Katy</a><a href="/sugar-land">Sugar Land</a><a href="/the-woodlands">The Woodlands</a><a href="/cypress">Cypress</a><a href="/pearland">Pearland</a></div>
      <div class="footer-bottom"><span>© <span id="year"></span> Fresh Ride Mobile</span><span>sugarlandcardetailing.shop</span></div>
    </footer>
    <div class="mobile-bar"><a class="mobile-call-bar" href="{PHONE_HREF}">Call {PHONE_DISPLAY}</a><a class="mobile-book-bar" href="{BOOK_URL}">Book</a></div>
    <script src="/script.js"></script>'''


def head(title, description, url, schema, image="/assets/hero-car.jpg"):
    absolute_image = f"{SITE}{image}"
    return f'''<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="theme-color" content="#071722" />
    <meta name="description" content="{html.escape(description, quote=True)}" />
    <link rel="canonical" href="{url}" />
    <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml" />
    <link rel="preload" href="/assets/fonts/barlow-800.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="preload" href="/assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="stylesheet" href="/fonts.css" />
    <link rel="stylesheet" href="/styles.css" />
    <link rel="stylesheet" href="/header-contrast.css" />
    <link rel="stylesheet" href="/content-pages.css" />
    <title>{html.escape(title)}</title>
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Fresh Ride Mobile" />
    <meta property="og:title" content="{html.escape(title, quote=True)}" />
    <meta property="og:description" content="{html.escape(description, quote=True)}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{absolute_image}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{html.escape(title, quote=True)}" />
    <meta name="twitter:description" content="{html.escape(description, quote=True)}" />
    <meta name="twitter:image" content="{absolute_image}" />
    <script type="application/ld+json">
{json.dumps(schema, indent=2)}
    </script>
  </head>'''


def business_ref():
    return {
        "@type": "AutoWash",
        "@id": f"{SITE}/#business",
        "name": "Fresh Ride Mobile",
        "url": f"{SITE}/",
        "telephone": PHONE_SCHEMA,
        "priceRange": "$$",
        "address": {"@type": "PostalAddress", "streetAddress": "18726 University Blvd", "addressLocality": "Sugar Land", "addressRegion": "TX", "postalCode": "77479", "addressCountry": "US"},
        "areaServed": [
            {"@type": "City", "name": "Houston"}, {"@type": "City", "name": "Katy"},
            {"@type": "City", "name": "Sugar Land"}, {"@type": "City", "name": "The Woodlands"},
            {"@type": "City", "name": "Cypress"}, {"@type": "City", "name": "Pearland"},
        ],
    }


def service_schema(service):
    url = f"{SITE}/services/{service['slug']}"
    faq = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in service["faqs"]]
    return {
        "@context": "https://schema.org",
        "@graph": [
            business_ref(),
            {
                "@type": "Service",
                "@id": f"{url}#service",
                "name": service["name"],
                "description": service["description"],
                "url": url,
                "provider": {"@id": f"{SITE}/#business"},
                "areaServed": {"@type": "AdministrativeArea", "name": "Greater Houston"},
                "serviceType": "Mobile auto detailing",
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Services", "item": f"{SITE}/#services"},
                    {"@type": "ListItem", "position": 3, "name": service["name"], "item": url},
                ],
            },
            {"@type": "FAQPage", "@id": f"{url}#faq", "mainEntity": faq},
        ],
    }


def list_items(items, class_name="check-list"):
    return f'<ul class="{class_name}">' + "".join(f"<li>{html.escape(item)}</li>" for item in items) + "</ul>"


def related_cards(active):
    cards = []
    for item in SERVICES:
        if item["slug"] == active:
            continue
        cards.append(
            f'''<a class="related-card" href="/services/{item['slug']}">
              <span>{html.escape(item['eyebrow'])}</span><h3>{html.escape(item['name'])}</h3>
              <p>{html.escape(item['description'].split('.')[0])}.</p><strong>Explore service ↗</strong>
            </a>'''
        )
    cards.append('''<a class="related-card related-pricing" href="/pricing"><span>Before you book</span><h3>Pricing + quotes</h3><p>See what changes the quote and what to share when you call.</p><strong>See pricing ↗</strong></a>''')
    return "".join(cards)


def service_page(service):
    url = f"{SITE}/services/{service['slug']}"
    faqs = "".join(f"<details><summary>{html.escape(q)}<span>+</span></summary><p>{html.escape(a)}</p></details>" for q, a in service["faqs"])
    return f'''<!doctype html>
<html lang="en">
  {head(service['title'], service['description'], url, service_schema(service), service['image'])}
  <body>
    <a class="skip-link" href="#main">Skip to content</a>
    {header("services")}
    <main id="main">
      <section class="subhero">
        <img class="subhero-media" src="{service['image']}" alt="{html.escape(service['image_alt'], quote=True)}" />
        <div class="subhero-shade" aria-hidden="true"></div><div class="clean-pass" aria-hidden="true"></div>
        <div class="subhero-content">
          <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><a href="/#services">Services</a><span>/</span>{html.escape(service['name'])}</nav>
          <p class="eyebrow"><span></span>{html.escape(service['eyebrow'])}</p>
          <h1>{html.escape(service['h1'])}</h1>
          <p class="subhero-lead">{html.escape(service['lead'])}</p>
          <div class="hero-actions"><a class="button button-call" href="{PHONE_HREF}">Call for a quote <span aria-hidden="true">↗</span></a><a class="button button-book" href="{BOOK_URL}">Book online <span aria-hidden="true">↗</span></a></div>
        </div>
      </section>

      <section class="service-detail section">
        <div class="service-detail-main"><p class="section-kicker">What the service covers</p><h2>A focused checklist. A quote that fits the vehicle.</h2>{list_items(service['included'])}</div>
        <aside class="service-quote-panel"><p class="panel-label">Quote factors</p><h3>Why every vehicle gets its own number.</h3>{list_items(service['quote_factors'], 'factor-list')}<a href="/pricing">How pricing works <span aria-hidden="true">↗</span></a></aside>
      </section>

      <section class="fit-section section">
        <div><p class="section-kicker light">Best fit</p><h2>Choose this reset when…</h2></div>
        {list_items(service['best_for'], 'fit-list')}
      </section>

      <section class="service-flow section">
        <div class="section-head"><div><p class="section-kicker">From call to clean</p><h2>Three decisions. No surprises.</h2></div><p>We confirm the vehicle, condition, location, and requested work before the visit.</p></div>
        <ol class="flow-grid"><li><span>1</span><h3>Describe the vehicle</h3><p>Share the year, make, model, location, and any problem areas.</p></li><li><span>2</span><h3>Confirm scope + quote</h3><p>We match the service to the condition and agree on the price before arrival.</p></li><li><span>3</span><h3>Get your time back</h3><p>We work on-site while you keep your day moving.</p></li></ol>
      </section>

      <section class="faq section"><div><p class="section-kicker">Good to know</p><h2>{html.escape(service['name'])} questions.</h2><p class="faq-intro">Clear answers before we pull up.</p></div><div class="accordion">{faqs}</div></section>

      <section class="related section"><div class="section-head"><div><p class="section-kicker">Other starting points</p><h2>Match the service to the need.</h2></div><p>Not sure which one fits? Call and describe the condition. We will help you choose.</p></div><div class="related-grid">{related_cards(service['slug'])}</div></section>

      <section class="quote section"><div class="quote-copy"><p class="section-kicker light">Ready when you are</p><h2>Get a clear quote before the visit.</h2><p>Call {PHONE_DISPLAY}, or choose a time online and we will confirm the details.</p></div><div class="call-card"><p class="call-card-kicker">Fastest way to book</p><a class="button button-call call-button" href="{PHONE_HREF}">Call {PHONE_DISPLAY}</a><a class="button button-book call-button" href="{BOOK_URL}">Book online</a></div></section>
    </main>
    {footer()}
  </body>
</html>
'''


def pricing_schema():
    url = f"{SITE}/pricing"
    return {
        "@context": "https://schema.org",
        "@graph": [
            business_ref(),
            {"@type": "WebPage", "@id": f"{url}#webpage", "url": url, "name": "Mobile Detailing Pricing in Houston", "about": {"@id": f"{SITE}/#business"}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Pricing", "item": url},
            ]},
        ],
    }


def pricing_page():
    title = "Mobile Car Detailing Pricing Houston | Fresh Ride Mobile"
    description = "Fresh Ride Mobile confirms detailing prices by vehicle size, condition, service, and add-ons. See how quotes work, then call or book online for a clear price before the visit."
    url = f"{SITE}/pricing"
    cards = "".join(
        f'''<article class="price-card"><span>{html.escape(s['eyebrow'])}</span><h2>{html.escape(s['name'])}</h2><p>{html.escape(s['description'].split('.')[0])}.</p><strong>Quote confirmed before the visit</strong><a href="/services/{s['slug']}">See what is included <i aria-hidden="true">↗</i></a></article>'''
        for s in SERVICES
    )
    return f'''<!doctype html>
<html lang="en">
  {head(title, description, url, pricing_schema())}
  <body>
    <a class="skip-link" href="#main">Skip to content</a>
    {header("pricing")}
    <main id="main">
      <section class="pricing-hero">
        <div class="pricing-orbit" aria-hidden="true"><span></span><span></span><span></span></div>
        <div class="pricing-hero-content"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span>Pricing</nav><p class="eyebrow"><span></span>Mobile detailing · Greater Houston</p><h1>A clear quote before we arrive.</h1><p>Fresh Ride prices the actual vehicle—not a best-case version of it. Tell us the size, condition, location, and service you need. We confirm the scope and number before the visit.</p><div class="hero-actions"><a class="button button-call" href="{PHONE_HREF}">Call for pricing <span aria-hidden="true">↗</span></a><a class="button button-book" href="{BOOK_URL}">Book online <span aria-hidden="true">↗</span></a></div></div>
      </section>

      <section class="pricing-intro section"><p class="section-kicker">Choose a starting point</p><div class="intro-grid"><h2>Three services. One honest quote.</h2><p class="lead">Fresh Ride uses vehicle-specific quotes because size, condition, and add-ons change the job. We confirm the number before the visit so this page never promises a best-case price that does not fit your vehicle.</p></div><div class="pricing-grid">{cards}</div></section>

      <section class="quote-factors section"><div><p class="section-kicker light">What changes the quote</p><h2>The work follows the condition.</h2></div><div class="factor-stack"><article><span>01</span><h3>Vehicle size</h3><p>A coupe, three-row SUV, and work truck do not require the same amount of time or material.</p></article><article><span>02</span><h3>Current condition</h3><p>Routine maintenance and months of heavy buildup are different jobs. Photos help us quote accurately.</p></article><article><span>03</span><h3>Problem areas</h3><p>Pet hair, stains, odors, sap, mineral spots, and bonded contamination can need extra treatment.</p></article><article><span>04</span><h3>Requested finish</h3><p>Protection and paint-enhancement options are scoped separately from the core wash or interior detail.</p></article></div></section>

      <section class="quote-prep section"><div><p class="section-kicker">Get the number faster</p><h2>Have these five details ready.</h2></div><ol><li>Year, make, and model</li><li>Which service looks closest</li><li>Where the vehicle will be parked</li><li>Problem areas or add-ons</li><li>Two or three clear photos for heavier conditions</li></ol></section>

      <section class="quote section"><div class="quote-copy"><p class="section-kicker light">No arrival-day surprise</p><h2>Describe it. Price it. Book it.</h2><p>Call {PHONE_DISPLAY} for the fastest quote, or book online and we will confirm the vehicle details before the visit.</p></div><div class="call-card"><p class="call-card-kicker">Talk through the vehicle now</p><a class="button button-call call-button" href="{PHONE_HREF}">Call {PHONE_DISPLAY}</a><a class="button button-book call-button" href="{BOOK_URL}">Book online</a><ul class="call-points"><li>Scope confirmed before arrival</li><li>Condition and add-ons discussed up front</li><li>No invented one-size-fits-all price</li></ul></div></section>
    </main>
    {footer()}
  </body>
</html>
'''


def validate():
    seen = set()
    for service in SERVICES:
        assert service["slug"] not in seen
        seen.add(service["slug"])
        assert 134 <= len(service["lead"].split()) <= 167, f"{service['slug']}: answer block outside GEO range"
        assert len(service["faqs"]) >= 4
        json.loads(json.dumps(service_schema(service)))
    json.loads(json.dumps(pricing_schema()))


if __name__ == "__main__":
    validate()
    here = os.path.dirname(os.path.abspath(__file__))
    services_dir = os.path.join(here, "services")
    os.makedirs(services_dir, exist_ok=True)
    for service in SERVICES:
        path = os.path.join(services_dir, f"{service['slug']}.html")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(service_page(service))
        print(f"wrote services/{service['slug']}.html")
    with open(os.path.join(here, "pricing.html"), "w", encoding="utf-8") as handle:
        handle.write(pricing_page())
    print("wrote pricing.html")
