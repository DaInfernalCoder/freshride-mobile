import { chromium } from "/Users/sumit/.agents/skills/web-clone/node_modules/playwright-core/index.mjs";
import fs from "node:fs/promises";

const base = (process.env.BASE_URL || "http://127.0.0.1:4173").replace(/\/$/, "");
const chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const output = process.env.QA_OUTPUT || "/private/tmp/freshride-visual-qa";
const pages = [
  ["home", "/index.html"],
  ["pricing", "/pricing.html"],
  ["interior", "/services/interior.html"],
  ["katy", "/katy.html"],
];

await fs.mkdir(output, { recursive: true });
const browser = await chromium.launch({ headless: true, executablePath: chrome });
const failures = [];

for (const [name, path] of pages) {
  for (const [size, viewport] of [
    ["desktop", { width: 1440, height: 1000 }],
    ["mobile", { width: 390, height: 844 }],
  ]) {
    const context = await browser.newContext({ viewport, deviceScaleFactor: 1 });
    const page = await context.newPage();
    const consoleErrors = [];
    const pageErrors = [];
    const externalFonts = [];
    page.on("console", (message) => message.type() === "error" && consoleErrors.push(message.text()));
    page.on("pageerror", (error) => pageErrors.push(String(error)));
    page.on("request", (request) => /fonts\.(googleapis|gstatic)\.com/.test(request.url()) && externalFonts.push(request.url()));
    const response = await page.goto(base + path, { waitUntil: "networkidle" });
    if (!response?.ok()) failures.push(`${name}/${size}: HTTP ${response?.status()}`);
    const checks = await page.evaluate(() => ({
      h1: document.querySelectorAll("h1").length,
      overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      title: document.title,
      navVisible: getComputedStyle(document.querySelector(".site-header")).backgroundColor,
      callLinks: document.querySelectorAll('a[href^="tel:+13464892266"]').length,
      bookLinks: document.querySelectorAll('a[href="https://cal.com/sumitdatta/auto-detail-service"]').length,
    }));
    if (checks.h1 !== 1) failures.push(`${name}/${size}: H1 count ${checks.h1}`);
    if (checks.overflow > 1) failures.push(`${name}/${size}: horizontal overflow ${checks.overflow}px`);
    if (!checks.title) failures.push(`${name}/${size}: empty title`);
    if (checks.callLinks < 1) failures.push(`${name}/${size}: no call link`);
    if (checks.bookLinks < 1) failures.push(`${name}/${size}: no booking link`);
    if (consoleErrors.length) failures.push(`${name}/${size}: console ${consoleErrors.join(" | ")}`);
    if (pageErrors.length) failures.push(`${name}/${size}: pageerror ${pageErrors.join(" | ")}`);
    if (externalFonts.length) failures.push(`${name}/${size}: external font requests remain`);
    await page.screenshot({ path: `${output}/${name}-${size}.png`, fullPage: false });

    if (size === "mobile") {
      const toggle = page.locator(".nav-toggle");
      await toggle.click();
      const expanded = await toggle.getAttribute("aria-expanded");
      const menuVisible = await page.locator("#site-nav").isVisible();
      if (expanded !== "true" || !menuVisible) failures.push(`${name}/mobile: menu did not open`);
      await page.screenshot({ path: `${output}/${name}-mobile-menu.png`, fullPage: false });
    }
    await context.close();
  }
}

await browser.close();
if (failures.length) {
  console.error("VISUAL QA FAILED");
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}
console.log(`VISUAL QA OK — ${pages.length} pages at desktop/mobile; screenshots: ${output}`);
