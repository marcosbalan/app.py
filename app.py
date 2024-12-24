import streamlit as st
from datetime import datetime, timedelta
import holidays

# Lista de feriados nacionais e estaduais de SP
feriados = holidays.Brazil(state='SP')

# Título da aplicação
st.title("🗓️ Calculadora de Prazo Judicial")

# Entradas do usuário
data_inicial = st.text_input("📅 Data Inicial (DD/MM/AAAA)")
dias_prazo = st.number_input("⏳ Dias Úteis", min_value=1, step=1)

# Botão para calcular o prazo
if st.button("Calcular Prazo"):
    try:
        # Conversão e cálculo do prazo
        data = datetime.strptime(data_inicial, '%d/%m/%Y')
        dias_corridos = 0

        while dias_corridos < dias_prazo:
            data += timedelta(days=1)
            if data.weekday() < 5 and data not in feriados:
                dias_corridos += 1

        st.success(f"✅ O prazo final é: {data.strftime('%d/%m/%Y')}")
    except ValueError:
        st.error("⚠️ Por favor, insira uma data válida no formato DD/MM/AAAA.")
       

