#!/usr/bin/env python3
"""SEO expansion: 6 new service pages, 24 new area pages, /areas hub, global nav/footer/schema/sitemap/llms.

Idempotent overlay on the reviewed static output. Do NOT run build_pages.py / build_content_pages.py
(stale historic generators). Run:  python3 build_expansion.py
City copy comes from _seo-research/content/<slug>.json (verified facts only).
"""
import hashlib
import html
import json
import math
import re
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
SITE = "https://sugarlandcardetailing.shop"
PHONE = "+1 346-489-2266"
PHONE_HREF = "tel:+13464892266"
BOOK = "https://cal.com/sumitdatta/auto-detail-service"
TODAY = date.today().isoformat()
e = html.escape

# ---------------------------------------------------------------- services
EXISTING_SERVICES = [
    ("full-reset", "Full Reset (interior + exterior)"),
    ("interior", "Interior Detailing"),
    ("exterior", "Exterior Detailing"),
    ("car-waxing", "Car Waxing"),
    ("clay-bar-treatment", "Clay-Bar Treatment"),
    ("seat-shampooing", "Car Seat Shampooing"),
    ("steam-cleaning", "Interior Steam Cleaning"),
    ("engine-detailing", "Engine-Bay Detailing"),
]

NEW_SERVICES = {
    "ceramic-coating": {
        "name": "Ceramic Coating",
        "title": "Ceramic Coating in Sugar Land, TX | Mobile Application",
        "desc": "Mobile ceramic coating in Sugar Land, TX. Paint preparation, coating application and care guidance at your location. Call to confirm your vehicle and quote.",
        "image": "result-finish",
        "eyebrow": "Paint protection · Sugar Land, TX",
        "h1": "Ceramic Coating in Sugar Land, TX",
        "lead": "Ceramic coating adds a hard, slick protective layer over properly prepared paint, which makes a car easier to wash and helps the finish shrug off Texas sun, road film and water spotting. Sugar Land Car Detailing applies ceramic coating at a suitable location you arrange, after the wash, decontamination and surface preparation the coating needs to bond. The result depends on how much prep the paint needs first, so we look at the vehicle and agree the scope and quote before any product goes on.",
        "included": [
            "Condition review of the paint, glass and trim to be coated",
            "Thorough wash and decontamination so the surface is clean for bonding",
            "Panel wipe and the preparation the chosen coating requires",
            "Application of the agreed ceramic coating to the paint panels",
            "Cure and care instructions for the first days and weeks after application",
        ],
        "limits_h": "What a coating does and does not do",
        "limits": "A ceramic coating is a protective layer, not a repair. It does not fill or remove scratches, swirl marks or etching, and it will lock in whatever condition the paint is in when it is applied, which is why a coating is often paired with paint correction first. Coatings are not scratch-proof and still need regular, careful washing. Ask for the specific product, the cure requirements and the care instructions before you book, and do not rely on any fixed-year promise. Weather matters: coatings need dry, controlled conditions to apply and cure properly, so we schedule around rain, heat and wind.",
        "prep_h": "Plan the day and the location",
        "prep": "Choose a shaded, level spot such as a garage bay or covered driveway where the car can sit undisturbed while the coating flashes and begins to cure. Tell us the year, make, model and colour, any previous waxes, sealants or coatings, and any paint repair or repaint history. Keep the vehicle out of rain and sprinklers for the cure period we give you. If your community or workplace restricts washing or chemical use on site, tell us before the appointment so we can plan around it.",
        "cost": "Vehicle size, paint condition, how much correction is needed beforehand, and the coating product chosen all change the quote. A newer garage-kept car needs far less preparation than an older daily driver with swirls and water spots. Share photos or describe the condition when you call and we will confirm scope and price before the visit.",
        "local": "Sugar Land heat and sun are hard on clear coat, and sprinkler water in neighbourhoods like First Colony, New Territory and Telfair leaves mineral spotting that a coating makes easier to wipe away. If you are further out in Fort Bend County, check the service-area pages and confirm your address when you call.",
        "faqs": [
            ("Can you apply ceramic coating at my home?", "Often yes, if there is a suitable covered or shaded spot, access and room to work. We confirm the location, weather window and cure requirements before booking."),
            ("Will ceramic coating stop scratches?", "No. A coating adds protection and makes washing easier, but it is not scratch-proof and it does not repair existing damage. Correct visible defects before coating."),
            ("Do I need paint correction before a coating?", "Frequently, because a coating seals in the surface as it is. If the paint has swirls, haze or etching, discuss paint correction first so the coated finish looks its best."),
            ("How much does ceramic coating cost?", "It depends on vehicle size, condition, the product and the preparation required. Call or book online and we will quote after hearing about your vehicle."),
        ],
        "related": ["paint-correction", "car-waxing", "full-reset"],
    },
    "paint-correction": {
        "name": "Paint Correction, Buffing & Polishing",
        "title": "Car Buffing & Paint Correction in Sugar Land, TX",
        "desc": "Mobile car buffing, polishing and paint correction in Sugar Land, TX for swirls, haze and light scratches. Call for a paint-condition review and quote.",
        "image": "service-exterior",
        "eyebrow": "Buffing & polishing · Sugar Land, TX",
        "h1": "Car Buffing & Paint Correction in Sugar Land, TX",
        "lead": "Paint correction is machine buffing and polishing that levels the clear coat to remove swirl marks, light scratches, oxidation haze and water-spot etching, so the paint reflects light again. Sugar Land Car Detailing brings buffing and polishing to a suitable location you arrange. How much improvement is possible depends on how deep the defects are and how much clear coat is left, so we inspect the paint and explain what to expect before we start.",
        "included": [
            "Paint inspection in good light to identify swirls, scratches, haze and etching",
            "Wash and decontamination so no grit is dragged across the paint",
            "Machine polishing with the pad and polish matched to the paint",
            "Panel wipe to reveal the true finish after polishing",
            "Optional wax, sealant or ceramic coating to protect the corrected paint",
        ],
        "limits_h": "Correction has limits",
        "limits": "Buffing removes a thin layer of clear coat, so it can only improve defects that sit within that layer. A scratch you can catch with a fingernail, deep etching, clear-coat failure or a chip needs repair beyond polishing. We tell you honestly which defects can be reduced, which can only be softened and which cannot be fixed by polishing. Single-stage polishing for gloss differs from multi-step correction for heavy swirling, and the time and quote differ with it.",
        "prep_h": "How to get the most from the appointment",
        "prep": "Park where we have light and space to walk around the car, ideally shaded. Point out the scratches, rub marks and spots that bother you most, and mention any previous repaint, bodywork, wraps or ceramic coating, since those change the approach. Wash-and-wax customers often add correction later, so tell us your goal: a quick gloss boost before a sale, or a thorough restoration before you protect the paint.",
        "cost": "Paint condition, vehicle size, paint hardness and the number of polishing steps drive the quote. A light gloss polish takes much less time than correcting a dark, heavily swirled car. Describe the condition or send photos when you call, and we confirm scope and price before the visit.",
        "local": "Automatic car-wash brushes, gritty towels and Houston-area sun and humidity are the usual causes of swirling and haze we see on daily drivers around Sugar Land, Stafford and Missouri City. If you are buffing before a ceramic coating or waxing, plan both together so the corrected paint is protected straight away.",
        "faqs": [
            ("Can you buff out scratches?", "Light surface scratches and swirl marks often improve a lot or disappear. Deeper scratches that catch a fingernail may only soften. We assess the paint first and tell you what is realistic."),
            ("Is buffing the same as polishing?", "People use the words interchangeably. Paint correction is machine polishing with different pads and polishes to remove defects first, then refine the finish to a high gloss."),
            ("Will buffing damage my paint?", "Done properly it removes a very thin amount of clear coat. Thin or previously repainted paint needs extra care, so mention any bodywork and we measure risk before polishing."),
            ("Should I wax or coat after correction?", "Yes, protect corrected paint. Waxing is the simpler option, while a ceramic coating gives longer-lasting protection. We can quote either with the correction."),
        ],
        "related": ["ceramic-coating", "car-waxing", "clay-bar-treatment"],
    },
    "headlight-restoration": {
        "name": "Headlight Restoration",
        "title": "Headlight Restoration in Sugar Land, TX | Mobile Service",
        "desc": "Mobile headlight restoration in Sugar Land, TX for yellowed, foggy or hazy lenses. Sanding, polishing and UV protection at your location. Call for a quote.",
        "image": "service-exterior",
        "eyebrow": "Clear lenses · Sugar Land, TX",
        "h1": "Headlight Restoration in Sugar Land, TX",
        "lead": "Plastic headlight lenses cloud and yellow as the factory UV coating wears away under Texas sun, which dims the beam and makes the whole front end look tired. Sugar Land Car Detailing restores foggy, hazy and yellowed headlights by sanding away the oxidized layer, polishing the lens clear and sealing it with UV protection. We come to a suitable location you arrange, and we confirm what is realistic for each lens before work begins.",
        "included": [
            "Lens inspection to separate surface oxidation from moisture inside the housing",
            "Masking of surrounding paint and trim",
            "Staged wet sanding to remove the oxidized outer layer",
            "Polishing to restore clarity",
            "UV-protective sealant over the finished lens",
        ],
        "limits_h": "What restoration can and cannot fix",
        "limits": "Restoration treats the outside of the lens. It cannot fix cracked lenses, moisture or condensation trapped inside the housing, or a failing bulb or reflector. Heavily damaged lenses may improve but not return to like-new, and any restored lens will yellow again over time if it is left unprotected, which is why the UV sealing step matters. Replacement may be the better answer for deep pitting, cracks or internal damage.",
        "prep_h": "Before the appointment",
        "prep": "Tell us the year, make and model and whether the haze is on the outside surface or inside the lens. Park in a spot with room to open the hood and work around the front of the car. Headlights often pair well with an exterior detail or paint correction, so mention if you want the front end freshened as a whole.",
        "cost": "Lens condition, vehicle model and whether both lights need full restoration or a lighter polish affect the quote. Ask about combining headlight restoration with an exterior detail.",
        "local": "Long summers and constant sun exposure are a major reason headlights cloud on cars parked outdoors around Sugar Land and Fort Bend County. If your car sits in the sun at work all day, ask about the UV protection step.",
        "faqs": [
            ("Is headlight restoration worth it?", "For oxidized or yellowed lenses it can make a big difference to appearance and night visibility at a fraction of replacement cost. Cracked or moisture-filled lenses need replacement."),
            ("How long do restored headlights stay clear?", "It varies with sun exposure, parking and washing. A UV-protective sealant slows re-yellowing, but we do not promise a fixed duration."),
            ("Can you fix headlights with moisture inside?", "No. Condensation or water inside the housing is a seal problem. Restoration only works on the outer lens surface."),
            ("Do you restore both headlights?", "Yes. Both lenses are restored so they match. Tell us if only one is cloudy and we will quote accordingly."),
        ],
        "related": ["paint-correction", "exterior", "car-waxing"],
    },
    "pet-hair-removal": {
        "name": "Pet Hair Removal",
        "title": "Pet Hair Removal Car Detailing in Sugar Land, TX",
        "desc": "Mobile pet hair removal for cars in Sugar Land, TX. Embedded dog and cat hair removed from carpet, seats and cargo areas. Call for a quote.",
        "image": "service-interior",
        "eyebrow": "Pet-friendly interiors · Sugar Land, TX",
        "h1": "Pet Hair Removal Car Detailing in Sugar Land, TX",
        "lead": "Dog and cat hair weaves into carpet and fabric, and a normal vacuum rarely lifts it. Sugar Land Car Detailing removes embedded pet hair from seats, floors, mats and cargo areas using agitation and extraction methods matched to the material, then finishes the interior so the cabin looks and smells clean. We come to your driveway or workplace and confirm how heavy the hair load is before quoting.",
        "included": [
            "Assessment of how much hair and where it is embedded",
            "Loosening and lifting hair from carpet, mats and fabric",
            "Detailed vacuuming of seats, seams, vents and cargo area",
            "Wipe-down of hard surfaces and interior glass",
            "Optional seat shampooing or deodorizing for pet stains and smells",
        ],
        "limits_h": "Expect a big improvement, not always every hair",
        "limits": "Short, stiff hair woven into looped carpet can be stubborn, and some fine strands can remain in deep seams. Heavy shedding breeds mean the hair returns soon after cleaning. Pet urine, vomit and stains may need separate treatment, and permanent odor or discoloration cannot be guaranteed away. Tell us about pets, accidents and previous cleaning products so we can plan the right approach.",
        "prep_h": "How to prepare",
        "prep": "Remove pet carriers, blankets, harnesses and loose belongings. Tell us the pet type, the coat, and whether anything has soiled the seats. If the hair is mainly in the cargo area of an SUV or the back seat, tell us which areas to focus on. Hair tends to return, so ask about seat covers and between-visit upkeep.",
        "cost": "Vehicle size, the amount of hair and the material (looped carpet versus smooth fabric) change the time required. Heavy buildup in an SUV cargo area costs more than a light pass on a sedan. Add seat shampooing or odor treatment if stains are involved.",
        "local": "Families across Sugar Land, First Colony and Fort Bend County commute with dogs to parks and vet visits year-round, so back seats and cargo areas pick up hair, dirt and mud quickly in humid Gulf Coast weather.",
        "faqs": [
            ("Can you remove all the pet hair from my car?", "We remove the large majority from most vehicles. Very fine, deeply woven hair can leave a few strands. We tell you what to expect after seeing the car."),
            ("Do you also remove pet odors?", "We clean the sources we can reach, and we can add seat shampooing or odor treatment. Strong odors from accidents may need more than one step."),
            ("Is there an extra fee for pet hair?", "Heavy hair takes extra time and is reflected in the quote. A light dusting on one seat costs far less than a cargo area covered in hair."),
            ("How often should I schedule pet hair removal?", "That depends on shedding and how often pets ride. Many owners schedule seasonally or before selling or returning a lease."),
        ],
        "related": ["interior", "seat-shampooing", "odor-removal"],
    },
    "odor-removal": {
        "name": "Car Odor Removal",
        "title": "Car Odor Removal in Sugar Land, TX | Mobile Interior Cleaning",
        "desc": "Mobile car odor removal in Sugar Land, TX. We find and clean the source of smoke, pet, food, mildew and spill odors. Call for an interior review and quote.",
        "image": "service-interior",
        "eyebrow": "Fresh cabin · Sugar Land, TX",
        "h1": "Car Odor Removal in Sugar Land, TX",
        "lead": "Bad smells in a car almost always have a source: a spill soaked into carpet, food under a seat, mildew from a damp mat, smoke in the headliner or pet accidents in fabric. Sugar Land Car Detailing finds and cleans the source of cabin odors rather than masking them with air freshener. We come to a suitable location you arrange, review the interior with you and agree a plan before we start.",
        "included": [
            "Interior inspection to locate the source of the smell",
            "Removal of trash, debris and contaminated floor mats",
            "Deep vacuuming of carpet, seats, seams and vents",
            "Cleaning of fabric, carpet and hard surfaces affected by the odor",
            "Optional seat shampooing or steam cleaning where the material allows",
        ],
        "limits_h": "Odors are cleaned, not guaranteed away",
        "limits": "Some smells, such as long-term smoke, mold from a leak or a deep spill into foam padding, may take more than one visit or may only be reduced rather than fully removed. If the cause is a water leak, a clogged AC drain or a mechanical fault, cleaning alone will not stop the smell, and the underlying problem needs repair. We explain what we find and which steps are likely to help before you commit.",
        "prep_h": "Help us find the source",
        "prep": "Tell us what the smell is like, when it started, and whether it gets worse in humidity or when the AC runs. Mention smoking, pets, spills, wet gym bags, milk, vomit or flooding. Leave the windows closed so we can smell the problem on arrival, and clear out any trash and loose items beforehand.",
        "cost": "The source, severity and how many surfaces are involved decide the scope and the quote. A quick treatment for a food spill is far smaller than smoke removal across a full cabin.",
        "local": "Gulf Coast humidity, wet summers and damp floor mats are the main causes of musty smells in vehicles around Sugar Land. If the smell returns after cleaning, have a technician check for leaks or a blocked AC drain.",
        "faqs": [
            ("Can you remove cigarette smoke smell from a car?", "We can clean and reduce it significantly, but heavy smoke in the headliner and padding may need repeated treatment. We explain what is realistic after inspecting the car."),
            ("Why does my car smell musty?", "Usually damp carpet, a wet mat, a leak or a dirty AC system. Cleaning helps, but the moisture source must be fixed or the smell returns."),
            ("Do you use air fresheners?", "Our focus is cleaning the source. A light finishing scent is possible on request, but freshener alone does not remove an odor."),
            ("How long does odor removal take?", "It depends on the source and severity. A spill may be quick, while smoke or mildew takes longer. We estimate after inspecting the interior."),
        ],
        "related": ["interior", "pet-hair-removal", "steam-cleaning"],
    },
    "mobile-car-wash": {
        "name": "Mobile Car Wash",
        "title": "Mobile Car Wash & Hand Wash in Sugar Land, TX",
        "desc": "Mobile hand car wash in Sugar Land, TX. We wash and dry your car, wheels and glass at your home or office. Call or book online to schedule.",
        "image": "service-exterior",
        "eyebrow": "Hand wash · Sugar Land, TX",
        "h1": "Mobile Car Wash in Sugar Land, TX",
        "lead": "Skip the tunnel line. Sugar Land Car Detailing brings a careful hand car wash to your home or workplace, so you get a clean, spot-free car without driving anywhere or letting spinning brushes touch your paint. The wash covers the body, wheels, tires and glass, and it pairs easily with interior cleaning, waxing or a full detail when the car needs more than a rinse.",
        "included": [
            "Pre-rinse to loosen dirt before any contact with the paint",
            "Hand wash with clean wash media, not tunnel brushes",
            "Wheels, tires and wheel wells cleaned",
            "Exterior glass cleaned",
            "Dry and finish to avoid water spots",
        ],
        "limits_h": "A wash is not a detail",
        "limits": "A hand wash removes surface dirt and road film. It does not remove bonded contamination, etched water spots, swirl marks or scratches, and it does not clean the interior. If your paint feels rough after washing, ask about clay-bar treatment, or about paint correction for swirls. Heavily soiled vehicles may need a more thorough exterior detail than a basic wash.",
        "prep_h": "What we need at your location",
        "prep": "A driveway or parking space where the vehicle can sit with room to work around it, ideally out of direct midday sun. Tell us about gates, HOA or workplace rules on washing, and whether the property has a spigot or we should plan self-contained supplies. We reschedule around heavy rain.",
        "cost": "Vehicle size and how dirty it is drive the quote. Add interior vacuuming, waxing or a full detail when you book and we price the combination.",
        "local": "Sugar Land summers bring dust, pollen and bug splatter to paint, and many neighborhoods have rules about driveway washing. Mobile service is a simple way to keep the car clean without leaving home or breaking HOA rules.",
        "faqs": [
            ("Is a mobile hand wash safer for paint than a tunnel wash?", "A careful hand wash with clean media avoids the spinning brushes and recycled water that cause swirl marks on many automatic washes."),
            ("Do you need water and power at my house?", "Tell us what the location offers when you book. We plan the setup around the available water and access."),
            ("Can I add an interior clean?", "Yes. Many customers combine a wash with interior vacuuming or choose the Full Reset for inside and outside."),
            ("What if it rains?", "We reschedule when rain would compromise the wash and finish."),
        ],
        "related": ["exterior", "full-reset", "car-waxing"],
    },
}

