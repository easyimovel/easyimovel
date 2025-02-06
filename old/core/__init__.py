# scraper/__init__.py

from .bypass import CloudflareBypasser
from .browser import ChromiumPage
from .utils import ler_links, converter_data, salvar_dados, obter_elemento_com_tempo_limite, validar_pagina
from .scraper import WebScraper
import config.settings as settings
