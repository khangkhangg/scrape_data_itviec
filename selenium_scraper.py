import time
import random
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.selenium_helper import get_company_details_selenium, setup_selenium_driver, login, get_total_companies, click_see_more
from utils.constants import base_url

def wait_for_page_load(driver, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    except TimeoutException:
        pass

def scrape_companies_selenium(driver):
    login(driver)
    driver.get(f'{base_url}/companies/review-company')
    wait_for_page_load(driver)
    
    total_companies = get_total_companies(driver)
    print(f'Total number of companies to scrape: {total_companies}')
    
    companies_scraped = 0
    scraped_company_urls = set()
    companies = []

    while companies_scraped < total_companies:
        company_elements = driver.find_elements(By.CLASS_NAME, 'company')

        for company in company_elements:
            company_link = company.find_element(By.CLASS_NAME, 'company__link').get_attribute('href')
            if company_link in scraped_company_urls:
                continue
            scraped_company_urls.add(company_link)
            
            company_name = company.find_element(By.CLASS_NAME, 'company__name').text.strip()
            print(f'Scraping {company_name} ({companies_scraped + 1}/{total_companies})')

            try:
                # Click to go to the company page
                company_link_element = company.find_element(By.CLASS_NAME, 'company__link')
                driver.execute_script("window.open(arguments[0].getAttribute('href'), '_blank');", company_link_element)
                driver.switch_to.window(driver.window_handles[-1])
                wait_for_page_load(driver)
                time.sleep(1)  # Ensure the page is fully loaded

                # Detect the "Overview" tab
                overview_tab = driver.find_element(By.XPATH, "//a[@data-controller='utm-tracking' and contains(@class, 'tab-link') and contains(text(), 'Overview')]")
                if overview_tab:
                    print(f"Found Overview tab for {company_name}")
                    overview_tab.click()
                    wait_for_page_load(driver)
                    time.sleep(1)

                    # Scrape the company details
                    company_details = get_company_details_selenium(driver, company_link)
                    if company_details:
                        companies.append(company_details)

                    print(f"Scraped data for {company_name}")

                # Close the company tab and go back to the listing page
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                wait_for_page_load(driver)
                
                companies_scraped += 1
                if companies_scraped >= total_companies:
                    break

            except Exception as e:
                print(f'Failed to scrape {company_link}: {e}')

            time.sleep(random.randint(1, 10))  # Be respectful of the server; add delay between requests

        # Click "See more" to load more companies if needed
        if companies_scraped < total_companies:
            click_see_more(driver)
            wait_for_page_load(driver)
            time.sleep(1)  # Ensure the page is fully loaded
    
    return companies
