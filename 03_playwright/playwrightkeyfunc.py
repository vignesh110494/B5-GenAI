import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Open Playwright docs
        await page.goto(
            "https://playwright.dev/python/docs/intro",
            timeout=60000
        )

        # Wait for main content
        await page.wait_for_selector("main", timeout=60000)

        # Extract title
        title = await page.title()

        # Extract meta description
        meta_desc = await page.evaluate("""
            () => {
                const meta = document.querySelector("meta[name='description']");
                return meta ? meta.content : "No description";
            }
        """)

        # Extract documentation content
        content = await page.evaluate("""
            () => document.querySelector("main").innerText
        """)

        # Save to Notepad file
        with open("playwright_notes.txt", "w", encoding="utf-8") as f:
            f.write(f"""
PLAYWRIGHT PYTHON NOTES
======================

TITLE:
{title}

META DESCRIPTION:
{meta_desc}

CONTENT:
{content}
""")

        print("✅ Data extracted and saved successfully")
        print("⏳ Browser will close after 10 seconds...")

        # ✅ WAIT FOR 10 SECONDS BEFORE CLOSING
        await page.wait_for_timeout(10_000)

        await browser.close()

asyncio.run(main())