SERVICE_NAMES = dict(EXISTING_SERVICES)
SERVICE_NAMES.update({k: v["name"] for k, v in NEW_SERVICES.items()})
ALL_SERVICE_SLUGS = [s for s, _ in EXISTING_SERVICES] + list(NEW_SERVICES)

# ---------------------------------------------------------------- areas
# (slug, display, url, lat, lon, region)
AREAS = [
    ("sugar-land", "Sugar Land", "/sugar-land", 29.619, -95.635, "core"),
    ("first-colony", "First Colony", "/areas/first-colony", 29.598, -95.615, "core"),
    ("telfair", "Telfair", "/areas/telfair", 29.585, -95.600, "core"),
    ("riverstone", "Riverstone", "/areas/riverstone", 29.545, -95.640, "core"),
    ("new-territory", "New Territory", "/areas/new-territory", 29.650, -95.700, "core"),
    ("greatwood", "Greatwood", "/areas/greatwood", 29.600, -95.730, "core"),
    ("stafford", "Stafford", "/areas/stafford", 29.616, -95.557, "core"),
    ("missouri-city", "Missouri City", "/areas/missouri-city", 29.618, -95.538, "core"),
    ("sienna", "Sienna", "/areas/sienna", 29.505, -95.520, "core"),
    ("meadows-place", "Meadows Place", "/areas/meadows-place", 29.668, -95.585, "core"),
    ("four-corners", "Four Corners", "/areas/four-corners", 29.655, -95.610, "core"),
    ("richmond", "Richmond", "/areas/richmond", 29.582, -95.760, "west"),
    ("pecan-grove", "Pecan Grove", "/areas/pecan-grove", 29.627, -95.775, "west"),
    ("aliana", "Aliana", "/areas/aliana", 29.689, -95.739, "west"),
    ("rosenberg", "Rosenberg", "/areas/rosenberg", 29.557, -95.809, "west"),
    ("thompsons", "Thompsons", "/areas/thompsons", 29.482, -95.600, "west"),
    ("fulshear", "Fulshear", "/areas/fulshear", 29.690, -95.900, "west"),
    ("cinco-ranch", "Cinco Ranch", "/areas/cinco-ranch", 29.730, -95.760, "west"),
    ("katy", "Katy", "/katy", 29.786, -95.824, "west"),
    ("mission-bend", "Mission Bend", "/areas/mission-bend", 29.690, -95.660, "west"),
    ("fresno", "Fresno", "/areas/fresno", 29.550, -95.460, "south"),
    ("arcola", "Arcola", "/areas/arcola", 29.500, -95.460, "south"),
    ("pearland", "Pearland", "/pearland", 29.563, -95.286, "south"),
    ("needville", "Needville", "/areas/needville", 29.400, -95.840, "south"),
    ("booth", "Booth", "/areas/booth", 29.590, -95.740, "south"),
    ("simonton", "Simonton", "/areas/simonton", 29.690, -95.980, "south"),
    ("beasley", "Beasley", "/areas/beasley", 29.500, -95.920, "south"),
    ("orchard", "Orchard", "/areas/orchard", 29.600, -95.960, "south"),
    ("houston", "Houston", "/areas/houston", 29.707, -95.590, "metro"),
    ("sharpstown", "Sharpstown", "/areas/sharpstown", 29.690, -95.520, "metro"),
    ("crabb", "Crabb", "/areas/crabb", 29.545, -95.760, "west"),
    ("fort-bend-county", "Fort Bend County", "/areas/fort-bend-county", 29.520, -95.770, "core"),
    ("cypress", "Cypress", "/cypress", 29.969, -95.697, "metro"),
    ("the-woodlands", "The Woodlands", "/the-woodlands", 30.165, -95.461, "metro"),
]
AREA_BY_SLUG = {a[0]: a for a in AREAS}
REGIONS = [
    ("core", "Sugar Land and central Fort Bend"),
    ("west", "Richmond, Rosenberg, Fulshear, Katy and the west side"),
    ("south", "Pearland, Fresno, Arcola and rural Fort Bend"),
    ("metro", "Greater Houston"),
]
EXISTING_AREA_SLUGS = {"sugar-land", "katy", "pearland", "cypress", "the-woodlands", "new-territory", "greatwood"}


