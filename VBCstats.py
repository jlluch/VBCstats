#Aplicación streamlit para visualizar estadísticas de VBC
# Autor: JLLUCH
# Fecha: 2024-12-20 
#
# """
import streamlit as st
import pandas as pd
from st_pages import get_nav_from_toml
from encrypt_utils import decrypt_csv_file
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuración de la página
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
    
# Cargar visitas iniciales
@st.cache_data
def load_visits():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)

    sheet = client.open("vbcStats").sheet1
    data = sheet.get_all_records()
    return data[-1]["Visitas"] if data else 0

visitas = load_visits()

def load_encrypted_data(file_path):
    try:
        # Get decryption key from secrets
        decryption_key = st.secrets["data_encryption"]["key"]
        return decrypt_csv_file(file_path, decryption_key)
    except Exception as e:
        st.error(f"Error accessing data: {str(e)}")
        return None

#Crear una función para cargar los datos de cada competición, de partidos y de jugadores
#Hacer cache de los datos para que no se carguen cada vez que se actualiza la página

# Crear una columna con el partido
def create_partido_column(df):
    df['Partido'] = df.apply(lambda x: f"VBC - {x['Equipo Rival']}" if x['VBC Local'] else f"{x['Equipo Rival']} - VBC", axis=1)
    return df


