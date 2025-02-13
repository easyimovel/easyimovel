import requests
import logging
import time
import os
import random
import asyncio

from pprint import pprint, pformat
from urllib.parse import urlparse, urlencode, urljoin
from typing import List

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, SessionNotCreatedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from playwright.async_api import async_playwright

def get_selenium_driver(logger: logging.Logger) -> webdriver:
    logger.debug("Chrome driver mount.")
    print(os.environ["CHROMEDRIVER_PATH"])
    service = Service(os.environ["CHROMEDRIVER_PATH"])
    options = Options()
    options.add_argument('--headless')  # Ensures Chrome runs without UI
    options.add_argument('--no-sandbox')  # Bypass the sandbox for headless usage
    options.add_argument('--disable-dev-shm-usage')  # Fix potential issues in Docker environments
    options.add_argument('--remote-debugging-port=9222')  # DevTools connection
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def get_scrapeops_url(url: str, api_key: bool = False) -> str:
    api_key_list = [
        # "d4a17a9b-ea30-4d85-aae8-3ce14df28f41",
        "5a5bdcaa-ea84-49a8-b734-60f308b56453",
        "2380a408-0e07-47c4-9c41-283076d54863",
        "bad27a98-2ccf-4c68-a981-9f1c8165b33c",
    ]
    if api_key:
        return random.choice(api_key_list)
    
    payload = {"api_key": random.choice(api_key_list), "url": url}
    proxy_url = "https://proxy.scrapeops.io/v1/?" + urlencode(payload)
    return proxy_url

def scroll_to_bottom(driver: webdriver):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            break
        
        last_height = new_height

def get_links_selenium(logger: logging.Logger, url: str) -> list:
    driver: webdriver = get_selenium_driver(logger)

    page: int = 1
    all_links: list = []
    while True:
        url = urljoin(url, f"?o={page}")
        logger.info(f"Acessando: {url}")
        
        try:
            driver.get(get_scrapeops_url(url))
            links = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[@data-ds-component="DS-NewAdCard-Link"]'))
            )
        except SessionNotCreatedException:
            logger.error("Proxy API KEY probably is out.")
            driver.quit()
            break
        except TimeoutException:
            logger.error(f"Page {page} not found.")
            driver.quit()
            break
        except NoSuchElementException:
            logger.error("caiu no timeout 2")
            driver.quit()
            break
        except TimeoutError:
            logger.error("caiu no timeout 3")
            time.sleep(5)
            continue
        except Exception as e:
            logger.error(f"An unexpected error ocurred: {str(e)}")
            driver.quit()
            break

        page = page+1

        logger.info(f"peguei todos os links {len(links)}")
        for _link in [link.get_attribute('href') for link in links]:
            if _link and _link not in all_links:
                all_links.append(_link)
                logger.info(f"peguei link: {_link}")
    
    driver.quit()
    return all_links

async def playwright(logger: logging.Logger, urls: list):
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=['--disable-http2', '--no-sandbox'])
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            proxy={
                "server": "https://proxy.scrapeops.io:5353",
                "username": "scrapeops",
                "password": get_scrapeops_url("", api_key=True)
            }
        )
        page = await context.new_page()

        logger.info(f"chave de proxy: {get_scrapeops_url("", api_key=True)}")

        for _url in urls:
            logger.info(f"Pegando url {_url}")
            # await page.goto(get_scrapeops_url(_url))
            await page.goto(_url)
            await page.wait_for_selector("a:has-text('Entrar')", timeout=0)
            await page.locator("a[href='https://conta.olx.com.br/anuncios'].olx-link--caption.olx-link--main.olx-header__profile-link").click()

            await page.wait_for_selector('input#input-1.olx-text-input__input-field.olx-text-input__input-field--medium', timeout=0)
            await page.locator('input#input-1.olx-text-input__input-field.olx-text-input__input-field--medium').fill('henriquedpadua12@gmail.com')
            await page.locator('button.olx-button.olx-button--primary.olx-button--medium.olx-button--fullwidth').click()

            # await page.wait_for_load_state('networkidle')
            await asyncio.sleep(5)
            await page.screenshot(path="test.png")
            await browser.close()
            break

        logger.info("SAINDO")

class OLX:
    
    def __init__(self, logger):
        self.logger = logger

    def gen_token(self) -> str:
        url = urljoin(os.environ["API_URL"], "token")
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'password',
            'username': 'admin',
            'password': os.environ["ADMIN_API_PASS"],
            'scope': '',
            'client_id': 'string',
            'client_secret': 'string'
        }
        response = requests.post(url, headers=headers, data=data)
        if response.status_code != 200:
            return False
        return response.json()["access_token"]

    def save(self, links: list):
        if token := self.gen_token():
            url = urljoin(os.environ["API_URL"], "urls/post_urls")
            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            response = requests.post(url, headers=headers, json=links)

    def get_links(self):
        start_urls: List[str] = [
            "https://www.olx.com.br/imoveis/venda/estado-ba/grande-salvador/grande-salvador",
            "https://www.olx.com.br/imoveis/venda/estado-sp/sao-paulo-e-regiao",
        ]
        for _url in start_urls:
            links_to_save = get_links_selenium(self.logger, _url)
            self.save(links_to_save)

    def get_data_from_urls(self):
        if token := self.gen_token():
            url = urljoin(os.environ["API_URL"], "urls/get_urls")
            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            params = {
                "platform": "olx"
            }
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()["list"]

        try:
            start_urls: List[str] = data
            asyncio.run(playwright(self.logger, start_urls))
            
        except Exception as e:
            self.logger.error(f"Error detail: {str(e)}")
