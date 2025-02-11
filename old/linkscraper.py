from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import time
from urllib.parse import urlencode
from datetime import datetime

base_url = 'https://www.olx.com.br/imoveis/venda/estado-ba/grande-salvador/salvador'
driver_path = "./chromedriver"

def get_scrapeops_url(url):
    api_key = "d4a17a9b-ea30-4d85-aae8-3ce14df28f41"
    payload = {"api_key": api_key, "url": url}
    proxy_url = "https://proxy.scrapeops.io/v1/?" + urlencode(payload)
    return proxy_url

# Verifica se o ChromeDriver está no caminho especificado
if not os.path.exists(driver_path):
    raise FileNotFoundError(f"ChromeDriver não encontrado no caminho: {driver_path}")

# Configurando o driver do Selenium
service = Service(driver_path)
options = Options()
options.add_argument('--headless')  # Ensures Chrome runs without UI
options.add_argument('--no-sandbox')  # Bypass the sandbox for headless usage
options.add_argument('--disable-dev-shm-usage')  # Fix potential issues in Docker environments
options.add_argument('--remote-debugging-port=9222')  # DevTools connection
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=service, options=options)

# Criando a pasta Links na mesma pasta do script
links_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Links')
os.makedirs(links_folder, exist_ok=True)

# Gerando o nome do arquivo com a data e hora atual
current_time = datetime.now().strftime('%d-%m-%Y--%H-%M')
output_file = os.path.join(links_folder, f'links-{current_time}.txt')

try:
    all_links = []  # Lista para armazenar todos os links

    # Iterando pelas 100 páginas
    for page in range(1, 101):  # De 1 a 100
        # Construindo a URL da página
        url = base_url if page == 1 else f"{base_url}?o={page}"
        print(f"Acessando: {url}")
        driver.get(get_scrapeops_url(url))
        time.sleep(3)  # Aguarda o carregamento da página
        driver.get_screenshot_as_file('screenshot.png') 



        # Encontrando os links de anúncios
        links = driver.find_elements(By.XPATH, '//a[@data-ds-component="DS-NewAdCard-Link"]')
        print(f"peguei todos os links {len(links)}", [link.get_attribute('href') for link in links])
        for _link in [link.get_attribute('href') for link in links]:
            
            if _link and _link not in all_links:  # Evita duplicados e links nulos
                print("peguei link", _link)
                all_links.append(_link)

    # Salvando os links em um arquivo
    # with open(output_file, 'w', encoding='utf-8') as file:
    #     for link in all_links:
    #         file.write(link + '\n')

    print(all_links)

    print(f"Coleta concluída! {len(all_links)} links salvos em '{output_file}'.")

finally:
    driver.quit()