def dist(a, b):
    return math.hypot(a[3] - b[3], (a[4] - b[4]) * 0.87)


def neighbors(slug, n=6):
    me = AREA_BY_SLUG[slug]
    others = sorted((a for a in AREAS if a[0] != slug), key=lambda a: dist(me, a))
    return others[:n]


# ---------------------------------------------------------------- shared html pieces
def base_nodes():
    base = BeautifulSoup((ROOT / "services/interior.html").read_text(), "html.parser")
    header = str(base.header)
    footer = str(base.footer)
    mobile = str(base.select_one(".mobile-bar"))
    return header, footer, mobile


AREA_LIST_FOR_SCHEMA = [a[1] for a in AREAS]


def business_node():
    return {
        "@type": "AutoWash",
        "@id": f"{SITE}/#business",
        "name": "Sugar Land Car Detailing",
        "url": f"{SITE}/",
        "telephone": "+1-346-489-2266",
        "priceRange": "$$",
        "hasMap": "https://www.google.com/maps?cid=4001523659056233645",
        "address": {"@type": "PostalAddress", "streetAddress": "18726 University Blvd", "addressLocality": "Sugar Land", "addressRegion": "TX", "postalCode": "77479", "addressCountry": "US"},
        "areaServed": [{"@type": "City", "name": f"{n}, TX"} for n in AREA_LIST_FOR_SCHEMA],
        "makesOffer": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": SERVICE_NAMES[s], "url": f"{SITE}/services/{s}"}} for s in ALL_SERVICE_SLUGS
        ],
    }


