from WebScrapping import WebScraper
import asyncio

scraper = WebScraper()
asyncio.run(scraper.scrape_fslab(lambda message: print(message), "https://www.flightsimlabs.com/index.php/a321-ceo-msfs/"))
asyncio.run(scraper.scrape_fslab(lambda message: print(message), "https://www.flightsimlabs.com/index.php/a321neo/"))
asyncio.run(scraper.scrape_fenixsim(lambda message: print(message)))