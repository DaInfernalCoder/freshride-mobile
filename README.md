# Fresh Ride Mobile

Marketing site for [freshridemobile.shop](https://freshridemobile.shop), a mobile auto detailing service.

## Local preview

```bash
npx serve .
```

The site is dependency-free HTML, CSS, and JavaScript and deploys directly to Vercel.

Generated pages are committed. Rebuild after editing the source data:

```bash
python3 build_pages.py
python3 build_content_pages.py
```

## Site map

- `/` — Houston/Greater Houston homepage
- `/pricing` — quote logic and pricing factors
- `/services/full-reset` — interior + exterior service
- `/services/interior` — interior service
- `/services/exterior` — exterior service
- `/katy`, `/sugar-land`, `/the-woodlands`, `/cypress`, `/pearland` — differentiated service-area pages
- `/llms.txt`, `/robots.txt`, `/sitemap.xml` — crawler discovery and GEO guidance

## Photography

Launch photography is sourced from Unsplash under the Unsplash License. Replace with original Fresh Ride work as the portfolio grows.

The website labels the images as representative launch photography and does not present them as completed Fresh Ride jobs.

## Typography

Barlow Condensed and Manrope are self-hosted under the SIL Open Font License. License files are stored in `assets/fonts/`.
