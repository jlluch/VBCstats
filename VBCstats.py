#Aplicación streamlit para visualizar estadísticas de VBC
# Autor: JLLUCH
# Fecha: 2024-12-20 
#
# """
import streamlit as st
import pandas as pd
from st_pages import get_nav_from_toml

st.set_page_config(
    page_title="Estadísticas de Valencia Basket",
    page_icon="🏀",
    layout="wide",  # This forces wide mode
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    [data-testid="stSidebar"] {
        width: 12rem !important;
    }
</style>
""", unsafe_allow_html=True)
    
st.sidebar.header("Selecciona una competición")
#Configurar páginas
nav = get_nav_from_toml(path=".streamlit/pages.toml")

# Crea la navegación
pg = st.navigation(nav)

# Ejecuta la página seleccionada
pg.run()