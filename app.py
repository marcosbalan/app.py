import streamlit as st
from datetime import datetime, timedelta
import holidays
import requests
from bs4 import BeautifulSoup

# Feriados nacionais e estaduais
feriados = holidays.Brazil(state='SP')

# Função de scraping para extrair feriados do TJ-SP
@st.cache_data
def obter_feriados_tjsp():
    url = "https://www.tjsp.jus.br/Feriados"  # URL de exemplo (ajuste se necessário)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    feriados_tjsp = []
    for item in soup.select('.feriado-lista li'):  # Ajustar seletor de acordo com o site
        try:
            data = item.text.strip().split(' - ')[0]
            feriados_tjsp.append(datetime.strptime(data, '%d/%m/%Y'))
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

       

