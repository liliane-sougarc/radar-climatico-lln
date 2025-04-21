
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

data = {
    'Cidade': ['Porto Alegre', 'Canoas', 'Pelotas', 'Santa Maria', 'Uruguaiana'],
    'Risco Climático': ['Alto', 'Moderado', 'Latente', 'Alto', 'Resiliência'],
    'População em Risco': [120000, 85000, 30000, 95000, 10000],
    'Último Evento Crítico': ['2023-09', '2022-01', '2018-07', '2023-11', '2015-03'],
    'Latitude': [-30.0346, -29.9128, -31.7649, -29.6868, -29.7531],
    'Longitude': [-51.2177, -51.1839, -52.3371, -53.8069, -57.0863]
}
df = pd.DataFrame(data)

st.set_page_config(page_title="Radar Climático – LLN", layout="wide")
st.title("Radar Climático – LLN")
st.markdown("""
**Painel de Visualização de Risco Climático no RS**

Este aplicativo demonstra como dados públicos podem ser utilizados para classificar zonas de risco climático e orientar decisões de prefeituras, ONGs e empresas.
""")

cidade_selecionada = st.selectbox("Selecione uma cidade:", df['Cidade'])
info = df[df['Cidade'] == cidade_selecionada].iloc[0]

st.subheader(f"Risco em {cidade_selecionada}: {info['Risco Climático']}")
st.write(f"População em risco: {info['População em Risco']:,} pessoas")
st.write(f"Último evento climático crítico: {info['Último Evento Crítico']}")

mapa = folium.Map(location=[info['Latitude'], info['Longitude']], zoom_start=7)
folium.Marker(
    location=[info['Latitude'], info['Longitude']],
    popup=f"{cidade_selecionada} - Risco: {info['Risco Climático']}",
    tooltip="Clique para ver detalhes",
    icon=folium.Icon(color="red" if info['Risco Climático'] == 'Alto' else "orange" if info['Risco Climático'] == 'Moderado' else "blue")
).add_to(mapa)
folium_static(mapa)

st.markdown("---")
st.subheader("Plano de Ação Sugerido")
if info['Risco Climático'] == 'Alto':
    st.markdown("- Investimento imediato em drenagem urbana\n- Simulações de evacuação\n- Campanhas de alerta antecipado")
elif info['Risco Climático'] == 'Moderado':
    st.markdown("- Monitoramento frequente\n- Revisão do plano de emergência\n- Manutenção em infraestrutura local")
elif info['Risco Climático'] == 'Latente':
    st.markdown("- Mapeamento de áreas vulneráveis\n- Acompanhamento de obras públicas\n- Educação ambiental nas escolas")
else:
    st.markdown("- Monitoramento contínuo\n- Compartilhamento de boas práticas\n- Manter planos de contingência atualizados")

st.markdown("---")
st.info("Versão inicial demonstrativa com dados simulados. Em breve, integração com dados reais e exportação em PDF.")
