import re
from playwright.sync_api import sync_playwright


SEEDS = ["70", "71", "72", "73", "74", "75", "76", "77", "78", "79"]


def main():
    total = 0.0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            for seed in SEEDS:
                url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"

                print(f"Scraping {url}")

                # Load the dynamically generated page
                page.goto(url, wait_until="networkidle")

                # Wait until at least one table exists
                page.wait_for_selector("table")

                # Get every table cell from every table
                cells = page.locator("table td").all_inner_texts()

                seed_total = 0.0

                for cell_text in cells:
                    # Find all numbers in the cell
                    numbers = re.findall(
                        r"-?\d+(?:\.\d+)?",
                        cell_text.strip()
                    )

                    for number in numbers:
                        seed_total += float(number)

                print(f"Seed {seed}: {seed_total}")

                total += seed_total

        finally:
            browser.close()

    final_total = int(round(total))

    print(f"TOTAL_SUM={final_total}")
    print("Scraping completed successfully.")


if __name__ == "__main__":
    main()
