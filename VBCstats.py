#Aplicación streamlit para visualizar estadísticas de VBC
# Autor: JLLUCH
# Fecha: 2024-12-20 
#
# """
import streamlit as st
import pandas as pd
from st_pages import get_nav_from_toml
from encrypt_utils import decrypt_csv_file


st.markdown("""
<style>
    [data-testid="stSidebar"] {
        width: 12rem !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_encrypted_data(file_path):
    try:
        # Get decryption key from secrets
        decryption_key = st.secrets["data_encryption"]["key"]
        return decrypt_csv_file(file_path, decryption_key)
    except Exception as e:
        st.error(f"Error accessing data: {str(e)}")
        return None
    
st.sidebar.header("Selecciona una competición")
#Configurar páginas
nav = get_nav_from_toml(path=".streamlit/pages.toml")

# Crea la navegación
pg = st.navigation(nav)

# Ejecuta la página seleccionada
pg.run()