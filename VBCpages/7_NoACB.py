#Aplicación streamlit para visualizar estadísticas de VBC
# Autor: JLLUCH
# Fecha: 2025-10-10 
#
# """
# from turtle import width
import streamlit as st
import pandas as pd

#Crear una función para cargar los datos de cada competición, de partidos y de jugadores
#Hacer cache de los datos para que no se carguen cada vez que se actualiza la página

@st.cache_data 
def load_data():
    
    df_players_EBA = st.session_state.df_players_EBA
    df_games_EBA = st.session_state.df_games_EBA 
    return df_players_EBA, df_games_EBA

#Cargar los datos
df_players_EBA, df_games_EBA = load_data()


st.title("Estadísticas de temporadas sin ACB")
# Inyecta CSS para cambiar el ancho del selectbox
st.markdown("""
<style>
    .stSelectbox > div {
        width: 400px; /* Ajusta el ancho según sea necesario */
    }
</style>
""", unsafe_allow_html=True)

# Crear tres pestañas para los años sin ACB: 1986, 1987 y 1995
tab1, tab2, tab3 = st.tabs(["1986-87", "1987-88", "1995-96"])

with tab1:
    st.header("Temporada 1986-87")
    # Añadir un cuadro de texto con formato markdown
    st.markdown("""
        La temporada 1986-87 fue la del nacimiento de Pamesa Valencia, disputando la Primera División B.
        No tenemos datos de partidos ni de jugadores. Si alguien los tiene, por favor, que me los envíe.
        La plantilla de Pamesa Valencia fue:""")
    # Crear tabla con los datos de la plantilla
    plantilla_1986_data = {
        'Dorsal': ['-', '-', '4', '5', '8', '9', '10', '11', '12', '13', '14', '15'],
        'Nombre': ['Fernando Jiménez', 'Toni Ferrer', 'JA Lluch', 'Angel Farré', 'Bruno Squarzia', 
                   'Ron Crevier', 'Howard Wood', 'Javier Izquierdo', 'Paco Guillem', 
                   'Víctor Pérez', 'Leo Belloch', 'Paco Pallardó'],
        'Posición': ['2ºEnt', 'Ent', 'E', 'B', 'A', 'P', 'P', 'A-P', 'B', 'A', 'A', 'A-P']
    }
    
    df_plantilla_1986 = pd.DataFrame(plantilla_1986_data)
    st.dataframe(df_plantilla_1986, width= 500, hide_index=True, column_config={
        'Dorsal': st.column_config.Column("Dorsal", width="small"),
        'Nombre': st.column_config.Column("Nombre", width="small"),
        'Posición': st.column_config.Column("Posición", width="small")
    })
    
    st.page_link("https://www.valenciabasket.com/es-1986-87", label="Más información sobre la temporada 1986-87\nFuente: Valencia Basket", icon="ℹ️")

with tab2:
    st.header("Temporada 1987-88")
    # Añadir un cuadro de texto con formato markdown
    st.markdown("""
        La temporada 1987-88 fue la del ascenso de Pamesa Valencia a la ACB, disputando la Primera División B.
        No tenemos datos de partidos ni de jugadores. Si alguien los tiene, por favor, que me los envíe.
        La plantilla de Pamesa Valencia fue:""")
    # Crear tabla con los datos de la plantilla
   

    plantilla_1987_data = {
        'Dorsal': ['-', '-', '5', '6', '7', '8', '10', '11', '12', '13', '14', '15', '7', '12'],
        'Nombre': ['Toni Ferrer', 'Antonio Serra', 'Roberto Íñiguez', 'Paco Solsona', 'Orlando Phillips', 
                'Javier Morant', 'Sergio Coterón', 'Javier Jerry Herranz', 'Paco Guillem', 
                'Jordi Fernández', 'Clyde Mayes', 'Paco Pallardó', 'Larry Spicer', 'Manu Rodríguez'],
        'Posición': ['2ºEnt', 'Ent', 'B', 'A', 'A-P', 'P', 'A', 'A-P', 'B', 'A', 'P', 'A-P', 'A', 'B']
    }

    df_plantilla_1987 = pd.DataFrame(plantilla_1987_data)
    st.dataframe(df_plantilla_1987, width= 500, hide_index=True, column_config={
        'Dorsal': st.column_config.Column("Dorsal", width="small"),
        'Nombre': st.column_config.Column("Nombre", width="small"),
        'Posición': st.column_config.Column("Posición", width="small")
    })

    st.page_link("https://www.valenciabasket.com/es-1987-88", label="Más información sobre la temporada 1987-88\nFuente: Valencia Basket", icon="ℹ️")

with tab3:
    st.header("Temporada 1995-96")
    # Añadir un cuadro de texto con formato markdown
    st.markdown("""
        La temporada 1995-96 fue la del regreso de Pamesa Valencia a la ACB, disputando la Liga EBA. El entrenador fue el mítico Miki Vukovic.
        En liga EBA, Pamesa Valencia quedó campeón de su grupo y quedó segundo en la fase de ascenso, comprando la plaza de ACB.
        Tenemos los resultados de partidos y acumulados de puntos y minutos.\n
        Gracias al usuario @jujuboto JJ Bosch a través del foro de ACB.COM.\n 
        Si alguien tiene más datos, por favor, que me los envíe.
        Enlaces con más información sobre la temporada 1995-96:
        - [Valencia Basket](https://www.valenciabasket.com/es-1995-96)
        - [Peña Nacho Rodilla](https://penyanachorodilla.blogspot.com/2011/05/15-anos-del-ascenso-moral-de-la-liga.html)
        - [jmalmenzar](http://bancoderesultados.jmalmenzar.com/_bkt/liga_iv/liga_iv_1995_96.php)
        - [Hispaligas](http://www.hispaligas.net/Baloncesto/95-96%20EBA.html)
    """)
    # La tabla es df_games_EBA, las columnas: ID Temporada	Jornada	Fase	VBC Local	VBC Victoria	Puntos VBC	Puntos Rival	Entrenador VBC	ID Entrenador VBC	Equipo Rival
    # Visualizar la tabla de resultados de partidos
    # Solo mostrar las columnas: Jornada, Fase, y el resultado si VBC local, ponerlo antes que el rival
    st.subheader("Resultados de partidos")
    # Crear tabla con los datos de los partidos
    df_results_1995 = df_games_EBA[['Jornada', 'Fase', 'VBC Local', 'Puntos VBC', 'Puntos Rival', 'Equipo Rival']]
    df_results_1995['Resultado'] = df_results_1995.apply(lambda row: f"{'Pamesa Valencia' if row['VBC Local'] else row['Equipo Rival']}: {row['Puntos VBC'] if row['VBC Local'] else row['Puntos Rival']} - {row['Equipo Rival'] if row['VBC Local'] else 'Pamesa Valencia'}: {row['Puntos Rival'] if row['VBC Local'] else row['Puntos VBC']}", axis=1)
    df_results_1995 = df_results_1995[['Jornada', 'Fase', 'Resultado']]
    st.dataframe(df_results_1995, width= 700, hide_index=True, column_config={
        'Jornada': st.column_config.Column("Jornada", width="small"),
        'Fase': st.column_config.Column("Fase", width="medium"),
        'Resultado': st.column_config.Column("Resultado", width="large")
    })
    
    st.subheader("Estadísticas de jugadores")
    st.dataframe(df_players_EBA[['Dorsal', 'Nombre', 'Puntos', 'Partidos', 'Minutos']], width= 700, hide_index=True)