@st.cache_data 
def load_data():
    path = r"Data/"
    
    if "df_players_VBC" not in st.session_state:
        df_players_VBC = pd.read_csv(path+"jugadores_VBC.csv")
        
    file_path = path+"estadisticas_jugadores_VBC_ACB.csv.enc"
    if 'df_players_ACB' not in st.session_state:
        df_players_ACB = load_encrypted_data(file_path)
        
    file_path = path+"estadisticas_jugadores_VBC_Eurocup.csv.enc"
    if 'df_players_Eurocup' not in st.session_state:
        df_players_Eurocup = load_encrypted_data(file_path)
        
    file_path = path+"estadisticas_jugadores_VBC_Euroleague.csv.enc"
    if 'df_players_Euroleague' not in st.session_state:
        df_players_Euroleague = load_encrypted_data(file_path)
        
    file_path = path+"estadisticas_jugadores_VBC_Saporta.csv.enc"
    if 'df_players_Saporta' not in st.session_state:
        df_players_Saporta = load_encrypted_data(file_path)
        
    file_path = path+"estadisticas_jugadores_VBC_CopaRey.csv.enc"
    if 'df_players_CopaRey' not in st.session_state:
        df_players_CopaRey = load_encrypted_data(file_path)
        
    df_players_Eurocup['ID Jugador'] = df_players_Eurocup['ID Jugador'].apply(lambda x: df_players_VBC[df_players_VBC['ID Eurocup'] == x]['ID ACB'].values[0] if not df_players_VBC[df_players_VBC['ID Eurocup'] == x].empty else x)
    df_players_Euroleague['ID Jugador'] = df_players_Euroleague['ID Jugador'].apply(lambda x: df_players_VBC[df_players_VBC['ID Euroleague'] == x]['ID ACB'].values[0] if not df_players_VBC[df_players_VBC['ID Euroleague'] == x].empty else x)
    df_players_Saporta['ID Jugador'] = df_players_Saporta['ID Jugador'].apply(lambda x: df_players_VBC[df_players_VBC['ID Saporta'] == x]['ID ACB'].values[0] if not df_players_VBC[df_players_VBC['ID Saporta'] == x].empty else x)


    file_path = path+"estadisticas_partidos_VBC_ACB.csv.enc"
    if 'df_games_ACB' not in st.session_state:
        df_games_ACB = load_encrypted_data(file_path)
        
    file_path = path+"estadisticas_partidos_VBC_Eurocup.csv.enc"
    if 'df_games_Eurocup' not in st.session_state:
        df_games_Eurocup = load_encrypted_data(file_path)
        
    file_path = path+"estadisticas_partidos_VBC_Euroleague.csv.enc"
    if 'df_games_Euroleague' not in st.session_state:
        df_games_Euroleague = load_encrypted_data(file_path)
        
    file_path = path+"estadisticas_partidos_VBC_Saporta.csv.enc"
    if 'df_games_Saporta' not in st.session_state:
        df_games_Saporta = load_encrypted_data(file_path)
        
    file_path = path+"estadisticas_partidos_VBC_CopaRey.csv.enc"
    if 'df_games_CopaRey' not in st.session_state:
        df_games_CopaRey = load_encrypted_data(file_path)
        
    
    # Entrenadores de VBC
    df_coaches_VBC = df_games_ACB[['ID Entrenador VBC', 'Entrenador VBC']].drop_duplicates()

    # Convertit ID Temporada a int
    df_games_ACB['ID Temporada'] = df_games_ACB['ID Temporada'].astype(int)
    df_games_Eurocup['ID Temporada'] = df_games_Eurocup['ID Temporada'].astype(int)
    df_games_Euroleague['ID Temporada'] = df_games_Euroleague['ID Temporada'].astype(int)
    df_games_Saporta['ID Temporada'] = df_games_Saporta['ID Temporada'].astype(int)
    df_games_CopaRey['ID Temporada'] = df_games_CopaRey['ID Temporada'].astype(int)

    # Aplicar la función a cada dataframe de partidos
    df_games_ACB = create_partido_column(df_games_ACB)
    df_games_Eurocup = create_partido_column(df_games_Eurocup)
    df_games_Euroleague = create_partido_column(df_games_Euroleague)
    df_games_Saporta = create_partido_column(df_games_Saporta)
    df_games_CopaRey = create_partido_column(df_games_CopaRey)

    # Crer una columna con el enlace a la página del partido
    df_games_CopaRey['Enlace'] = 'https://www.acb.com/partido/estadisticas/id/' + df_games_CopaRey['ID Partido'].astype(str)
    df_games_ACB['Enlace'] = 'https://www.acb.com/partido/estadisticas/id/' + df_games_ACB['ID Partido'].astype(str)
    df_games_Eurocup['Enlace'] = df_games_Eurocup['ID Partido']
    df_games_Euroleague['Enlace'] = df_games_Euroleague['ID Partido']
    df_games_Saporta['Enlace'] = 'https://www.fibaeurope.com/' + df_games_Saporta['ID Partido'].astype(str)

    # Crear una columna con la diferencia de puntos
    df_games_ACB['Diferencia'] = df_games_ACB['Puntos VBC'] - df_games_ACB['Puntos Rival']
    df_games_Eurocup['Diferencia'] = df_games_Eurocup['Puntos VBC'] - df_games_Eurocup['Puntos Rival']
    df_games_Euroleague['Diferencia'] = df_games_Euroleague['Puntos VBC'] - df_games_Euroleague['Puntos Rival']
    df_games_Saporta['Diferencia'] = df_games_Saporta['Puntos VBC'] - df_games_Saporta['Puntos Rival']
    df_games_CopaRey['Diferencia'] = df_games_CopaRey['Puntos VBC'] - df_games_CopaRey['Puntos Rival']
    
    # Crear una columna con el partido
    df_games_ACB['Partido'] = df_games_ACB.apply(lambda x: f"{x['ID Partido']} - {x['Fecha']} - VBC - {x['Equipo Rival']}"  if x['VBC Local'] else f"{x['ID Partido']} - {x['Fecha']} - {x['Equipo Rival']} - VBC", axis=1)
    df_games_Eurocup['Partido'] = df_games_Eurocup.apply(lambda x: f"{x['ID Partido']} - {x['Fecha']} - VBC - {x['Equipo Rival']}"  if x['VBC Local'] else f"{x['ID Partido']} - {x['Fecha']} - {x['Equipo Rival']} - VBC", axis=1)
    df_games_Euroleague['Partido'] = df_games_Euroleague.apply(lambda x: f"{x['ID Partido']} - {x['Fecha']} - VBC - {x['Equipo Rival']}"  if x['VBC Local'] else f"{x['ID Partido']} - {x['Fecha']} - {x['Equipo Rival']} - VBC", axis=1)
    df_games_Saporta['Partido'] = df_games_Saporta.apply(lambda x: f"{x['ID Partido']} - {x['Fecha']} - VBC - {x['Equipo Rival']}"  if x['VBC Local'] else f"{x['ID Partido']} - {x['Fecha']} - {x['Equipo Rival']} - VBC", axis=1)
    df_games_CopaRey['Partido'] = df_games_CopaRey.apply(lambda x: f"{x['ID Partido']} - {x['Fecha']} - VBC - {x['Equipo Rival']}"  if x['VBC Local'] else f"{x['ID Partido']} - {x['Fecha']} - {x['Equipo Rival']} - VBC", axis=1)   
    
     # Convertir las columnas de fecha a datetime
    df_games_ACB['Fecha'] = pd.to_datetime(df_games_ACB['Fecha'], format='%d/%m/%Y')
    df_games_Eurocup['Fecha'] = pd.to_datetime(df_games_Eurocup['Fecha'], format='%Y-%m-%d')
    df_games_Euroleague['Fecha'] = pd.to_datetime(df_games_Euroleague['Fecha'], format='%Y-%m-%d')
    df_games_Saporta['Fecha'] = pd.to_datetime(df_games_Saporta['Fecha'], format='%d.%m.%y')
    df_games_CopaRey['Fecha'] = pd.to_datetime(df_games_CopaRey['Fecha'], format='%d/%m/%Y')    
    
    return df_players_CopaRey, df_games_CopaRey, df_players_ACB, df_games_ACB, df_players_Eurocup, df_games_Eurocup, df_players_Euroleague, df_games_Euroleague, df_players_Saporta, df_games_Saporta, df_players_VBC, df_coaches_VBC
    

