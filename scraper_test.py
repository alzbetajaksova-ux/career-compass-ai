import asyncio
import random
import pandas as pd
from playwright.async_api import async_playwright



async def run_scraper():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 720}

        )
        page = await context.new_page()
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        all_jobs_data = []
        # Prechádzame prvé 4 strany
        for page_num in range(1, 7):
            if page_num == 1:
                url = "https://www.profesia.sk/praca/?count_days=14&positions[]=740&positions[]=153&positions[]=596&positions[]=600&positions[]=89&positions[]=84&positions[]=85&positions[]=746&positions[]=747&positions[]=593&positions[]=70&search_anywhere=python&sort_by=relevance"
            else:
                url = f"https://www.profesia.sk/praca/?count_days=14&positions[]=740&positions[]=153&positions[]=596&positions[]=600&positions[]=89&positions[]=84&positions[]=85&positions[]=746&positions[]=747&positions[]=593&positions[]=70&search_anywhere=python&sort_by=relevance&page_num={page_num}"

            print(f" Navigujem na {page_num} stranu...")

            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=60000)
                await asyncio.sleep(random.uniform(3, 5))
                job_elements = await page.query_selector_all('li.list-row')

                if not job_elements:
                    print(f"ℹ️ Na strane {page_num} sa nenašli žiadne inzeráty. Končím.")
                    break

                for el in job_elements:
                    try:
                        title_el = await el.query_selector('span.title')
                        title = await title_el.inner_text() if title_el else "N/A"

                        comp_el = await el.query_selector('span.employer')
                        company = await comp_el.inner_text() if comp_el else "N/A"

                        salary = "Neuvedený"
                        selectors = ['span.label-success', '.salary', 'span.label']

                        for selector in selectors:
                            salary_el = await el.query_selector(selector)

                            if salary_el:
                                text = await salary_el.inner_text()
                                if "EUR" in text or "€" in text:
                                    salary = text.replace('\xa0', ' ').strip()
                                    break

                        if salary == "Neuvedený":
                            eur_el = await el.query_selector(':scope >> text="EUR"')

                            if eur_el:
                                salary = await eur_el.inner_text()
                                salary = salary.replace('\xa0', ' ').strip()

                        if title != "N/A":
                            all_jobs_data.append({
                                "Pozícia": title.strip(),
                                "Firma": company.strip(),
                                "Plat": salary
                            })

                    except:
                        continue

                print(f" Strana {page_num} spracovaná. Priebežný počet inzerátov: {len(all_jobs_data)}")

            except Exception as e:
                print(f" Chyba pri sťahovaní strany {page_num}: {e}")
                break

        if all_jobs_data:
            df = pd.DataFrame(all_jobs_data)
            df = df.drop_duplicates(subset=['Pozícia', 'Firma'])
            df.to_csv("test_data.csv", index=False, encoding='utf-8-sig')
            print(f"Uložených {len(df)} unikátnych inzerátov.")

        else:
            print("Žiadne dáta na uloženie.")

        await browser.close()

if __name__ == "__main__":

    asyncio.run(run_scraper())