def website_node():
    return {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "Sugar Land Car Detailing", "publisher": {"@id": f"{SITE}/#business"}}


def head(title, desc, url, graph, image):
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return (
        f'<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title>'
        f'<meta name="description" content="{e(desc, quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large">'
        f'<link rel="canonical" href="{url}"><meta property="og:type" content="website"><meta property="og:title" content="{e(title, quote=True)}">'
        f'<meta property="og:description" content="{e(desc, quote=True)}"><meta property="og:url" content="{url}">'
        f'<meta property="og:image" content="{SITE}/assets/{image}.jpg"><meta name="twitter:card" content="summary_large_image">'
        '<link rel="icon" href="/assets/favicon.svg"><link rel="preload" href="/assets/fonts/barlow-800.woff2" as="font" type="font/woff2" crossorigin>'
        '<link rel="preload" href="/assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>'
        '<link rel="stylesheet" href="/fonts.css"><link rel="stylesheet" href="/styles.css"><link rel="stylesheet" href="/header-contrast.css">'
        '<link rel="stylesheet" href="/content-pages.css"><link rel="stylesheet" href="/portfolio-components.css">'
        f'<script type="application/ld+json">{ld}</script></head>'
    )


def img_tag(name, alt="Illustrative vehicle care photography"):
    return (
        f'<img class="subhero-media" src="/assets/{name}-800.webp" alt="{alt}" width="799" height="533" decoding="async" '
        f'srcset="/assets/{name}-480.webp 480w, /assets/{name}-800.webp 799w, /assets/{name}-1200.webp 1200w, /assets/{name}-1600.webp 1600w" sizes="100vw" fetchpriority="high">'
    )


