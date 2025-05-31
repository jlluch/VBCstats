#Aplicación streamlit para visualizar estadísticas de VBC
# Autor: JLLUCH
# Fecha: 2024-12-20 
#
# """
import streamlit as st
import pandas as pd
from st_pages import get_nav_from_toml
import streamlit.components.v1 as components

ga_code = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HTHR3HRXS1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-HTHR3HRXS1');
</script>
"""

# Configuración de la página
st.set_page_config(
    page_title="Estadísticas de Valencia Basket",
    page_icon="🏀",
    layout="wide",  # This forces wide mode
    initial_sidebar_state="expanded"
)

components.html(ga_code, height=0)

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