# from flask import Flask

# app = Flask(__name__)

# @app.route('/')

# def hello():
#     return "Hello, Flask!"


# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, jsonify
import asyncio
from playwright.async_api import async_playwright

app = Flask(__name__)


async def run_playwright():
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

        # Save to file
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

        # Wait 10 seconds before closing
        await page.wait_for_timeout(10_000)
        await browser.close()

        return {
            "title": title,
            "meta_description": meta_desc,
            "status": "Data extracted and saved successfully"
        }


@app.route("/extract", methods=["GET"])
def extract_data():
    result = asyncio.run(run_playwright())
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