def hero(crumbs, eyebrow, h1, lead, image):
    return (
        f'<section class="subhero">{img_tag(image)}<div class="subhero-shade" aria-hidden="true"></div><div class="subhero-content">'
        f'<nav class="crumbs" aria-label="Breadcrumb">{crumbs}</nav><p class="eyebrow"><span></span>{e(eyebrow)}</p><h1>{e(h1)}</h1>'
        f'<p class="subhero-lead">{e(lead)}</p><div class="hero-actions"><a class="button button-call" href="{PHONE_HREF}">Call {PHONE.replace("+1 ", "")}</a>'
        f'<a class="button button-book" href="{BOOK}">Book online</a></div></div></section>'
    )


def cta(kicker, h2, p):
    return (
        f'<section class="quote section"><div class="quote-copy"><p class="section-kicker light">{e(kicker)}</p><h2>{e(h2)}</h2><p>{e(p)}</p></div>'
        f'<div class="call-card"><a class="button button-call call-button" href="{PHONE_HREF}">Call {PHONE.replace("+1 ", "")}</a>'
        f'<a class="button button-book call-button" href="{BOOK}">Book online</a></div></section>'
    )


def faq_section(kicker, h2, faqs):
    items = "".join(f"<details><summary>{e(q)}<span>+</span></summary><p>{e(a)}</p></details>" for q, a in faqs)
    return f'<section class="faq section"><div><p class="section-kicker">{e(kicker)}</p><h2>{e(h2)}</h2></div><div class="accordion">{items}</div></section>'


def text_section(kicker, h2, paras, extra=""):
    body = "".join(f"<p>{p}</p>" for p in paras)
    return f'<section class="service-area-links section"><p class="section-kicker">{e(kicker)}</p><h2>{e(h2)}</h2>{body}{extra}</section>'


def write(path, content):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def page(title, desc, url, graph, image, main, nodes):
    header, footer, mobile = nodes
    return (
        f'<!doctype html><html lang="en">{head(title, desc, url, graph, image)}<body><a class="skip-link" href="#main">Skip to content</a>'
        f'{header}<main id="main">{main}</main>{footer}{mobile}<script src="/script.js" defer></script><script src="/portfolio-components.js" defer></script></body></html>'
    )


def breadcrumb_graph(url, trail):
    return {
        "@type": "BreadcrumbList",
        "@id": url + "#breadcrumb",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(trail)],
    }


