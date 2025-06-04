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

#components.html(ga_code, height=0)
st.components.v1.iframe('https://covid19.aipert.org/google_analytics.html', height=1, scrolling=False)

st.markdown("""
<style>
    [data-testid="stSidebar"] {
        width: 12rem !important;
    }
</style>
""", unsafe_allow_html=True)
    
st.sidebar.header("Selecciona una competición")
st.sidebar.markdown('Autor: Xavi Lluch\n https://x.com/xavi_runner\n\n Github: [JLLUCH](https://github.com/jlluch/VBCstats)')
#Configurar páginas
nav = get_nav_from_toml(path=".streamlit/pages.toml")

# Crea la navegación
pg = st.navigation(nav)

# Ejecuta la página seleccionada
pg.run()

# Syntax:
# st.components.v1.iframe(src, width=None, height=None, scrolling=False)
# 
# Parameters:
# - src (str): The URL of the page to embed
# - width (int or str, optional): The width of the iframe in CSS units (e.g., 100%, 700px)
# - height (int or str, optional): The height of the iframe in CSS units
# - scrolling (bool, optional): Whether to allow scrolling within the iframe

# Example with all parameters:
st.components.v1.iframe(
    src=ga_code,
    width=None,  # Will use default or container width
    height=1,    # 1 pixel height (effectively invisible)
    scrolling=False  # Disable scrolling
)