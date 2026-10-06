# 🛒 Amazon Product Link Scraper

AI-assisted web scraping script using Playwright.

A Python-based web automation and scraping tool built with **Playwright**. This script extracts Amazon product links from search results and exports them directly into a structured CSV file for data research and analysis.

> 💡 **Note:** Developed using an **AI-assisted scripting approach** (leveraging AI tools like GitHub Copilot for rapid prototyping, robust browser handling, and clean code generation).

---

## 🚀 Features

- **Automated Browser Handling:** Uses Playwright to handle dynamic web elements and continuous scrolling.
- **ASIN & URL Parsing:** Automatically cleans and formats product links into standard Amazon product URLs (`/dp/ASIN`).
- **Bot & CAPTCHA Detection:** Safely halts execution if Amazon displays a bot-check page to avoid unnecessary requests.
- **CSV Export:** Saves output into a clean CSV format ready for data analysis.

---

## 🛠️ Tech Stack & Requirements

- **Language:** Python 3.8+
- **Automation Library:** Playwright
- **Methodology:** AI-Assisted Scripting / Automation Research

---

## 📥 Installation & Setup

1. **Clone this repository:**
   ```bash
   git clone [https://github.com/ArnoldElano/Amazon-Product-Scraper.git](https://github.com/ArnoldElano/Amazon-Product-Scraper.git)
   cd Amazon-Product-Scraper

2. Install Playwright and dependencies:

   pip install playwright
   playwright install chromium

4. Run the scraper using the default settings:

   python scrape_amazon.py

You can pass custom parameters for maximum items or a different output CSV filename:
$ python scrape_shopee.py --max-items 30 --output product_links.csv

📊 Sample Output
The scraped product links are exported to amazon_product_links.csv:link :
1. https://www.amazon.com/dp/B0HFJXV8L3
2. https://www.amazon.com/dp/B09XK94491
3. https://www.amazon.com/dp/B0GYRSHB2F

📄 License
This project is open-source and available for educational and portfolio presentation purposes.