# ---------------------------------------------------------------- service pages
def build_service(slug, s, nodes):
    url = f"{SITE}/services/{slug}"
    crumbs = f'<a href="/">Home</a><span>/</span><a href="/services">Services</a><span>/</span>{e(s["name"])}'
    included = "".join(f"<li>{e(i)}</li>" for i in s["included"])
    related = "".join(
        f'<a class="related-card" href="/services/{r}"><span>Related service</span><h3>{e(SERVICE_NAMES[r])}</h3><strong>Review the service ↗</strong></a>' for r in s["related"]
    )
    area_links = "".join(f'<a href="{a[2]}">{e(a[1])}</a> · ' for a in AREAS[:12]).rstrip(" · ")
    main = (
        hero(crumbs, s["eyebrow"], s["h1"], s["lead"], s["image"])
        + f'<section class="service-detail section"><div class="service-detail-main"><p class="section-kicker">What the service covers</p><h2>What is included in {e(s["name"].lower())}.</h2><ul class="check-list">{included}</ul></div>'
        f'<aside class="service-quote-panel"><p class="panel-label">Vehicle-specific scope</p><h3>Every vehicle gets its own quote.</h3><p>{e(s["cost"])}</p><a href="/pricing">Review packages and pricing ↗</a></aside></section>'
        + text_section("Suitability and limits", s["limits_h"], [e(s["limits"])])
        + text_section("Before the visit", s["prep_h"], [e(s["prep"]), e(s["local"]) + ' See the <a href="/areas">full list of areas we serve</a>.'])
        + faq_section("Customer questions", f'{s["name"]}: questions before you book.', s["faqs"])
        + f'<section class="related section"><div class="section-head"><div><p class="section-kicker">Compare the options</p><h2>Pair it with the right service.</h2></div><p>Combine work only after the included checklist and quote are confirmed.</p></div><div class="related-grid">{related}</div></section>'
        + f'<section class="service-area-links section"><p class="section-kicker">Where we work</p><h2>{e(s["name"])} near you.</h2><p>We bring mobile detailing across Sugar Land and nearby communities: {area_links} and <a href="/areas">more</a>.</p></section>'
        + cta("Describe the vehicle first", "Confirm the work and the location.", "Call with the vehicle details, condition, requested service and appointment setting.")
    )
    graph = [
        business_node(),
        website_node(),
        {
            "@type": "WebPage", "@id": url + "#webpage", "url": url, "name": s["title"], "description": s["desc"], "inLanguage": "en-US",
            "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": f"{SITE}/#business"},
            "mainEntity": {"@id": url + "#service"}, "breadcrumb": {"@id": url + "#breadcrumb"},
        },
        {
            "@type": "Service", "@id": url + "#service", "url": url, "name": s["name"], "serviceType": s["name"], "description": s["desc"],
            "provider": {"@id": f"{SITE}/#business"},
            "areaServed": [{"@type": "City", "name": f"{n}, TX"} for n in AREA_LIST_FOR_SCHEMA],
            "mainEntityOfPage": {"@id": url + "#webpage"},
        },
        breadcrumb_graph(url, [("Home", f"{SITE}/"), ("Services", f"{SITE}/services"), (s["name"], url)]),
    ]
    write(f"services/{slug}.html", page(s["title"], s["desc"], url, graph, s["image"], main, nodes))


# ---------------------------------------------------------------- area pages
SERVICE_ANGLE_KEYS = [
    ("interior", "interior", "Interior detailing"),
    ("exterior", "exterior", "Exterior detailing"),
    ("full", "full-reset", "Full interior + exterior detail"),
    ("ceramic", "ceramic-coating", "Ceramic coating"),
    ("correction", "paint-correction", "Buffing & paint correction"),
    ("wax", "car-waxing", "Car waxing"),
]


DIST = re.compile(r"[^.]*\b\d+(?:-\d+)?\s*(?:miles?|minutes?|mi)\b[^.]*\.\s*", re.I)


def clean(o):
    if isinstance(o, str):
        n = DIST.sub("", o).strip()
        return n or o
    if isinstance(o, list):
        return [clean(x) for x in o]
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    return o


def build_area(c, nodes):
    c = clean(c)
    slug, name = c["slug"], c["name"]
    url = f"{SITE}/areas/{slug}"
    places = c.get("places", [])
    title = f"Mobile Car Detailing in {name}, TX | Sugar Land Car Detailing"
    if len(title) > 66:
        title = f"Mobile Car Detailing in {name}, TX"
    desc = (
        f"Mobile car detailing in {name}, TX: interior, exterior, ceramic coating, paint correction and waxing at your home or workplace. Call {PHONE.replace('+1 ', '')}."
    )
    crumbs = f'<a href="/">Home</a><span>/</span><a href="/areas">Areas</a><span>/</span>{e(name)}'
    chips = "".join(f"<li>{e(p)}</li>" for p in places)
    cards = "".join(
        f'<article><h3><a href="/services/{svc}">{e(label)} in {e(name)}</a></h3><p>{e(c["service_angles"][key])}</p></article>'
        for key, svc, label in SERVICE_ANGLE_KEYS
    )
    more_services = "".join(
        f'<li><a href="/services/{s}">{e(SERVICE_NAMES[s])} in {e(name)}</a></li>'
        for s in ["headlight-restoration", "pet-hair-removal", "odor-removal", "mobile-car-wash", "clay-bar-treatment", "seat-shampooing", "steam-cleaning", "engine-detailing"]
    )
    near = "".join(f'<li><a href="{a[2]}">Car detailing in {e(a[1])}</a></li>' for a in neighbors(slug))
    faqs = [(f["q"], f["a"]) for f in c["faqs"]] + [
        (f"Do you come to {name}?", f"Yes. Sugar Land Car Detailing is a mobile service that travels to {name} homes and workplaces. Call {PHONE.replace('+1 ', '')} or book online with your address and vehicle."),
        (f"Can I book ceramic coating or paint correction in {name}?", f"Yes, ask about ceramic coating, buffing and paint correction when you call. We review the paint and the {name} location, then confirm scope and quote before the visit."),
    ]
    main = (
        hero(crumbs, f"{name}, Texas · Mobile detailing", f"Mobile Car Detailing in {name}, TX", c["intro"], "service-full")
        + text_section(f"Serving {name}", f"Where we work in and around {name}", [e(c["geo"])], f'<ul class="check-list">{chips}</ul>' if chips else "")
        + text_section("Local conditions", f"What {name} does to your car", [e(c["conditions"])])
        + f'<section class="service-area-links section"><p class="section-kicker">Services</p><h2>Car detailing services for {e(name)} drivers.</h2><div class="service-cards">{cards}</div></section>'
        + f'<section class="service-area-links section"><p class="section-kicker">More services</p><h2>Also available in {e(name)}.</h2><ul class="check-list">{more_services}</ul></section>'
        + text_section("Arranging the visit", f"Booking a detail in {name}", [e(c["access"])])
        + faq_section("Before you book", f"{name} car detailing questions.", faqs)
        + f'<section class="service-area-links section"><p class="section-kicker">Nearby</p><h2>More areas we serve near {e(name)}.</h2><ul class="check-list">{near}</ul><p><a href="/areas">See every area we serve</a> · <a href="/services">Compare all detailing services</a> · <a href="/pricing">Pricing</a></p></section>'
        + cta(f"Detailing in {name}", f"Book mobile detailing in {name}.", f"Call {PHONE.replace('+1 ', '')} or book online with your {name} address, vehicle and the service you want.")
    )
    graph = [
        business_node(),
        website_node(),
        {
            "@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc, "inLanguage": "en-US",
            "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": f"{SITE}/#business"},
            "spatialCoverage": {"@type": "Place", "name": f"{name}, TX"}, "breadcrumb": {"@id": url + "#breadcrumb"},
        },
        {
            "@type": "Service", "@id": url + "#service", "url": url, "name": f"Mobile car detailing in {name}, TX", "serviceType": "Mobile car detailing",
            "provider": {"@id": f"{SITE}/#business"}, "areaServed": {"@type": "City", "name": f"{name}, TX"},
        },
        breadcrumb_graph(url, [("Home", f"{SITE}/"), ("Areas", f"{SITE}/areas"), (name, url)]),
    ]
    write(f"areas/{slug}.html", page(title, desc, url, graph, "service-full", main, nodes))


