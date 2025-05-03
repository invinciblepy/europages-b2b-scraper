import os
import time
import csv
import random
from user_agent import generate_user_agent
from .wrapper import fetch_url




class EuropagesScraper:
    def __init__(self, keyword):
        self.keyword = keyword
        self.language = '.co.uk'
        self.base_url = 'https://www.europages.co.uk/search-frontend/alibaba-api/online.company.search'
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': generate_user_agent()
        }
        self.languages = {"en":"co.uk", "fr":"fr", "de":"de", "it":"it", "es":"es", "nl":"nl", 
                          "pl":"pl", "tr":".com.tr", "cz":"cz", "dk":"dk", "ee":"ee", "gr": "gr",
                          "lt":"lt", "hu":"co.hu", "no":"no", "pt":"pt", "ro":"ro", "si":"si",
                          "fi":"fi", "se":"se", "bg":"bg"}
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.parent_dir = os.path.dirname(self.script_dir)
        self.output_dir = os.path.join(self.parent_dir, "output")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
        self.csv_file = open(f"{self.output_dir}/{self.keyword}.csv", "w", newline="")
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(["Name", "PHONE", "WEBSITE", "STREET", "COUNTRY", "ZIPCODE", "CITY", "ACRONYM", "DESCRIPTION", "DISTRIBUTION AREA", "AVERAGE RESPONSE TIME", "FOUNDING YEAR", "NUMBER OF EMPLOYEES"])
        self.total_pages = 0
        self.total_companies = 0
        print("""
                 EUROPAGES CLI SCRAPER
---------------------------------------------------
Author : invinciblepy
GitHub : https://github.com/invinciblepy
Site   : https://hashamx.com
---------------------------------------------------""")

        self.items = []

    def scrape(self, keyword, page=1):
        self.keyword = keyword
        params = {
            'query': keyword,
            'lang': "en",
            'country': "gb",
            'site': 'ep',
            'cityExtractionRadius': '50km',
            'userLatitude': random.uniform(48.0, 54.0),
            'userLongitude': random.uniform(6.0, 15.0),
            'shuffle': 'true',
            'verified': 'false',
            'limit': '9',
            'sort': 'responsiveness',
            'goodResponders': 'true',
            'scene': 'topResponders',
            'page': page
        }
        self.headers['referer'] = f"https://www.europages.co.uk/en/search?q={keyword}"
        response = fetch_url(self.base_url, params=params, headers=self.headers)
        code = response.get('code')
        if code != 200:
            print("[X] Error: {}".format(code))
            return 
        data = response.get('data')
        if page == 1:
            self.total_pages = data.get('paging').get('total_pages')
            print(f"[+] Total pages: {self.total_pages}")
            self.total_companies = data.get('paging').get('total')
        while page <= self.total_pages:
            print(f"[+] Scraping page {page} of {self.total_pages}")
            for company in data.get('companies'):
                self.csv_writer.writerow([
                    company.get('name'),
                    company.get('phone_number'),
                    company.get('homepage'),
                    company.get('street'),
                    company.get('country_code'),
                    company.get('zipcode'),
                    company.get('city'),
                    company.get('acronym'),
                    company.get('description'),
                    company.get('distribution_area'),
                    company.get('average_response_time'),
                    company.get('founding_year'),
                    company.get('employee_count')
                ])
                time.sleep(0.5)
                print(f"[+] Scraped {company.get('name')}")
            page += 1
            self.scrape(keyword, page)
            print(f"[!] Scraped {self.total_companies} companies")
