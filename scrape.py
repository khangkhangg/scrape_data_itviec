from bs4_scraper import scrape_companies_bs4
from selenium_scraper import scrape_companies_selenium
from utils.csv_helper import save_to_csv
from utils.json_helper import save_to_json
from utils.db_helper import save_to_db
from utils.selenium_helper import setup_selenium_driver
import threading

def get_user_input(prompt, timeout, default):
    def ask_input():
        nonlocal user_input
        user_input = input(prompt).strip().lower()

    user_input = default
    thread = threading.Thread(target=ask_input)
    thread.start()
    thread.join(timeout)
    return user_input

def main():
    method = get_user_input("Choose scraping method (bs4/selenium): ", 20, "bs4")

    if method == 'bs4':
        companies = scrape_companies_bs4()
    elif method == 'selenium':
        browser = get_user_input("Choose browser (firefox/safari/edge): ", 20, "safari")
        driver = setup_selenium_driver(browser)
        if driver:
            companies = scrape_companies_selenium(driver)
            driver.quit()
        else:
            print("Unsupported browser.")
            return
    else:
        print("Unsupported method.")
        return

    if companies:
        export_format = get_user_input("Choose export format (csv/json/db): ", 20, "csv")
        if export_format == 'csv':
            save_to_csv(companies)
        elif export_format == 'json':
            save_to_json(companies)
        elif export_format == 'db':
            save_to_db(companies)
        else:
            print("Unsupported export format.")
            return
        print(f'Scraping completed. Data saved to companies_detailed.{export_format if export_format != "db" else "MySQL"}')
    else:
        print('No companies scraped.')

if __name__ == '__main__':
    main()
