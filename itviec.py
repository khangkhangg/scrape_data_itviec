from bs4_scraper import scrape_companies_bs4
from selenium_scraper import scrape_companies_selenium
from utils import save_to_csv, setup_selenium_driver

def main():
    method = input("Choose scraping method (bs4/selenium): ").strip().lower()

    if method == 'bs4':
        companies = scrape_companies_bs4()
    elif method == 'selenium':
        browser = input("Choose browser (firefox/safari/edge): ").strip().lower()
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
        save_to_csv(companies)
        print('Scraping completed. Data saved to companies_detailed.csv')
    else:
        print('No companies scraped.')

if __name__ == '__main__':
    main()