#Cargar todos los datos
df_players_CopaRey, df_games_CopaRey, df_players_ACB, df_games_ACB, df_players_Eurocup, df_games_Eurocup, df_players_Euroleague, df_games_Euroleague, df_players_Saporta, df_games_Saporta, df_players_VBC, df_coaches_VBC = load_data()


df_games_Total = pd.concat([df_games_ACB, df_games_Eurocup, df_games_Euroleague, df_games_Saporta, df_games_CopaRey], ignore_index=True)
df_players_Total = pd.concat([df_players_ACB, df_players_Eurocup, df_players_Euroleague, df_players_Saporta, df_players_CopaRey], ignore_index=True)

# Crear un diccionario que mapee ID Jugador a Nombre a partir de df_players_VBC la clave se llama ID Jugador
player_names = df_players_VBC.set_index('ID ACB')['Nombre ACB'].to_dict()

# Crear un diccionario que mapee ID Entrenador a Nombre a partir de df_coaches_VBC la clave se llama ID Entrenador
coach_names = df_coaches_VBC.set_index('ID Entrenador VBC')['Entrenador VBC'].to_dict()

# Cargar los dataframes en st.session_state para que estén disponibles en todas las páginas
st.session_state['df_players_CopaRey'] = df_players_CopaRey
st.session_state['df_games_CopaRey'] = df_games_CopaRey
st.session_state['df_players_ACB'] = df_players_ACB
st.session_state['df_games_ACB'] = df_games_ACB
st.session_state['df_players_Eurocup'] = df_players_Eurocup
st.session_state['df_games_Eurocup'] = df_games_Eurocup
st.session_state['df_players_Euroleague'] = df_players_Euroleague
st.session_state['df_games_Euroleague'] = df_games_Euroleague
st.session_state['df_players_Saporta'] = df_players_Saporta
st.session_state['df_games_Saporta'] = df_games_Saporta
st.session_state['df_players_VBC'] = df_players_VBC
st.session_state['df_coaches_VBC'] = df_coaches_VBC
st.session_state['df_games_Total'] = df_games_Total
st.session_state['df_players_Total'] = df_players_Total
st.session_state['player_names'] = player_names
st.session_state['coach_names'] = coach_names
  

#Configurar páginas
nav = get_nav_from_toml(path=".streamlit/pages.toml")

# Crea la navegación
pg = st.navigation(nav)


# --- CONTADOR DE VISITAS POR PÁGINA ---
def contar_visita_google_sheets(nombre_pagina):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)

    sheet = client.open("vbcStats").sheet1
    data = sheet.get_all_records()

    for idx, fila in enumerate(data, start=2):
        if fila["Página"] == nombre_pagina:
            visitas = int(fila["Visitas"]) + 1
            sheet.update_cell(idx, 2, visitas)
            # devuelve el número de visitas totales
            return data[-1]["Visitas"]
            
    # Si no existe, añadir
    sheet.append_row([nombre_pagina, 1])
    return 1
# ✅ Obtener nombre de la página seleccionada
nombre_pagina = pg.title

# Solo contar una vez por carga
if "pagina_contada" not in st.session_state or st.session_state.pagina_contada != nombre_pagina:
    visitas = contar_visita_google_sheets(nombre_pagina)
    st.session_state.pagina_contada = nombre_pagina

st.sidebar.header("Selecciona una competición")
st.sidebar.header("Número de partidos:")
st.sidebar.markdown(f"**ACB:** {len(df_games_ACB)}")
st.sidebar.markdown(f"**Eurocup:** {len(df_games_Eurocup)}")    
st.sidebar.markdown(f"**Euroleague:** {len(df_games_Euroleague)}")
st.sidebar.markdown(f"**Saporta:** {len(df_games_Saporta)}")
st.sidebar.markdown(f"**Copa del Rey:** {len(df_games_CopaRey)}")
st.sidebar.markdown(f"**Total:** {len(df_games_Total)}")
# Separador
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Visitas:** {visitas}")
st.sidebar.markdown("---")
st.sidebar.markdown('Autor: Xavi Lluch\n https://x.com/xavi_runner\n Github: [JLLUCH](https://github.com/jlluch/VBCstats)')

# Ejecuta la página seleccionada
pg.run()


