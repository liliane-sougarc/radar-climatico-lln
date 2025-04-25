import streamlit as st
import pandas as pd
import plotly.express as px

# URL do CSV público no Google Sheets
URL_CSV = "https://docs.google.com/spreadsheets/d/1_sevoT4zpto6Fhns-XxOhX5MYX0TRwNi9LoB0n9LMhg/export?format=csv"

# Carregar os dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv(URL_CSV)
    df.fillna("Não informado", inplace=True)
    return df

df = carregar_dados()

# Cálculo automático do IRE (caso esteja vazio)
def calcular_ire(row):
    if row["defesa_civil"] == "Sim" and row["bombeiros"] == "Sim" and row["plano_contingencia"] == "Sim":
        return 3
    elif (row["defesa_civil"] == "Sim" and row["plano_contingencia"] == "Sim") or \
         (row["bombeiros"] == "Sim" and row["plano_contingencia"] == "Sim"):
        return 2
    elif row["defesa_civil"] == "Sim" or row["bombeiros"] == "Sim" or row["plano_contingencia"] == "Sim":
        return 1
    else:
        return 0

df["IRE"] = df.apply(calcular_ire, axis=1)

# Interface do App
st.set_page_config(page_title="Radar Climático LLN", layout="wide")
st.title("⚡ Radar Climático - LLN")

st.markdown("""
Este dashboard apresenta indicadores de risco climático para diferentes municípios do RS, com base em dados ambientais, estruturais e de resposta emergencial.
""")

# Filtro por município
municipios = df["municipio"].unique()
selecao = st.selectbox("Selecione um município:", municipios)

filtro = df[df["municipio"] == selecao]
st.subheader(f"Análise detalhada: {selecao}")
st.dataframe(filtro)

# Gráfico de risco por cidade
st.subheader("🔍 Comparativo de IRE entre municípios")
fig = px.bar(df, x="municipio", y="IRE", color="IRE", text="IRE",
             color_continuous_scale="reds", title="Índice de Resposta a Emergências (IRE)")
fig.update_layout(xaxis_title="Município", yaxis_title="IRE", height=500)
st.plotly_chart(fig, use_container_width=True)

# Aviso final
st.markdown("---")
st.markdown("Desenvolvido por LLN Automações | Projeto MVP Radar Climático")
