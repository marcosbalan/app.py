import streamlit as st
from datetime import datetime, timedelta
import holidays
import requests
from bs4 import BeautifulSoup

# Feriados nacionais e estaduais
feriados = holidays.Brazil(state='SP')

# Função de scraping para extrair feriados do TJ-SP
@st.cache_data(ttl=86400)  # Cache de 24 horas
def obter_feriados_tjsp():
    url = "https://www.tjsp.jus.br/CanaisComunicacao/Feriados/ExpedienteForense"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Garante que a requisição teve sucesso
    except requests.exceptions.Timeout:
        st.error("⏳ O site do TJ-SP demorou muito para responder. Tente novamente mais tarde.")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erro ao acessar o site do TJ-SP: {e}")
        return []

    # Parsing da página com BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    feriados_tjsp = []
    # Exemplo de seletor - ajustado com base na estrutura do site
    for item in soup.select('.corpo-texto li'):  # Ajustar caso necessário
        try:
            data_texto = item.text.strip().split(' - ')[0]
            data = datetime.strptime(data_texto, '%d/%m/%Y')
            feriados_tjsp.append(data)
        except ValueError:
            continue

    return feriados_tjsp

# Obter feriados do TJ-SP e adicionar à lista
feriados_tjsp = obter_feriados_tjsp()
for f in feriados_tjsp:
    feriados[f] = "Feriado Municipal TJ-SP"

# Interface Streamlit
st.title("🗓️ Calculadora de Prazo Judicial TJ-SP (Scraping Automático)")

data_inicial = st.text_input("📅 Data Inicial (DD/MM/AAAA)")
dias_prazo = st.number_input("⏳ Dias Úteis", min_value=1, step=1)

if st.button("Calcular Prazo"):
    try:
        data = datetime.strptime(data_inicial, '%d/%m/%Y')
        dias_corridos = 0

        while dias_corridos < dias_prazo:
            data += timedelta(days=1)
            if data.weekday() < 5 and data not in feriados:
                dias_corridos += 1

        st.success(f"✅ O prazo final é: {data.strftime('%d/%m/%Y')}")
    except ValueError:
        st.error("⚠️ Por favor, insira uma data válida no formato DD/MM/AAAA.")

    feriados[f] = "Feriado Municipal TJ-SP"

# Interface Streamlit
st.title("🗓️ Calculadora de Prazo Judicial TJ-SP (Scraping Automático)")

data_inicial = st.text_input("📅 Data Inicial (DD/MM/AAAA)")
dias_prazo = st.number_input("⏳ Dias Úteis", min_value=1, step=1)

if st.button("Calcular Prazo"):
    try:
        data = datetime.strptime(data_inicial, '%d/%m/%Y')
        dias_corridos = 0

        while dias_corridos < dias_prazo:
            data += timedelta(days=1)
            if data.weekday() < 5 and data not in feriados:
                dias_corridos += 1

        st.success(f"✅ O prazo final é: {data.strftime('%d/%m/%Y')}")
    except ValueError:
        st.error("⚠️ Por favor, insira uma data válida no formato DD/MM/AAAA.")

       

