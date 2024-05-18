import csv

def save_to_csv(companies):
    if not companies:
        print("No companies found to save.")
        return

    keys = companies[0].keys()
    with open('companies_detailed.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(companies)