def build_hub(nodes):
    url = f"{SITE}/areas"
    title = "Mobile Car Detailing Service Areas | Sugar Land & Fort Bend"
    desc = "Mobile car detailing across Sugar Land, Stafford, Missouri City, Richmond, Rosenberg, Katy, Pearland and 30 nearby Texas communities. Find your area."
    blocks = ""
    for key, label in REGIONS:
        links = "".join(f'<li><a href="{a[2]}">Car detailing in {e(a[1])}, TX</a></li>' for a in AREAS if a[5] == key)
        blocks += f'<section class="service-area-links section"><p class="section-kicker">Service areas</p><h2>{e(label)}</h2><ul class="check-list">{links}</ul></section>'
    svc = "".join(f'<li><a href="/services/{s}">{e(SERVICE_NAMES[s])}</a></li>' for s in ALL_SERVICE_SLUGS)
    crumbs = '<a href="/">Home</a><span>/</span>Areas'
    lead = "Sugar Land Car Detailing is based at 18726 University Blvd in Sugar Land and travels to customers across Fort Bend County and the Greater Houston area. Find your community below for local detailing information, then call or book online."
    main = (
        hero(crumbs, "Service areas · Greater Houston", "Mobile Car Detailing Service Areas", lead, "service-full")
        + blocks
        + f'<section class="service-area-links section"><p class="section-kicker">Services</p><h2>Every service we offer.</h2><ul class="check-list">{svc}</ul></section>'
        + cta("Not sure we cover you?", "Ask about your address.", "Call or book online with your location. If it is outside the list, ask anyway.")
    )
    graph = [
        business_node(),
        website_node(),
        {"@type": "CollectionPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc, "inLanguage": "en-US", "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": f"{SITE}/#business"}, "breadcrumb": {"@id": url + "#breadcrumb"}},
        breadcrumb_graph(url, [("Home", f"{SITE}/"), ("Areas", url)]),
    ]
    write("areas/index.html", page(title, desc, url, graph, "service-full", main, nodes))


# ---------------------------------------------------------------- global patches
def patch_all_pages():
    """Nav + footer links, services hub cards, sitemap page, expanded schema. Idempotent."""
    pages = [p for p in ROOT.rglob("*.html") if ".git" not in p.parts and ".vercel" not in p.parts and "_seo-research" not in p.parts]
    service_links = "".join(f'<a href="/services/{s}">{e(n)}</a>' for s, n in EXISTING_SERVICES[:3]) + "".join(f'<a href="/services/{s}">{e(v["name"])}</a>' for s, v in NEW_SERVICES.items())
    for p in pages:
        t = p.read_text()
        o = t
        # cleanup: stray hub link in header, duplicate homepage-anchor Areas link
        head_part, sep, rest = t.partition("<main")
        head_part = head_part.replace('<a href="/areas">All service areas</a>', "")
        if 'href="/areas">Areas</a>' in head_part:
            head_part = head_part.replace('<a href="/#areas">Areas</a>', "")
        t = head_part + sep + rest
        # header nav: add Areas hub link
        if 'href="/areas"' not in t.split("<main")[0]:
            t = re.sub(r'(<a href="/pricing"[^>]*>Pricing</a>)', r'\1<a href="/areas">Areas</a>', t, count=1)
        # footer explore: add areas hub
        if '<nav aria-label="Footer navigation">' in t and 'Footer navigation"><a href="/">Home</a><a href="/areas">' not in t:
            t = t.replace('Footer navigation"><a href="/">Home</a>', 'Footer navigation"><a href="/">Home</a><a href="/areas">All service areas</a>', 1)
        # footer services list: all services
        t = re.sub(
            r'(<nav aria-label="Service pages">)(.*?)(</nav>)',
            lambda m: m.group(1) + '<!--SVC-FOOT-->' + service_links + m.group(3) if "<!--SVC-FOOT-->" not in m.group(2) else m.group(0),
            t, count=1, flags=re.S,
        )
        # JSON-LD business node: broaden areaServed + offers
        def fix_ld(m):
            try:
                data = json.loads(m.group(1))
            except Exception:
                return m.group(0)
            changed = False
            for node in data.get("@graph", []):
                if node.get("@type") == "AutoWash" and node.get("@id", "").endswith("#business"):
                    full = business_node()
                    if node.get("areaServed") != full["areaServed"]:
                        node["areaServed"] = full["areaServed"]
                        node["makesOffer"] = full["makesOffer"]
                        node["hasMap"] = full["hasMap"]
                        changed = True
            if not changed:
                return m.group(0)
            return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"
        t = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix_ld, t, flags=re.S)
        if t != o:
            p.write_text(t)


def patch_services_hub():
    p = ROOT / "services/index.html"
    t = p.read_text()
    if "NEW-SERVICE-CARDS" in t:
        return
    cards = "".join(
        f'<article><h2>{e(v["name"])}</h2><p>{e(v["desc"])}</p><a href="/services/{k}">Explore {e(v["name"].lower())}</a></article>' for k, v in NEW_SERVICES.items()
    )
    block = f'<!--NEW-SERVICE-CARDS--><section class="pilot-section"><h2>Protection, correction and specialty cleaning</h2><p>Ceramic coating, buffing and paint correction, headlight restoration, pet hair and odor removal, and mobile hand washing. Confirm the scope and quote for your vehicle before booking.</p><div class="service-cards">{cards}</div></section>'
    t = t.replace('<section class="pilot-section tone">', block + '<section class="pilot-section tone">', 1)
    t = t.replace("Compare Full Reset, Interior Reset, and Exterior Refresh.", "Compare interior, exterior, full detailing, ceramic coating, paint correction, waxing and more.", 1)
    p.write_text(t)


