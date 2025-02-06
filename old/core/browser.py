# core/browser.py
from DrissionPage import Chromium, ChromiumOptions, ChromiumPage as BaseChromiumPage
from core.bypass import CloudflareBypasser
import config.settings as settings

class ChromiumPage:
    def __init__(self):
        # Configurações do Chromium, como cabeçalhos e configurações de rede
        options = ChromiumOptions()
        options.add_argument('--headless')  # Caso deseje rodar sem interface gráfica
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')

        # Inicialização do navegador
        self.browser = Chromium(options=options)

        # Bypass para Cloudflare (se necessário)
        self.bypasser = CloudflareBypasser(self.browser)

    def new_tab(self, url):
        """Cria uma nova aba e abre a URL fornecida."""
        page = self.browser.get(url)
        return ChromiumPageWrapper(page)

    def close(self):
        """Fecha o navegador."""
        self.browser.quit()

class ChromiumPageWrapper:
    def __init__(self, page):
        self.page = page

    def ele(self, locator, timeout=10):
        """Retorna o primeiro elemento encontrado no locator especificado."""
        return self.page.wait_for_element(locator, timeout=timeout)

    def close(self):
        """Fecha a página."""
        self.page.close()

    def wait(self):
        """Esperar o carregamento de elementos, por exemplo."""
        return self.page.wait
