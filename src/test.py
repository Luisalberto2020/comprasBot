from WebScrapping import WebScraper
import asyncio

scraper = WebScraper()
asyncio.run(scraper.scrape_fenixsim())