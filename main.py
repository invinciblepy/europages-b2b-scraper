import europages.scraper
import argparse

def main():
    parser = argparse.ArgumentParser(description="Europages Scraper CLI")
    parser.add_argument("-k", "--keyword", help="Keyword to search for", required=True)
    args = parser.parse_args()
    scraper = europages.scraper.EuropagesScraper(args.keyword)
    scraper.scrape(args.keyword)

if __name__ == "__main__":
    main()
