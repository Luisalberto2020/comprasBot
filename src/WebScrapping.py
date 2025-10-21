from bs4 import BeautifulSoup
import asyncio
from playwright.async_api import async_playwright
import time
import random



class WebScraper:

    async def scrape_fenixsim(self, callback):
        print("🚀 Iniciando scraping de fenixsim.com con Playwright...")

        async with async_playwright() as p:
            # Lanza Chromium en modo headless (ideal para servidores)
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--single-process'
                ]
            )

            page = await browser.new_page()

            # Simular un usuario real
            await page.set_extra_http_headers({
                "Accept-Language": "en-US,en;q=0.9",
            })
            # Ocultar que es un bot
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                window.chrome = { runtime: {} };
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
            """)

            try:
                # Navegar con retraso humano
                delay = random.uniform(1.5, 3.0)
                print(f"⏳ Esperando {delay:.1f} segundos antes de navegar...")
                time.sleep(delay)

                print("🌐 Cargando página...")
                await page.goto("https://fenixsim.com", timeout=60000)

                # Esperar a que aparezca contenido clave (precios)
                print("⏳ Esperando a que cargue el contenido dinámico...")
                await page.wait_for_function(
                    "document.body.innerText.includes('£')",
                    timeout=30000
                )

                # Extraer todo el texto visible
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')


                card = soup.find('a', class_='card-link', href="/a320/")
                message = ''

                if card:
                    plane_prize = card.find(
                        'div', class_=['text-lg', 'text-gray-500', 'font-semibold', 'mb-2']).text.strip()
                    message = f"Fenix A320 Plane Price: {plane_prize}"
                    callback(message)
                   
                else:
                    message = "Could not find the plane price on Fenix website."
                    callback(message)

            except Exception as e:
                print(f"❌ Error durante el scraping: {e}")
            finally:
                await browser.close()