def patch_html_sitemap():
    p = ROOT / "sitemap/index.html"
    t = p.read_text()
    if "NEW-SITEMAP" in t:
        return
    svc = "".join(f'<li><a href="/services/{k}">{e(v["name"])}</a></li>' for k, v in NEW_SERVICES.items())
    t = t.replace('<li><a href="/pricing">Packages and pricing</a></li>', svc + '<li><a href="/pricing">Packages and pricing</a></li><!--NEW-SITEMAP-->', 1)
    areas = "".join(f'<li><a href="{a[2]}">{e(a[1])}</a></li>' for a in AREAS if a[0] not in EXISTING_AREA_SLUGS)
    t = t.replace("<h2>Area guides</h2>", '<h2>Area guides</h2><p><a href="/areas">All service areas</a></p>', 1)
    t = t.replace('<li><a href="/pearland">Pearland</a></li>', '<li><a href="/pearland">Pearland</a></li>' + areas, 1)
    p.write_text(t)


def patch_service_area_links():
    """Add a 'nearby cities' block to existing service pages."""
    block_html = '<section class="service-area-links section" id="service-areas-served"><p class="section-kicker">Where we work</p><h2>Serving Sugar Land and nearby cities.</h2><p>' + " · ".join(
        f'<a href="{a[2]}">{e(a[1])}</a>' for a in AREAS[:14]
    ) + ' · <a href="/areas">see all areas</a></p></section>'
    for slug in [s for s, _ in EXISTING_SERVICES]:
        p = ROOT / "services" / f"{slug}.html"
        t = p.read_text()
        if 'id="service-areas-served"' in t:
            continue
        # add cross-links to new services
        marker = '<section class="faq section"'
        if marker in t:
            t = t.replace(marker, block_html + marker, 1)
            p.write_text(t)


def patch_homepage():
    p = ROOT / "index.html"
    t = p.read_text()
    if 'id="home-areas-served"' in t:
        return
    areas = " · ".join(f'<a href="{a[2]}">{e(a[1])}</a>' for a in AREAS)
    svc = " · ".join(f'<a href="/services/{s}">{e(SERVICE_NAMES[s])}</a>' for s in ALL_SERVICE_SLUGS)
    block = (
        '<section class="service-area-links section" id="home-areas-served"><p class="section-kicker">Service areas</p><h2>Mobile car detailing across Sugar Land and Fort Bend County.</h2>'
        f'<p>{areas}</p><p class="section-kicker">All services</p><p>{svc}</p></section>'
    )
    marker = '<section class="faq section"'
    if marker in t:
        t = t.replace(marker, block + marker, 1)
    else:
        t = t.replace("</main>", block + "</main>", 1)
    p.write_text(t)


# ---------------------------------------------------------------- sitemap + llms
def write_sitemap():
    state_path = ROOT / ".sitemap-state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    urls = {}
    for p in sorted(ROOT.rglob("*.html")):
        if any(part in {".git", ".vercel", "_seo-research", "node_modules"} for part in p.parts):
            continue
        rel = p.relative_to(ROOT).as_posix()
        if rel == "index.html":
            path = "/"
        elif rel.endswith("/index.html"):
            path = "/" + rel[: -len("/index.html")]
        else:
            path = "/" + rel[:-5]
        url = SITE + path
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        prev = state.get(url)
        lastmod = prev["lastmod"] if prev and prev["sha256"] == digest else TODAY
        state[url] = {"sha256": digest, "lastmod": lastmod}
        urls[url] = lastmod
    state_path.write_text(json.dumps(state, indent=2))
    body = "".join(f"  <url><loc>{u}</loc><lastmod>{urls[u]}</lastmod></url>\n" for u in sorted(urls))
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "</urlset>\n")
    return len(urls)


def write_llms():
    lines = [
        "# Sugar Land Car Detailing",
        "",
        "> Appointment-based mobile car detailing in Sugar Land, Texas, serving Fort Bend County and Greater Houston.",
        "",
        "## Verified business facts",
        "- Business name: Sugar Land Car Detailing",
        "- Address: 18726 University Blvd, Sugar Land, TX 77479",
        "- Telephone: +1 346-489-2266",
        "- Service: Appointment-based mobile car detailing (we travel to the customer)",
        "- Booking: https://cal.com/sumitdatta/auto-detail-service",
        "- Google review profile: https://g.page/r/Ca08XiKRRIg3EBM/review",
        "",
        "## Primary pages",
        f"- [Homepage]({SITE}/)",
        f"- [Services]({SITE}/services)",
        f"- [Pricing]({SITE}/pricing)",
        f"- [Service areas]({SITE}/areas)",
        f"- [About]({SITE}/about)",
        f"- [Contact]({SITE}/contact)",
        "",
        "## Services",
    ]
    for s in ALL_SERVICE_SLUGS:
        lines.append(f"- [{SERVICE_NAMES[s]}]({SITE}/services/{s})")
    lines += ["", "## Service areas"]
    for a in AREAS:
        lines.append(f"- [{a[1]}, TX]({SITE}{a[2]})")
    (ROOT / "llms.txt").write_text("\n".join(lines) + "\n")


def main():
    patch_all_pages()  # nav/footer/schema first so cloned header/footer are current
    nodes = base_nodes()
    for slug, s in NEW_SERVICES.items():
        build_service(slug, s, nodes)
    content_dir = ROOT / "_seo-research" / "content"
    built = 0
    for a in AREAS:
        if a[0] in EXISTING_AREA_SLUGS:
            continue
        f = content_dir / f"{a[0]}.json"
        if not f.exists():
            print("MISSING content:", a[0])
            continue
        build_area(json.loads(f.read_text()), nodes)
        built += 1
    build_hub(nodes)
    patch_all_pages()  # new pages get nav/schema parity
    patch_services_hub()
    patch_html_sitemap()
    patch_service_area_links()
    patch_homepage()
    n = write_sitemap()
    write_llms()
    print(f"services {len(NEW_SERVICES)}, areas {built}, sitemap urls {n}")


if __name__ == "__main__":
    main()
