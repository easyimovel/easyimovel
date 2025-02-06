from DrissionPage import ChromiumPage
from DrissionPage.common import By
from core.bypass import CloudflareBypasser
from core.utils import obter_elemento_com_tempo_limite, converter_data, validar_pagina
from core.data_storage import salvar_dados
import re
from datetime import datetime
import config.settings as settings

class WebScraper:
    def __init__(self, links_file):
        self.links_file = links_file
        self.browser = ChromiumPage()
        self.bypasser = CloudflareBypasser(self.browser)
        self.links = self.ler_links()
    
    def ler_links(self):
        with open(self.links_file, 'r', encoding='utf-8') as file:
            return [linha.strip() for linha in file if linha.strip()]

    def coletar_dados(self, link, page):
        verificador_numero_perfil = 0
        verificador_nome_usuario = 0
        locators = {
            "titulo": '@|id=description-title@|class=olx-text olx-text--title-medium olx-text--block@|text()',
            "descricao": '@@class=olx-text olx-text--body-medium olx-text--block olx-text--regular ad__sc-2mjlki-1 hNWZgC',
            "valor": (By.XPATH, '/html/body/div[1]/div/div[3]/div/div[4]/div[1]/div[1]/div[1]/span'),
            "condominio": (By.XPATH, '/html/body/div[1]/div/div[3]/div/div[4]/div[1]/div[1]/div[3]/div/span[2]'),
            "iptu": (By.XPATH, '/html/body/div[1]/div/div[3]/div/div[4]/div[1]/div[1]/div[4]/div/span[2]'),
            "endereco_linha1": (By.XPATH, '/html/body/div[1]/div/div[3]/div/div[3]/div[2]/div[2]/div/div[2]/div/div/div/span[1]'),
            "endereco_linha2": (By.XPATH, '/html/body/div[1]/div/div[3]/div/div[3]/div[2]/div[2]/div/div[2]/div/div/div/span[2]'),
            "area_util": (By.XPATH, '/html/body/div[1]/div/div[3]/div/div[3]/div[2]/div[3]/div/div[2]/div[1]/div[2]/span[2]'),
            "quartos": (By.XPATH, '/html/body/div[1]/div/div[3]/div/div[3]/div[2]/div[3]/div/div[2]/div[2]/div[2]/a'),
            "banheiros": (By.XPATH, '/html/body/div[1]/div/div[3]/div/div[3]/div[2]/div[3]/div/div[2]/div[3]/div[2]/span[2]'),
            "vagas_garagem": (By.XPATH, '/html/body/div[1]/div/div[3]/div/div[3]/div[2]/div[3]/div/div[2]/div[4]/div[2]/span[2]'),
            "tipo_usuario": (By.XPATH, '/html/body/div[1]/div/div[3]/div/div[4]/div[2]/div/div[1]/div/div[2]/div/div/span'),
            "tempo_usuario": (By.XPATH, '/html/body/div[1]/div/div[3]/div/div[4]/div[2]/div/div[2]/div[1]/div/span'),
            "local_usuario": (By.XPATH, '/html/body/div[1]/div/div[3]/div/div[4]/div[2]/div/div[2]/div[2]/div/span'),
            "link_usuario": '@@class=olx-button olx-button--neutral olx-button--small olx-button--fullwidth olx-button--a ad__sc-1bqzobc-2 fXTbOn',
            "data_publicacao": (By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/div/span[1]'),
            "numero_perfil": (By.XPATH, '/html/body/div[1]/div/div[3]/div/div[4]/div[1]/div[2]/div[1]/span'),
            "nome_usuario": (By.XPATH, '/html/body/div[1]/div/div[3]/div/div[4]/div[2]/div/div[1]/div/div[2]/div/div/div/span'),
            "show_phone_perfil": ('@|class=olx-link olx-link--caption olx-link--main olx-link--button ad__sc-14mcmsd-4 hjmkGU@|id=price-box-button-show-phone'),
            "nome_usuario2": ('@|class=olx-text olx-text--body-large olx-text--block olx-text--regular ad__sc-ypp2u2-4 TTTuh')
        }

        
        # Coleta do título
        titulo = page.ele(locators["titulo"]).text.strip()
        if '|' in titulo:
            titulo = titulo.split('|')[0].strip()

        # Dados de coleta
        data_coleta = datetime.now().strftime("%d/%m/%Y")
        hora_coleta = datetime.now().strftime("%H:%M")

        # ID do anúncio
        id_anuncio = re.search(r'(\d+)$', link)
        id_anuncio = id_anuncio.group(1) if id_anuncio else 'ID não encontrado'

        # Coleta de elementos utilizando locators
        descricao = obter_elemento_com_tempo_limite(page, locators["descricao"])
        valor = obter_elemento_com_tempo_limite(page, locators["valor"])
        condominio = obter_elemento_com_tempo_limite(page, locators["condominio"])
        iptu = obter_elemento_com_tempo_limite(page, locators["iptu"])
        endereco_linha1 = obter_elemento_com_tempo_limite(page, locators["endereco_linha1"])
        endereco_linha2 = obter_elemento_com_tempo_limite(page, locators["endereco_linha2"])

        partes_endereco = endereco_linha2.split(", ")
        bairro = partes_endereco[0] if len(partes_endereco) > 0 else "Não Informado"
        cidade = partes_endereco[1] if len(partes_endereco) > 1 else "Não Informado"
        estado = partes_endereco[2] if len(partes_endereco) > 2 else "Não Informado"
        cep = partes_endereco[3] if len(partes_endereco) > 3 else "Não Informado"

        area_util = obter_elemento_com_tempo_limite(page, locators["area_util"])
        quartos = obter_elemento_com_tempo_limite(page, locators["quartos"])
        banheiros = obter_elemento_com_tempo_limite(page, locators["banheiros"])
        vagas_garagem = obter_elemento_com_tempo_limite(page, locators["vagas_garagem"])

        tipo_usuario = obter_elemento_com_tempo_limite(page, locators["tipo_usuario"])
        tempo_usuario = obter_elemento_com_tempo_limite(page, locators["tempo_usuario"])
        local_usuario = obter_elemento_com_tempo_limite(page, locators["local_usuario"])

        ele_link_usuario = page.ele(locators["link_usuario"])
        link_usuario = ele_link_usuario.link if ele_link_usuario else "Não Informado"

        data_publicacao = obter_elemento_com_tempo_limite(page, locators["data_publicacao"])
        
        try:
            if not page.ele(locators["numero_perfil"]):
                numero_perfil = "Não Informado"             
            else:
                if page.ele(locators["show_phone_perfil"]):  # Verifica se o elemento existe
                    page.ele(locators["show_phone_perfil"]).click()  # Clique no elemento
                    page.wait.eles_loaded(locators["numero_perfil"], timeout=0.5)
                    while verificador_numero_perfil == 0:
                            page.wait.eles_loaded(locators["numero_perfil"], timeout=0.5)
                            numero_perfil = obter_elemento_com_tempo_limite(page, locators["numero_perfil"])                    
                            if numero_perfil:  # Verifica se o número foi obtido com sucesso
                                if not numero_perfil.endswith("..."):  # Confirma que o número está completo
                                    verificador_numero_perfil += 1
                            else:
                                pass
                    else:
                        pass
        except Exception:
            pass             
    
        
        if page.ele(locators["nome_usuario"]):
            nome_usuario = obter_elemento_com_tempo_limite(page, locators["nome_usuario"])
            pass
        elif page.ele(locators["nome_usuario2"]):
            nome_usuario = obter_elemento_com_tempo_limite(page, locators["nome_usuario2"])
            pass
        else:
            nome_usuario = "Não Informado"        
            


        dados = {
            "data": data_coleta,
            "horario": hora_coleta,
            "plataforma": "OLX",
            "id": id_anuncio,
            "titulo": titulo,
            "descricao": descricao,
            "valor": valor,
            "condominio": condominio,
            "iptu": iptu,
            "endereco": endereco_linha1,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep,
            "area_util": area_util,
            "quartos": quartos,
            "banheiros": banheiros,
            "garagem": vagas_garagem,
            "telefone": numero_perfil,
            "link_anuncio": link,
            "data_anuncio": data_publicacao,
            "nome_usuario": nome_usuario,
            "tipo_usuario": tipo_usuario,
            "tempo_usuario": converter_data(tempo_usuario) if "desde" in tempo_usuario else "Não Informado",
            "local_usuario": local_usuario,
            "link_usuario": link_usuario
        }

        salvar_dados(dados, "resultados.json")

        return dados

    def processar_link(self, link):
        page = self.browser.new_tab(url=link)
        try:
            if validar_pagina(link, page):
                dados = self.coletar_dados(link, page)
                return True, dados
            else:
                return False, None
        finally:
            page.close()
