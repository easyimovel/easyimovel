import json
import os

def salvar_dados(dados, nome_arquivo="resultados.json"):
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo = os.path.join(diretorio_base, nome_arquivo)
    lista_dados = []
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            try:
                lista_dados = json.load(f)
                if not isinstance(lista_dados, list):
                    lista_dados = []
            except json.JSONDecodeError:
                lista_dados = []
    lista_dados.append(dados)
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(lista_dados, f, ensure_ascii=False, indent=4)
