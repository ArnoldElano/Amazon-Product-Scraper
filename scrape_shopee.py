"""Save visible Amazon product links to CSV.

Install with:
    python3 -m pip install playwright
    python3 -m playwright install chromium

Run with:
    python3 scrape_shopee.py
    python3 scrape_shopee.py --max-items 30 --output product_links.csv
"""

import argparse
import csv
import re
import sys
from pathlib import Path
from urllib.parse import urljoin

try:
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
    from playwright.sync_api import sync_playwright
except ImportError:
    print(
        "Missing dependency. Install it with: "
        "python3 -m pip install playwright",
        file=sys.stderr,
    )
    raise SystemExit(1)


URL = "https://www.amazon.com/s?k=desktop+computers"
FIELDS = ("link",)
PRODUCT_PATH_RE = re.compile(r"/dp/([A-Z0-9]{10})(?:[/?#]|$)", re.IGNORECASE)


def extract_products(page):
    products = []
    anchors = page.locator("a[href]")
    for index in range(anchors.count()):
        href = anchors.nth(index).get_attribute("href")
        match = PRODUCT_PATH_RE.search(href or "")
        if match:
            products.append(
                {"link": urljoin(URL, f"/dp/{match.group(1).upper()}")}
            )
    return products


def main():
    parser = argparse.ArgumentParser(
        description="Save visible Amazon product links into a CSV file."
    )
    parser.add_argument(
        "--max-items", type=int, default=60, help="Maximum listings to collect."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("amazon_product_links.csv"),
        help="CSV path.",
    )
    args = parser.parse_args()

    if args.max_items < 1:
        parser.error("--max-items must be at least 1")

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page(locale="en-PH")
            page.goto(URL, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(3000)

            page_text = page.locator("body").inner_text()
            if (
                "robot check" in page_text.lower()
                or "captcha" in page_text.lower()
                or "validatecaptcha" in page.url.lower()
            ):
                raise RuntimeError(
                    "Amazon showed a CAPTCHA or robot-check page. "
                    "The script will not bypass that restriction."
                )

            products_by_link = {}
            unchanged_scrolls = 0
            while len(products_by_link) < args.max_items and unchanged_scrolls < 3:
                for product in extract_products(page):
                    if product["link"]:
                        products_by_link[product["link"]] = product
                        if len(products_by_link) >= args.max_items:
                            break

                previous_count = len(products_by_link)
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(1800)
                if len(products_by_link) == previous_count:
                    unchanged_scrolls += 1
                else:
                    unchanged_scrolls = 0

            products = list(products_by_link.values())
            if not products:
                raise RuntimeError(
                    "No Amazon product links were found. The page may have changed "
                    "or Amazon may have restricted access."
                )

            with args.output.open("w", newline="", encoding="utf-8-sig") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(products)

            browser.close()
            print(f"Saved {len(products)} listings to {args.output}")
    except PlaywrightTimeoutError as error:
        raise SystemExit(f"Timed out while loading Amazon: {error}") from error
    except RuntimeError as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
