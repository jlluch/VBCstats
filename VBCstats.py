#Aplicación streamlit para visualizar estadísticas de VBC
# Autor: JLLUCH
# Fecha: 2024-12-20 
#
# """
import streamlit as st
import pandas as pd
from st_pages import get_nav_from_toml
import streamlit.components.v1 as components

sc_code = """
<!-- Default Statcounter code for VBC Stats
https://vbcstats.streamlit.app/ -->
<script type="text/javascript">
var sc_project=13141410; 
var sc_invisible=1; 
var sc_security="8c3d850a"; 
</script>
<script type="text/javascript"
src="https://www.statcounter.com/counter/counter.js"
async></script>
<noscript><div class="statcounter"><a title="Web Analytics
Made Easy - Statcounter" href="https://statcounter.com/"
target="_blank"><img class="statcounter"
src="https://c.statcounter.com/13141410/0/8c3d850a/1/"
alt="Web Analytics Made Easy - Statcounter"
referrerPolicy="no-referrer-when-downgrade"></a></div></noscript>
<!-- End of Statcounter Code -->
"""

# Configuración de la página
st.set_page_config(
    page_title="Estadísticas de Valencia Basket",
    page_icon="🏀",
    layout="wide",  # This forces wide mode
    initial_sidebar_state="expanded"
)

components.html(sc_code, height=0)

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