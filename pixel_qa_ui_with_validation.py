
import streamlit as st
import asyncio
from urllib.parse import urlparse, parse_qs
from playwright.async_api import async_playwright

# Define pixel domains and parameters to validate
PIXEL_RULES = {
    "facebook.com/tr": ["ev", "dl", "id"],  # Meta Pixel
    "googleads.g.doubleclick.net": ["gclid", "label", "value"],  # Google Ads
    "analytics.google.com": ["tid", "cid"],  # Google Analytics
    "tiktok.com": ["pixel_id", "event", "value"],
    "snapchat.com": ["id", "event_type", "amount"],
    "linkedin.com": ["conversionId", "event"],
}

async def check_pixels_and_params(url):
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        pixel_hits = []

        async def log_request(request):
            req_url = request.url
            for domain, required_params in PIXEL_RULES.items():
                if domain in req_url:
                    parsed = urlparse(req_url)
                    qs = parse_qs(parsed.query)
                    missing = [p for p in required_params if p not in qs]
                    status = "✅ All parameters present" if not missing else f"❌ Missing parameters: {', '.join(missing)}"
                    pixel_hits.append((domain, req_url, status))

        page.on("request", log_request)

        try:
            await page.goto(url, timeout=60000)
            await page.wait_for_timeout(5000)
        except Exception as e:
            results.append(f"Error loading page: {e}")

        if pixel_hits:
            for domain, hit_url, status in pixel_hits:
                results.append(f"[{domain}] {status}\\n-> {hit_url}")
-> {hit_url}")
        else:
            results.append("No pixels detected.")

        await browser.close()
    return results

st.title("Pixel QA Checker with Parameter Validation")

url_input = st.text_input("Enter the URL to scan for ad pixels:")

if st.button("Run Pixel Check"):
    if url_input:
        st.write("Scanning... please wait.")
        results = asyncio.run(check_pixels_and_params(url_input))
        st.subheader("Results")
        for res in results:
            st.write(res)
    else:
        st.warning("Please enter a valid URL.")
