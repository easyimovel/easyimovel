import streamlit as st
import json

# Carregar os dados do arquivo JSON
def carregar_dados():
    with open("core/resultados.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Função para identificar se é Casa ou Apartamento
def identificar_tipo_imovel(titulo):
    titulo_lower = titulo.lower()
    if "casa" in titulo_lower:
        return "🏠"
    elif "apartamento" in titulo_lower or "apto" in titulo_lower:
        return "🏢"
    return "❓"

# Função para limpar valores monetários
def limpar_valor(valor):
    if valor in ["Não Informado", "Não Tem", "Não especificado"]:
        return 0
    try:
        return float(valor.replace("R$", "").replace(".", "").replace(",", ".").strip())
    except ValueError:
        return 0

# Função para converter valores para float
def tratar_nao_informado(valor):
    if valor in ["Não Informado", "Não Tem", "Não especificado"]:
        return 0
    try:
        return int(valor.replace("m²", "").replace(",", ".").strip())
    except ValueError:
        return 0

# Formatar valores monetários
def formatar_valor(valor):
    if valor == 0:
        return "Não Informado"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Função para formatar o número de telefone
def formatar_telefone(telefone):
    numero_formatado = telefone.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    return f"https://wa.me/55{numero_formatado}"

# Função para gerar o link do mapa no Google Maps
def gerar_link_mapa_html(item):
    endereco_completo = f"{item['endereco']}, {item['bairro']}, {item['cidade']}, {item['estado']}"
    endereco_formatado = endereco_completo.replace(" ", "+")
    # Usando o marcador para destacar a rua no mapa
    link = f"https://www.google.com/maps?q={endereco_formatado}&z=16&ll={endereco_formatado}&markers={endereco_formatado}"

    # Gerar o código HTML com o link
    return link

# Layout do Streamlit
st.set_page_config(page_title="Resultados de Imóveis", layout="wide")
st.title("📊 Resultados de Imóveis")

# Carregar os dados
dados = carregar_dados()

# Sidebar - Filtros
st.sidebar.title("🔍 Filtros de Busca")

# Filtro por bairro
st.sidebar.markdown("### 📍 Bairro")
# Ordenar bairros alfabeticamente e garantir que 'Piatã' não esteja selecionado
bairros_disponiveis = sorted(set(item["bairro"] for item in dados))
bairros_selecionados = st.sidebar.multiselect(
    "Selecione os bairros:", 
    ["Todos os bairros"] + bairros_disponiveis, 
    default=["Todos os bairros"]
)

# Filtro de Tipo de Imóvel (com expander)
with st.sidebar.expander("🏡 Tipo de Imóvel"):
    mostrar_casas = st.checkbox("Mostrar Casas", value=True)
    mostrar_apartamentos = st.checkbox("Mostrar Apartamentos", value=True)

# Filtros de faixa de valor
st.sidebar.markdown("### 💰 Valor\n")
valor = st.sidebar.slider(
    "Selecione o valor:\n", 
    0, 5000000, 
    (0, 5000000), 
    step=50000,
    format="R$ %d"
)

# Filtros de área
st.sidebar.markdown("### 📏 Área\n")
area = st.sidebar.slider(
    "Selecione a área:\n", 
    0, 1000, 
    (0, 1000), 
    step=10,
    format= "%d m²"
)

# Filtros de Características dos Imóveis (com expander)
with st.sidebar.expander("🛏️ Características do Imóvel"):
    quartos = st.slider("Quartos:\n", 0, 10, (0, 10), step=1, format="%d quartos")
   
    banheiros = st.slider(
        "Banheiros:\n",
         0, 10,
         (0, 10),
         step=1,
         format="%d banheiros"
    )
    
    garagem = st.slider(
        "Garagem:\n",
         0, 10,
         (0, 10),
         step=1,
         format="%d garagens"
    )
    
    condominio = st.slider(
        "Condomínio:\n", 
        0, 10000, 
        (0, 10000), 
        step=100, 
        format="R$ %d"
    )
       
    iptu = st.slider(
        "IPTU:\n", 
        0, 10000, 
        (0, 10000), 
        step=100, 
        format="R$ %d"
    )
   

# Filtragem dos dados
dados_filtrados = []
for item in dados:
    tipo = identificar_tipo_imovel(item["titulo"])
    preco = limpar_valor(item["valor"])
    area_util = tratar_nao_informado(item["area_util"])
    quartos_disponiveis = tratar_nao_informado(item["quartos"])
    
    try:
        banheiros_disponiveis = tratar_nao_informado(item["banheiros"].split()[0])
    except:
        banheiros_disponiveis = 0

    garagem_disponivel = tratar_nao_informado(item["garagem"])
    valor_condominio = limpar_valor(item["condominio"].replace(" / mês", "").strip())
    valor_iptu = limpar_valor(item["iptu"].strip())

    # Aplica filtros selecionados
    if ((tipo == "🏠" and mostrar_casas) or (tipo == "🏢" and mostrar_apartamentos)) and \
       (valor[0] <= preco <= valor[1] or preco == 0) and \
       (area[0] <= area_util <= area[1] or area_util == 0) and \
       (quartos[0] <= quartos_disponiveis <= quartos[1]) and \
       (banheiros[0] <= banheiros_disponiveis <= banheiros[1]) and \
       (garagem[0] <= garagem_disponivel <= garagem[1]) and \
       (condominio[0] <= valor_condominio <= condominio[1] or valor_condominio == 0) and \
       (iptu[0] <= valor_iptu <= iptu[1] or valor_iptu == 0) and \
       (bairros_selecionados == ["Todos os bairros"] or item["bairro"] in bairros_selecionados):
        dados_filtrados.append(item)

# Exibição dos imóveis
if not dados_filtrados:
    st.warning("⚠️ Nenhum imóvel encontrado com os filtros selecionados.")
else:
    for item in dados_filtrados:
        tipo_imovel = identificar_tipo_imovel(item["titulo"])

        # Gerar o link para o mapa
        link_mapa = gerar_link_mapa_html(item)

        # Layout com informações do imóvel à esquerda (60%) e do usuário à direita (40%)
        col1, col2 = st.columns([3, 2])  # 60% e 40% de largura

        # Coluna 1: Imóvel
        with col1:
            st.markdown(
                f"""
                <div style="border: 2px solid #ddd; border-radius: 14px; padding: 20px; margin-bottom: 20px; background: linear-gradient(to right, #f9f9f9, #fff); box-shadow: 2px 2px 12px rgba(0,0,0,0.15); transition: transform 0.2s;">
                    <p style="font-size: 20px; font-weight: bold; color: #333;">
                        💰 <strong>Valor:</strong> {item["valor"]} &nbsp; | &nbsp; 📍 <strong>Bairro:</strong> {item['bairro']} &nbsp; | &nbsp; 🏙️ <strong>Cidade:</strong> {item['cidade']}
                    </p>
                    <p style="font-size: 17px; color: #444;">
                        📏 <strong>Área útil:</strong> {item["area_util"]} &nbsp; | &nbsp; 🛏️ <strong>Quartos:</strong> {item["quartos"]} &nbsp; | &nbsp; 🚿 <strong>Banheiros:</strong> {item["banheiros"]} &nbsp; | &nbsp; 🚗 <strong>Garagem:</strong> {item["garagem"]} 
                    </p>                    
                    <p style="font-size: 16px; color: #555;">
                        🏢 <strong>Condomínio:</strong> {item["condominio"]} &nbsp; | &nbsp; 🏠 <strong>IPTU:</strong> {item["iptu"]} 
                    </p>
                    <p style="font-size: 16px; color: #555;">
                        <strong>Endereço:</strong> <a href="{link_mapa}" target="_blank">{item["endereco"]} </a>
                    </p>
                     <p style="font-size: 17px; color: #444;">
                        <strong>Link do Anúncio:</strong> <a href="{item["link_anuncio"]}" target="_blank">
                            <img src="https://logosmarcas.net/wp-content/uploads/2022/04/OLX-Emblema.png" alt="OLX Logo" style="height: 20px;">
                        </a>
                    </p>
                     <p style="font-size: 17px; color: #444;">
                        <strong>Data do Anúncio:</strong> {item["data_anuncio"]} &nbsp;
                    </p>
                    <p style="font-size: 15px; color: #666; text-align: justify;">
                        📝 <strong>Descrição:</strong> {item['descricao']}
                    </p>
                </div>
                """, unsafe_allow_html=True
            )

        # Coluna 2: Card do Usuário
        with col2:
            st.markdown(
                f"""
                <div style="border: 2px solid #ddd; border-radius: 14px; padding: 20px; margin-bottom: 20px; background: linear-gradient(to right, #f9f9f9, #fff); box-shadow: 2px 2px 12px rgba(0,0,0,0.15); transition: transform 0.2s;">
                    <p style="font-size: 20px; font-weight: bold; color: #333;">👤  Perfil do Anunciante</p>
                    <p style="font-size: 17px; color: #555;"><strong>Nome:</strong> {item['nome_usuario']}</p>
                    <p style="font-size: 17px; color: #555;"><strong>Tipo de Conta:</strong> {item['tipo_usuario']}</p>
                    <p style="font-size: 17px; color: #555;"><strong>Conta criada:</strong> {item['tempo_usuario']}</p>
                    <p style="font-size: 17px; color: #555;"><strong>Telefone:</strong> <span style="font-size: 22px; color: #333;"><strong>{item['telefone']}</strong></span></p>
                    <p style="font-size: 17px; color: #444;">
                        <strong>Link do Perfil:</strong>  <a href="{item["link_usuario"]}" target="_blank">
                            <img src="https://logosmarcas.net/wp-content/uploads/2022/04/OLX-Emblema.png" alt="OLX Logo" style="height: 20px;">
                        </a>
                    </p>
                    <p style="font-size: 17px; color: #444;">
                        <strong>WhatsApp:</strong> <a href="{formatar_telefone(item["telefone"])}" target="_blank">
                            <img src="https://png.pngtree.com/png-clipart/20190516/original/pngtree-whatsapp-icon-png-image_3584845.jpg" alt="OLX Logo" style="height: 40px;">
                        </a>
                    </p>
                </div>
                """, unsafe_allow_html=True
            )
