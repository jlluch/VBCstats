#Aplicación streamlit para visualizar estadísticas de VBC
# Autor: JLLUCH
# Fecha: 2024-12-20 
#
# """
import streamlit as st
import pandas as pd
import ast
from VBCpages.encrypt_utils import decrypt_csv_file

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

@st.cache_data 
def load_data():
    path = r"Data/"
    file_path = path+"estadisticas_jugadores_VBC_CopaRey.csv.enc"
    df_players_CopaRey = load_encrypted_data(file_path)
# Columns: ID Temporada,Jornada,Fase,Fecha,Hora,ID Partido,ID Equipo,Dorsal,Nombre,Titular,ID Jugador,Minutos,Puntos,
# T2a,T2i,T2%,T3a,T3i,T3%,T1a,T1i,T1%,Rebotes,R.Def,R.Ofe,
# Asistencias, Robos,Perdidas,CTP,Tapones,TR,Mates,FPF,FPC,+/-,Val,
# eFG% ,TOV% ,OREB% ,DREB% ,Pace ,ORTG ,DRTG ,Net Rating ,AST/TO ,Posesiones
    file_path = path+"estadisticas_partidos_VBC_CopaRey.csv.enc"
    df_games_CopaRey = load_encrypted_data(file_path)
# Columns: ID Temporada	Jornada	Fase	Fecha	Hora	ID Partido	VBC Local	VBC Victoria	Puntos VBC	Puntos Rival	
# Entrenador VBC	ID Entrenador VBC	Minutos VBC	T2a VBC	T2i VBC	T2% VBC	T3a VBC	T3i VBC	T3% VBC	T1a VBC	T1i VBC	T1% VBC	
# Rebotes VBC	R.Def VBC	R.Ofe VBC	Asistencias VBC	Robos VBC	Perdidas VBC	CTP VBC	Tapones VBC	TR VBC	Mates VBC	
# FPF VBC	FPC VBC	+/- VBC	Val VBC	eFG% VBC	TOV% VBC	OREB% VBC	DREB% VBC	Pace VBC	ORTG VBC	DRTG VBC	
# Net Rating VBC	AST/TO VBC	Posesiones VBC	
# Equipo Rival	ID Rival	Entrenador Rival	ID Entrenador Rival	Minutos Rival	T2a Rival	T2i Rival	T2% Rival	
# T3a Rival	T3i Rival	T3% Rival	T1a Rival	T1i Rival	T1% Rival	Rebotes Rival	R.Def Rival	R.Ofe Rival	Asistencias Rival	
# Robos Rival	Perdidas Rival	CTP Rival	Tapones Rival	TR Rival	Mates Rival	FPF Rival	FPC Rival	+/- Rival	Val Rival	
# eFG% Rival	TOV% Rival	OREB% Rival	DREB% Rival	Pace Rival	ORTG Rival	DRTG Rival	Net Rating Rival	AST/TO Rival	
# Posesiones Rival	P1VBC	P2VBC	Q1VBC	Q2VBC	Q3VBC	Q4VBC	PR1VBC	PR2VBC	
# P1Rival	P2Rival	Q1Rival	Q2Rival	Q3Rival	Q4Rival	PR1Rival	PR2Rival
    return df_players_CopaRey, df_games_CopaRey

#Cargar los datos
df_players_CopaRey, df_games_CopaRey = load_data()

# Crear una columna con el partido
df_games_CopaRey['Partido'] = df_games_CopaRey.apply(lambda x: f"VBC - {x['Equipo Rival']}"  if x['VBC Local'] else f"{x['Equipo Rival']} - VBC", axis=1)

# Crear una columna con el enlace a la página del partido
df_games_CopaRey['Enlace'] = df_games_CopaRey['ID Partido']

# Crear una columna con la diferencia de puntos
df_games_CopaRey['Diferencia'] = df_games_CopaRey['Puntos VBC'] - df_games_CopaRey['Puntos Rival']

st.title("Estadísticas de la Copa del Rey")
# Inyecta CSS para cambiar el ancho del selectbox
st.markdown("""
<style>
    .stSelectbox > div {
        width: 400px; /* Ajusta el ancho según sea necesario */
    }
</style>
""", unsafe_allow_html=True)
#Crear un selectnox para cada marco
marco = st.selectbox("Selecciona una opción", ["Estadísticas de una temporada", "Estadísticas jugadores de una temporada", "Líderes de una temporada", "Estadísticas contra un rival", "Estadísticas de un partido", "Líderes históricos", "Récords equipo", "Entrenadores"])
if marco == "Estadísticas de un partido":
    #Crear un marco para mostrar las estadísticas de un partido en concreto
    st.subheader("Estadísticas de un partido")
    #Seleccionar una temporada, ordenar las temporadas de mayor a menor
    season = st.selectbox("Selecciona una temporada", df_games_CopaRey['ID Temporada'].sort_values(ascending=False).unique())
    #Seleccionar un partido
    # Crea una lista para el selectbox con la fecha, el equipo rival y si VBC es el equipo local
    game_list = df_games_CopaRey[df_games_CopaRey['ID Temporada'] == season][['Fecha','Partido']]
    # Invertir el orden de game_list
    game_list = game_list.iloc[::-1]     
    
    game_list = game_list.apply(lambda x: f"{x['Fecha']} - {x['Partido']}", axis=1)
    game = st.selectbox("Selecciona un partido", game_list)
    date = game.split(" - ")[0]        
    #Mostrar las estadísticas del partido seleccionado
    st.subheader("Datos del partido")
    if game.split(" - ")[1] == "VBC":
        columns_to_show = ['ID Temporada', 'Jornada', 'Fase', 'Fecha', 'Hora', 'Puntos VBC','Equipo Rival','Puntos Rival']
    else:
        columns_to_show = ['ID Temporada', 'Jornada', 'Fase', 'Fecha', 'Hora', 'Equipo Rival','Puntos Rival', 'Puntos VBC']
    st.dataframe(df_games_CopaRey[(df_games_CopaRey['ID Temporada'] == season) & (df_games_CopaRey['Fecha'] == date)][columns_to_show], hide_index=True)
    
    st.subheader("Estadísticas Valencia Basket")
    columns_to_show = ['Minutos VBC', 'T2a VBC','T2i VBC', 'T2% VBC', 'T3a VBC', 'T3i VBC', 'T3% VBC', 'T1a VBC',
    'T1i VBC', 'T1% VBC', 'Rebotes VBC', 'R.Def VBC', 'R.Ofe VBC',
    'Asistencias VBC', 'Robos VBC', 'Perdidas VBC', 
    'Tapones VBC', 'TR VBC',  'FPF VBC', 'FPC VBC', '+/- VBC', 'Val VBC', 
    'P1VBC','P2VBC', 'Q1VBC', 'Q2VBC', 'Q3VBC', 'Q4VBC', 'PR1VBC', 'PR2VBC']
    st.dataframe(df_games_CopaRey[(df_games_CopaRey['ID Temporada'] == season) & (df_games_CopaRey['Fecha'] == date)][columns_to_show], hide_index=True)
    
    st.subheader("Estadísticas del rival")
    columns_to_show = ['Minutos Rival', 'T2a Rival', 'T2i Rival',
    'T2% Rival', 'T3a Rival', 'T3i Rival', 'T3% Rival', 'T1a Rival',
    'T1i Rival', 'T1% Rival', 'Rebotes Rival', 'R.Def Rival', 'R.Ofe Rival',
    'Asistencias Rival', 'Robos Rival', 'Perdidas Rival', 
    'Tapones Rival', 'TR Rival', 'FPF Rival', 'FPC Rival','+/- Rival', 'Val Rival', 
    'P1Rival', 'P2Rival', 'Q1Rival', 'Q2Rival', 'Q3Rival', 'Q4Rival',
    'PR1Rival', 'PR2Rival']
    st.dataframe(df_games_CopaRey[(df_games_CopaRey['ID Temporada'] == season) & (df_games_CopaRey['Fecha'] == date)][columns_to_show], hide_index=True)
elif marco == "Líderes históricos":    
    #Crear un marco para mostrar los líderes históricos
    st.subheader("Líderes históricos")
    lh = 10
    # Poner un radio button para seleccionar por estadística total o por partido
    tipo = st.radio("Selecciona el tipo de estadística", ["Total", "Por partido"])
    if tipo == "Total":
        # Calcular los "lh" jugadores con el mayor número de partidos jugados, puntos, rebotes, asistencias, robos, tapones y valoración
        # Añadir una fila en cada tabla con el judador de la temporada actual 
        # Mostrar los resultados en una tabla

        st.markdown('<span style="color: #FF2222;">En rojo los jugadores de la temporada actual</span>', unsafe_allow_html=True)

        max_games = df_players_CopaRey.groupby('Nombre')['ID Partido'].count().sort_values(ascending=False)
        #Cambiar nombre de la columna
        max_games = max_games.rename("Partidos")
        max_points = df_players_CopaRey.groupby('Nombre')['Puntos'].sum().sort_values(ascending=False)
        max_rebounds = df_players_CopaRey.groupby('Nombre')['Rebotes'].sum().sort_values(ascending=False)
        max_assists = df_players_CopaRey.groupby('Nombre')['Asistencias'].sum().sort_values(ascending=False)
        max_steals = df_players_CopaRey.groupby('Nombre')['Robos'].sum().sort_values(ascending=False)
        max_blocks = df_players_CopaRey.groupby('Nombre')['Tapones'].sum().sort_values(ascending=False)
        max_val = df_players_CopaRey.groupby('Nombre')['Val'].sum().sort_values(ascending=False)
        #Cambiar nombre de la columna
        max_val = max_val.rename("Valoración")
        
        # Calcular el mayor número de tiros de 1,2 y 3 puntos anotados (mínimo 100) y el mayor porcentaje de tiros de 1,2 y 3 puntos anotados (mínimo 100 intentos)
        # Mostrar los resultados en una tabla
        # Crea una tabla con el acumulado de tiros de 1,2 y 3 puntos anotados, intentados y el porcentaje de acierto de cada jugador
        tmin = 30 # Mínimo de tiros para mostrar el porcentaje
        shots = df_players_CopaRey.groupby('Nombre')[['T1a', 'T1i', 'T2a', 'T2i', 'T3a', 'T3i']].sum()
        # Calula el porcentaje de acierto de cada jugador con 1 decimal
        shots['T1%'] = round(shots['T1a'] / shots['T1i'] * 100,1)
        shots['T2%'] = round(shots['T2a'] / shots['T2i'] * 100,1)
        shots['T3%'] = round(shots['T3a'] / shots['T3i'] * 100,1)
        max_t1a = shots[shots['T1a'] >= tmin]['T1a'].sort_values(ascending=False)
        #Cambiar nombre de la columna
        max_t1a = max_t1a.rename("T.Libres")
        max_t2a = shots[shots['T2a'] >= tmin]['T2a'].sort_values(ascending=False)
        #Cambiar nombre de la columna
        max_t2a = max_t2a.rename("T2")
        max_t3a = shots[shots['T3a'] >= tmin]['T3a'].sort_values(ascending=False)
        #Cambiar nombre de la columna
        max_t3a = max_t3a.rename("T3")
        max_t1p = (shots[shots['T1a'] >= tmin]['T1%']).sort_values(ascending=False)
        #Cambiar nombre de la columna
        max_t1p = max_t1p.rename("T1%")
        # Añade una columna con el total de tiros libres anotados
        shots['T.Libres'] = shots['T1a']
        max_t1p = max_t1p.to_frame()
        max_t1p['T.Libres'] = shots.loc[max_t1p.index, 'T.Libres']
        max_t2p = (shots[shots['T2a'] >= tmin]['T2%']).sort_values(ascending=False)
        #Cambiar nombre de la columna
        max_t2p = max_t2p.rename("T2%")
        shots['T2'] = shots['T2a']
        max_t2p = max_t2p.to_frame()
        max_t2p['T2'] = shots.loc[max_t2p.index, 'T2']
        max_t3p = (shots[shots['T3a'] >= tmin]['T3%']).sort_values(ascending=False)
        #Cambiar nombre de la columna
        max_t3p = max_t3p.rename("T3%")
        shots['T3'] = shots['T3a']
        max_t3p = max_t3p.to_frame()
        max_t3p['T3'] = shots.loc[max_t3p.index, 'T3']
        # En cada tabla busca el jugador de la temporada actual con mayor estadística, selecciona los 10 primeros y añade una fila con sus estadísticas
        current_season = df_players_CopaRey['ID Temporada'].max()
        # Selecciona el ID de los jugadores de la temporada actual
        current_players = df_players_CopaRey[df_players_CopaRey['ID Temporada'] == current_season]['ID Jugador'].unique()
        # Filtra los jugadores de la temporada actual
        current_players_df = df_players_CopaRey[df_players_CopaRey['ID Jugador'].isin(current_players)]
        # Encuentra el jugador con la mayor estadística en cada tabla
        max_games_current = current_players_df.groupby('Nombre')['ID Partido'].count().sort_values(ascending=False).head(1)
        max_points_current = current_players_df.groupby('Nombre')['Puntos'].sum().sort_values(ascending=False).head(1)
        max_rebounds_current = current_players_df.groupby('Nombre')['Rebotes'].sum().sort_values(ascending=False).head(1)
        max_assists_current = current_players_df.groupby('Nombre')['Asistencias'].sum().sort_values(ascending=False).head(1)
        max_steals_current = current_players_df.groupby('Nombre')['Robos'].sum().sort_values(ascending=False).head(1)
        max_blocks_current = current_players_df.groupby('Nombre')['Tapones'].sum().sort_values(ascending=False).head(1)
        max_val_current = current_players_df.groupby('Nombre')['Val'].sum().sort_values(ascending=False).head(1)
        max_t1a_current = current_players_df.groupby('Nombre')['T1a'].sum().sort_values(ascending=False).head(1)
        max_t2a_current = current_players_df.groupby('Nombre')['T2a'].sum().sort_values(ascending=False).head(1)
        max_t3a_current = current_players_df.groupby('Nombre')['T3a'].sum().sort_values(ascending=False).head(1)
        # Añadir los jugadores de la temporada actual a las tablas
        max_games = pd.concat([max_games.head(lh), max_games_current]).reset_index()
        max_games = max_games.rename(columns={0: 'Partidos'})
        max_points = pd.concat([max_points.head(lh), max_points_current]).reset_index()
        max_rebounds = pd.concat([max_rebounds.head(lh), max_rebounds_current]).reset_index()
        max_assists = pd.concat([max_assists.head(lh), max_assists_current]).reset_index()
        max_steals = pd.concat([max_steals.head(lh), max_steals_current]).reset_index()
        max_blocks = pd.concat([max_blocks.head(lh), max_blocks_current]).reset_index()
        max_val = pd.concat([max_val.head(lh), max_val_current]).reset_index()
        max_val = max_val.rename(columns={0: 'Valoración'})
        max_t1a = pd.concat([max_t1a.head(lh), max_t1a_current]).reset_index()
        max_t1a = max_t1a.rename(columns={0: 'T.Libres'})
        max_t2a = pd.concat([max_t2a.head(lh), max_t2a_current]).reset_index()
        max_t2a = max_t2a.rename(columns={0: 'T2'})
        max_t3a = pd.concat([max_t3a.head(lh), max_t3a_current]).reset_index()
        max_t3a = max_t3a.rename(columns={0: 'T3'})
        
       
        # Muestra los resultados en tablas y en columnas de streamlit separadas

        def highlight_last_row(df):
            # Devuelve estilos para poner la última fila en negrita
            styles = pd.DataFrame('', index=df.index, columns=df.columns)
            if len(df) > 0:
                styles.iloc[-1, :] = 'font-weight: bold; color: #FF2222;'  # Cambia el color y el estilo según tus preferencias
            return styles

        mg, mp, mr, ma = st.columns(4)
        mg.dataframe(
            max_games.style.apply(highlight_last_row, axis=None),
            hide_index=True,
            height=12*35,
            column_config={"Nombre": st.column_config.TextColumn(width="medium")}
        )
        mp.dataframe(
            max_points.style.apply(highlight_last_row, axis=None),
            hide_index=True,
            height=12*35,
            column_config={"Nombre": st.column_config.TextColumn(width="medium")}
        )
        mr.dataframe(
            max_rebounds.style.apply(highlight_last_row, axis=None),
            hide_index=True,
            height=12*35,
            column_config={"Nombre": st.column_config.TextColumn(width="medium")}
        )
        ma.dataframe(
            max_assists.style.apply(highlight_last_row, axis=None),
            hide_index=True,
            height=12*35,
            column_config={"Nombre": st.column_config.TextColumn(width="medium")}
        )

        ms, mb, mv, mn = st.columns(4)
        ms.dataframe(
            max_steals.style.apply(highlight_last_row, axis=None),
            hide_index=True,
            height=12*35,
            column_config={"Nombre": st.column_config.TextColumn(width="medium")}
        )
        mb.dataframe(
            max_blocks.style.apply(highlight_last_row, axis=None),
            hide_index=True,
            height=12*35,
            column_config={"Nombre": st.column_config.TextColumn(width="medium")}
        )
        mv.dataframe(
            max_val.style.apply(highlight_last_row, axis=None),
            hide_index=True,
            height=12*35,
            column_config={"Nombre": st.column_config.TextColumn(width="medium")}
        )

        st.write("Máximos tiros anotados de 1,2 y 3 puntos")
        mt1a, mt2a, mt3a, mn = st.columns(4)
        mt1a.dataframe(
            max_t1a.style.apply(highlight_last_row, axis=None),
            hide_index=True,
            height=12*35,
            column_config={"Nombre": st.column_config.TextColumn(width="medium"), "T.Libres": st.column_config.TextColumn(width="small")}
        )
        mt2a.dataframe(
            max_t2a.style.apply(highlight_last_row, axis=None),
            hide_index=True,
            height=12*35,
            column_config={"Nombre": st.column_config.TextColumn(width="medium"), "T2": st.column_config.TextColumn(width="small")}
        )
        mt3a.dataframe(
            max_t3a.style.apply(highlight_last_row, axis=None),
            hide_index=True,
            height=12*35,
            column_config={"Nombre": st.column_config.TextColumn(width="medium"), "T3": st.column_config.TextColumn(width="small")}
        )

        st.write(f"Mejores porcentajes con al menos {tmin} tiros anotados")
        mt1p, mt2p, mt3p = st.columns(3)
        mt1p.dataframe(max_t1p.head(lh), column_config={"Nombre": st.column_config.TextColumn(width="medium"),"T1%": st.column_config.TextColumn(width="small")})
        mt2p.dataframe(max_t2p.head(lh), column_config={"Nombre": st.column_config.TextColumn(width="medium"),"T2%": st.column_config.TextColumn(width="small")})
        mt3p.dataframe(max_t3p.head(lh), column_config={"Nombre": st.column_config.TextColumn(width="medium"),"T3%": st.column_config.TextColumn(width="small")})
        
    else: # Por partido
        # Calcular los "lh" jugadores con la mayor media por partido de puntos, rebotes, asistencias, robos, tapones y valoración
        # Mostrar los resultados en una tabla
        st.write ("Jugadores con al menos 30 partidos")
        # Filtrar jugadores con al menos 30 partidos
        filtered_players = df_players_CopaRey.groupby('Nombre')['ID Partido'].count()
        filtered_players = filtered_players[filtered_players >= 30].index

        max_games = df_players_CopaRey[df_players_CopaRey['Nombre'].isin(filtered_players)].groupby('Nombre')['ID Partido'].count()
        max_points = pd.DataFrame(df_players_CopaRey[df_players_CopaRey['Nombre'].isin(filtered_players)].groupby('Nombre')['Puntos'].sum())
        # Calcular la media por partido, teniendo en cuenta los partidos que ha jugado cada jugador
        max_points['Media'] = round(max_points['Puntos']/max_games,1)        
        max_points = max_points.sort_values(by='Media',ascending=False).head(lh)
        
        max_rebounds = pd.DataFrame(df_players_CopaRey[df_players_CopaRey['Nombre'].isin(filtered_players)].groupby('Nombre')['Rebotes'].sum())
        # Calcular la media por partido, teniendo en cuenta los partidos que ha jugado cada jugador
        max_rebounds['Media'] = round(max_rebounds['Rebotes']/max_games,1)
        max_rebounds = max_rebounds.sort_values(by='Media',ascending=False).head(lh)
        
        max_assists = pd.DataFrame(df_players_CopaRey[df_players_CopaRey['Nombre'].isin(filtered_players)].groupby('Nombre')['Asistencias'].sum())
        # Calcular la media por partido, teniendo en cuenta los partidos que ha jugado cada jugador
        max_assists['Media'] = round(max_assists['Asistencias']/max_games,1)
        max_assists = max_assists.sort_values(by='Media',ascending=False).head(lh)
        
        max_steals = pd.DataFrame(df_players_CopaRey[df_players_CopaRey['Nombre'].isin(filtered_players)].groupby('Nombre')['Robos'].sum())
        # Calcular la media por partido, teniendo en cuenta los partidos que ha jugado cada jugador
        max_steals['Media'] = round(max_steals['Robos']/max_games,1)
        max_steals = max_steals.sort_values(by='Media',ascending=False).head(lh)
        
        max_blocks = pd.DataFrame(df_players_CopaRey[df_players_CopaRey['Nombre'].isin(filtered_players)].groupby('Nombre')['Tapones'].sum())
        # Calcular la media por partido, teniendo en cuenta los partidos que ha jugado cada jugador
        max_blocks['Media'] = round(max_blocks['Tapones']/max_games,1)
        max_blocks = max_blocks.sort_values(by='Media',ascending=False).head(lh)
        
        max_val = pd.DataFrame(df_players_CopaRey[df_players_CopaRey['Nombre'].isin(filtered_players)].groupby('Nombre')['Val'].sum())
        # Calcular la media por partido, teniendo en cuenta los partidos que ha jugado cada jugador
        max_val['Media'] = round(max_val['Val']/max_games,1)
        max_val = max_val.sort_values(by='Media',ascending=False).head(lh)
        
        # Calcular el mayor número de tiros de 1,2 y 3 puntos anotados por partido
        # Mostrar los resultados en una tabla
        max_T1a = pd.DataFrame(df_players_CopaRey[df_players_CopaRey['Nombre'].isin(filtered_players)].groupby('Nombre')['T1a'].sum())
        # Renombrar la columna
        max_T1a = max_T1a.rename(columns={"T1a": "T.Libres"})
        # Calcular la media por partido, teniendo en cuenta los partidos que ha jugado cada jugador
        max_T1a['Media'] = round(max_T1a['T.Libres']/max_games,1)
        max_T1a = max_T1a.sort_values(by='Media',ascending=False).head(lh)

        max_T2a = pd.DataFrame(df_players_CopaRey[df_players_CopaRey['Nombre'].isin(filtered_players)].groupby('Nombre')['T2a'].sum())
        # Renombrar la columna
        max_T2a = max_T2a.rename(columns={"T2a": "T2"})
        # Calcular la media por partido, teniendo en cuenta los partidos que ha jugado cada jugador
        max_T2a['Media'] = round(max_T2a['T2']/max_games,1)
        max_T2a = max_T2a.sort_values(by='Media',ascending=False).head(lh)
        
        max_T3a = pd.DataFrame(df_players_CopaRey[df_players_CopaRey['Nombre'].isin(filtered_players)].groupby('Nombre')['T3a'].sum())
        # Renombrar la columna
        max_T3a = max_T3a.rename(columns={"T3a": "T3"})
        # Calcular la media por partido, teniendo en cuenta los partidos que ha jugado cada jugador
        max_T3a['Media'] = round(max_T3a['T3']/max_games,1)
        max_T3a = max_T3a.sort_values(by='Media',ascending=False).head(lh)
        
        # Muestra los resultados en tablas y en columnas de streamlit separadas
        mp, mr, ma = st.columns(3)
        mp.dataframe(max_points,column_config={"Nombre": st.column_config.TextColumn(width="medium")})
        mr.dataframe(max_rebounds,column_config={"Nombre": st.column_config.TextColumn(width="medium")})
        ma.dataframe(max_assists,column_config={"Nombre": st.column_config.TextColumn(width="medium")})
        
        ms, mb, mv = st.columns(3)
        ms.dataframe(max_steals,column_config={"Nombre": st.column_config.TextColumn(width="medium")})
        mb.dataframe(max_blocks,column_config={"Nombre": st.column_config.TextColumn(width="medium")})
        mv.dataframe(max_val,column_config={"Nombre": st.column_config.TextColumn(width="medium")})
            
        #Muestra los resultados en tablas y en columnas de streamlit separadas
        mt1a, mt2a, mt3a = st.columns(3)
        mt1a.dataframe(max_T1a,column_config={"Nombre": st.column_config.TextColumn(width="medium"),"T.Libres": st.column_config.TextColumn(width="small")})
        mt2a.dataframe(max_T2a,column_config={"Nombre": st.column_config.TextColumn(width="medium"),"T2": st.column_config.TextColumn(width="small")})
        mt3a.dataframe(max_T3a,column_config={"Nombre": st.column_config.TextColumn(width="medium"),"T3": st.column_config.TextColumn(width="small")})      

elif marco == "Estadísticas de una temporada":
    
    #Seleccionar una temporada, ordenar las temporadas de mayor a menor
    season = st.selectbox("Selecciona una temporada", df_games_CopaRey['ID Temporada'].sort_values(ascending=False).unique())

    #Crear un marco para mostrar los acumulados de la temporada
    st.subheader("Acumulados de la temporada "+str(season))
    
    # Añadir filtros
    st.write("Filtros")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Radio button para filtrar por victorias/derrotas
        resultado_filtro = st.radio("Resultado", ["Todos", "Victorias", "Derrotas"], horizontal=True)
    
    # Obtener el rango de jornadas de la temporada
    jornadas_temporada = df_games_CopaRey[df_games_CopaRey['ID Temporada'] == season]['Jornada'].unique()
    min_jornada = min(jornadas_temporada)
    max_jornada = max(jornadas_temporada)
    
    with col2:
        # Spinner para seleccionar jornada inicial
        jornada_inicio = st.number_input("Jornada inicial", min_value=min_jornada, max_value=max_jornada, value=min_jornada)
    
    with col3:
        # Spinner para seleccionar jornada final, debe ser mayor o igual que jornada_inicio
        jornada_fin = st.number_input("Jornada final", min_value=jornada_inicio, max_value=max_jornada, value=max_jornada)
    
    # Filtrar partidos por temporada
    season_games = df_games_CopaRey[df_games_CopaRey['ID Temporada'] == season]
    
    # Filtrar por jornadas
    season_games = season_games[(season_games['Jornada'] >= jornada_inicio) & 
                                (season_games['Jornada'] <= jornada_fin)]
    
    # Filtrar por resultado (victorias/derrotas)
    if resultado_filtro == "Victorias":
        season_games = season_games[season_games['VBC Victoria'] == 1]
    elif resultado_filtro == "Derrotas":
        season_games = season_games[season_games['VBC Victoria'] == 0]
    
    # Mostrar información sobre los filtros aplicados
    filtros_aplicados = []
    if resultado_filtro != "Todos":
        filtros_aplicados.append(f"Resultado: {resultado_filtro}")
    if jornada_inicio > min_jornada or jornada_fin < max_jornada:
        filtros_aplicados.append(f"Jornadas: {jornada_inicio} a {jornada_fin}")
    
    if filtros_aplicados:
        st.write(f"**Filtros aplicados:** {', '.join(filtros_aplicados)}")
    
    # Si no quedan partidos después del filtrado, mostrar mensaje y salir
    if len(season_games) == 0:
        st.warning("No hay datos disponibles para los filtros seleccionados.")
    else:
        # Calcular total partidos jugados, victorias y derrotas, total como local y como visitante y % de cada uno
        # usando los datos filtrados
        total_games = len(season_games)
        total_wins = season_games['VBC Victoria'].sum()
        total_losses = total_games - total_wins
        total_home = season_games['VBC Local'].sum()
        total_away = total_games - total_home
        total_home_wins = season_games[season_games['VBC Local'] == 1]['VBC Victoria'].sum()
        total_away_wins = season_games[season_games['VBC Local'] == 0]['VBC Victoria'].sum()
        total_home_losses = total_home - total_home_wins
        total_away_losses = total_away - total_away_wins
        total_home_wins_percentage = round(total_home_wins * 100 / total_home, 1) if total_home > 0 else 0
        total_away_wins_percentage = round(total_away_wins * 100 / total_away, 1) if total_away > 0 else 0
        total_wins_percentage = round(total_wins * 100 / total_games, 1) if total_games > 0 else 0
        total_losses_percentage = round(total_losses * 100 / total_games, 1) if total_games > 0 else 0
        
        # Crear un dataframe con los datos
        season_stats = pd.DataFrame({
            'Partidos': [total_games],
            'Victorias': [total_wins],
            'Derrotas': [total_losses],
            'Local': [total_home],
            'Visitante': [total_away],
            'Vic. Local': [total_home_wins],
            'Vic. Visitante': [total_away_wins],
            'Der. Local': [total_home_losses],
            'Der. Visitante': [total_away_losses],
            'Victorias %': [total_wins_percentage],
            'Derrotas %': [total_losses_percentage],
            'Vic. Local %': [total_home_wins_percentage],
            'Vic. Visitante %': [total_away_wins_percentage],
        })
        
        # Crear 3 columnas para mostrar los datos
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Partidos")
            st.dataframe(
                season_stats[['Partidos', 'Victorias', 'Derrotas']],
                hide_index=True,
                column_config={
                    "Partidos": st.column_config.NumberColumn(width="small"),
                    "Victorias": st.column_config.NumberColumn(width="small"),
                    "Derrotas": st.column_config.NumberColumn(width="small"),
                }
            )   
        with col2:
            st.write("Local/Visitante")
            st.dataframe(
                season_stats[['Local', 'Visitante', 'Vic. Local', 'Vic. Visitante', 'Der. Local', 'Der. Visitante']],
                hide_index=True,
                column_config={
                    "Local": st.column_config.NumberColumn(width="small"),
                    "Visitante": st.column_config.NumberColumn(width="small"),
                    "Vic. Local": st.column_config.NumberColumn(width="small"),
                    "Vic. Visitante": st.column_config.NumberColumn(width="small"),
                    "Der. Local": st.column_config.NumberColumn(width="small"),
                    "Der. Visitante": st.column_config.NumberColumn(width="small"),
                }
            )   
        with col3:
            st.write("Porcentajes")
            st.dataframe(
                season_stats[['Victorias %', 'Derrotas %', 'Vic. Local %', 'Vic. Visitante %']],
                hide_index=True,
                column_config={
                    "Victorias %": st.column_config.NumberColumn(width="small"),
                    "Derrotas %": st.column_config.NumberColumn(width="small"),
                    "Vic. Local %": st.column_config.NumberColumn(width="small"),
                    "Vic. Visitante %": st.column_config.NumberColumn(width="small"),
                }
            )
        
        # Calcular los acumulados de la temporada VBC usando los datos filtrados
        season_stats_vbc = pd.DataFrame(season_games[['Puntos VBC', 'Rebotes VBC', 'Asistencias VBC', 'Robos VBC', 'Tapones VBC', 'Val VBC']].sum(), columns=['Acumulados'])
        season_stats_vbc['Media'] = round(season_stats_vbc['Acumulados'] / len(season_games), 1)
        
        # Calcular los acumulados de la temporada Rival
        season_stats_rival = pd.DataFrame(season_games[['Puntos Rival', 'Rebotes Rival', 'Asistencias Rival', 'Robos Rival', 'Tapones Rival', 'Val Rival']].sum(), columns=['Acumulados'])
        season_stats_rival['Media'] = round(season_stats_rival['Acumulados'] / len(season_games), 1)
        
        # Datos de tiros VBC
        season_shots_vbc = pd.DataFrame(season_games[['T1a VBC', 'T1i VBC', 'T2a VBC', 'T2i VBC', 'T3a VBC', 'T3i VBC']].sum(), columns=['Acumulados'])
        season_shots_vbc['Media'] = round(season_shots_vbc['Acumulados'] / len(season_games), 1)
        season_shots_vbc['%'] = round(season_shots_vbc['Acumulados']*100 / season_shots_vbc['Acumulados'].shift(-1), 1)
        
        # Datos de tiros Rival
        season_shots_rival = pd.DataFrame(season_games[['T1a Rival', 'T1i Rival', 'T2a Rival', 'T2i Rival', 'T3a Rival', 'T3i Rival']].sum(), columns=['Acumulados'])
        season_shots_rival['Media'] = round(season_shots_rival['Acumulados'] / len(season_games), 1)
        season_shots_rival['%'] = round(season_shots_rival['Acumulados']*100 / season_shots_rival['Acumulados'].shift(-1), 1)
        
        # Crear 4 columnas para mostrar los datos
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.write("VBC Estadísticas")
            st.dataframe(
                season_stats_vbc,
                column_config={
                    "Acumulados": st.column_config.NumberColumn(width="small"),
                    "Media":      st.column_config.NumberColumn(width="small"),
                }
            )
        with col2:
            st.write("Rival Estadísticas")
            st.dataframe(
                season_stats_rival,
                column_config={
                    "Acumulados": st.column_config.NumberColumn(width="small"),
                    "Media":      st.column_config.NumberColumn(width="small"),
                }
            )
        with col3:
            st.write("VBC Tiros")
            st.dataframe(
                season_shots_vbc.iloc[::2],
                column_config={
                    "Acumulados": st.column_config.NumberColumn(width="small"),
                    "Media":      st.column_config.NumberColumn(width="small"),
                    "%":          st.column_config.NumberColumn(width="small"),
                }
            )
        with col4:
            st.write("Rival Tiros")
            st.dataframe(
                season_shots_rival.iloc[::2],
                column_config={
                    "Acumulados": st.column_config.NumberColumn(width="small"),
                    "Media":      st.column_config.NumberColumn(width="small"),
                    "%":          st.column_config.NumberColumn(width="small"),
                }
            )

elif marco == "Líderes de una temporada":
    
    #Seleccionar una temporada, ordenar las temporadas de mayor a menor
    season = st.selectbox("Selecciona una temporada", df_games_CopaRey['ID Temporada'].sort_values(ascending=False).unique(), index=0)
    #Crear un marco para mostrar los acumulados de la temporada
    st.subheader("Líderes de la temporada "+str(season))
    #Crear un marco para mostrar los líderes de la temporada, lo mismo que en el marco de líderes históricos pero solo para la temporada actual
    lh = 5
    # Calcular los "lh" jugadores con el mayor número de partidos jugados, puntos, rebotes, asistencias, robos, tapones y valoración
    # Mostrar los resultados en una tabla   
    season_games = df_players_CopaRey[df_players_CopaRey['ID Temporada'] == season]
    max_games = season_games.groupby('Nombre')['ID Partido'].count()
    max_points = pd.DataFrame(season_games.groupby('Nombre')['Puntos'].sum())
    # Calcular la media por partido, teniendo en cuenta los partidos que ha jugado cada jugador
    max_points['Media'] = round(max_points['Puntos']/max_games,1)        
    max_points = max_points.sort_values(by='Puntos',ascending=False).head(lh)
    
    max_rebounds = pd.DataFrame(season_games.groupby('Nombre')['Rebotes'].sum())
    # Calcular la media por partido, teniendo en cuenta los partidos que ha jugado cada jugador
    max_rebounds['Media'] = round(max_rebounds['Rebotes']/max_games,1)
    max_rebounds = max_rebounds.sort_values(by='Rebotes',ascending=False).head(lh)
    
    max_assists = pd.DataFrame(season_games.groupby('Nombre')['Asistencias'].sum())
    # Calcular la media por partido, teniendo en cuenta los partidos que ha jugado cada jugador
    max_assists['Media'] = round(max_assists['Asistencias']/max_games,1)
    max_assists = max_assists.sort_values(by='Asistencias',ascending=False).head(lh)
    
    max_steals = pd.DataFrame(season_games.groupby('Nombre')['Robos'].sum())
    # Calcular la media por partido, teniendo en cuenta los partidos que ha jugado cada jugador
    max_steals['Media'] = round(max_steals['Robos']/max_games,1)
    max_steals = max_steals.sort_values(by='Robos',ascending=False).head(lh)
    
    max_blocks = pd.DataFrame(season_games.groupby('Nombre')['Tapones'].sum())
    # Calcular la media por partido, teniendo en cuenta los partidos que ha jugado cada jugador
    max_blocks['Media'] = round(max_blocks['Tapones']/max_games,1)
    max_blocks = max_blocks.sort_values(by='Tapones',ascending=False).head(lh)
    
    max_val = pd.DataFrame(season_games.groupby('Nombre')['Val'].sum())
    # Calcular la media por partido, teniendo en cuenta los partidos que ha jugado cada jugador
    max_val['Media'] = round(max_val['Val']/max_games,1)
    max_val = max_val.sort_values(by='Val',ascending=False).head(lh)
    
    #Ordenar partidos jugados
    max_games = max_games.sort_values(ascending=False).head(lh)
    #Cambiar nombre de la columna
    max_games = max_games.rename("Partidos")        
    # Calcular el mayor número de tiros de 1,2 y 3 puntos anotados y el mayor porcentaje de tiros de 1,2 y 3 puntos anotados
    # Mostrar los resultados en una tabla
    # Crea una tabla con el acumulado de tiros de 1,2 y 3 puntos anotados, intentados y el porcentaje de acierto de cada jugador
    shots = season_games.groupby('Nombre')[['T1a', 'T1i', 'T2a', 'T2i', 'T3a', 'T3i']].sum()
    # Calula el porcentaje de acierto de cada jugador con 1 decimal
    shots['T1%'] = round(shots['T1a'] / shots['T1i'] * 100,1)
    shots['T2%'] = round(shots['T2a'] / shots['T2i'] * 100,1)
    shots['T3%'] = round(shots['T3a'] / shots['T3i'] * 100,1)
    max_t1a = shots['T1a'].sort_values(ascending=False).head(lh)
    #Cambiar nombre de la columna
    max_t1a = max_t1a.rename("T.Libres")
    max_t2a = shots['T2a'].sort_values(ascending=False).head(lh)
    #Cambiar nombre de la columna
    max_t2a = max_t2a.rename("T2")
    max_t3a = shots['T3a'].sort_values(ascending=False).head(lh)
    #Cambiar nombre de la columna
    max_t3a = max_t3a.rename("T3")
    max_t1p = (shots['T1%']).sort_values(ascending=False).head(lh)
    #Cambiar nombre de la columna
    max_t1p = max_t1p.rename("T1%")
    max_t2p = (shots['T2%']).sort_values(ascending=False).head(lh)
    #Cambiar nombre de la columna
    max_t2p = max_t2p.rename("T2%")
    max_t3p = (shots['T3%']).sort_values(ascending=False).head(lh)
    #Cambiar nombre de la columna
    max_t3p = max_t3p.rename("T3%")
    
    # Muestra los resultados en tablas y en columnas de streamlit separadas
    mg, mp, mr, ma = st.columns(4)
    mg.dataframe(max_games)
    mp.dataframe(max_points)
    mr.dataframe(max_rebounds)
    ma.dataframe(max_assists)
    
    ms, mb, mv, vc = st.columns(4)
    ms.dataframe(max_steals)
    mb.dataframe(max_blocks)
    mv.dataframe(max_val)
    
    # Muestra los resultados en tablas y en columnas de streamlit separadas
    mt1a, mt1p, mt2a, mt2p, mt3a, mt3p = st.columns(6)
    mt1a.dataframe(max_t1a, column_config={"T.Libres": st.column_config.TextColumn(width="medium")})
    mt1p.dataframe(max_t1p, column_config={"T1%": st.column_config.TextColumn(width="medium")})
    mt2a.dataframe(max_t2a, column_config={"T2": st.column_config.TextColumn(width="medium")})
    mt2p.dataframe(max_t2p, column_config={"T2%": st.column_config.TextColumn(width="medium")})
    mt3a.dataframe(max_t3a, column_config={"T3": st.column_config.TextColumn(width="medium")})
    mt3p.dataframe(max_t3p, column_config={"T3%": st.column_config.TextColumn(width="medium")})
    
elif marco == "Récords equipo":
    lh = 10
    #Crear un marco para mostrar los récords del equipo
    st.subheader("Récords del equipo")
    #Crear una tabla con los 10 mejores récords del equipo en puntos, puntos en una parte, puntos en un cuarto, rebotes, asistencias, robos, tapones, valoración, tiros de 1,2 y 3 puntos anotados y porcentaje de acierto en un partido
    #Puntos partido
    max10_points = df_games_CopaRey.sort_values(by='Puntos VBC',ascending=False).head(lh)
    #Seleccionar las columnas a mostrar
    columns_to_show = ['ID Temporada', 'Jornada', 'Fecha', 'Partido', 'Puntos VBC', 'Puntos Rival', 'Enlace']
    st.write("Récords en puntos")
    st.dataframe(max10_points[columns_to_show], hide_index=True)
    
    # Diferencia de puntos
    max10_diff = df_games_CopaRey.sort_values(by='Diferencia',ascending=False).head(lh)
    #Seleccionar las columnas a mostrar
    columns_to_show = ['ID Temporada', 'Jornada', 'Fecha', 'Partido', 'Diferencia','Enlace']
    st.write("Récords en diferencia de puntos")
    st.dataframe(max10_diff[columns_to_show], hide_index=True)

    # Puntos en una parte, máximo en P1VBC o P2VBC
    max10_p1 = df_games_CopaRey.sort_values(by='P1VBC',ascending=False).head(lh)
    max10_p2 = df_games_CopaRey.sort_values(by='P2VBC',ascending=False).head(lh)
    # Seleccionar las 10 mejores de ambas e indicar si es la primera o la segunda parte
    max10_p1['Parte'] = "Primera"
    max10_p2['Parte'] = "Segunda"
    max10_parts = pd.concat([max10_p1, max10_p2])
    # Ordenar por puntos en una parte
    max10_parts['Puntos'] = max10_parts[['P1VBC', 'P2VBC']].max(axis=1)
    max10_parts = max10_parts.sort_values(by='Puntos',ascending=False).head(lh)
    # Cambiar el nombre de las columnas
    max10_parts = max10_parts.rename(columns={'P1VBC': 'Primera', 'P2VBC': 'Segunda'})
       
    # Seleccionar las columnas a mostrar
    columns_to_show = ['ID Temporada', 'Jornada', 'Fecha', 'Partido', 'Puntos', 'Parte', 'Enlace']
    st.write("Récords de puntos en una parte")
    st.dataframe(max10_parts[columns_to_show], hide_index=True)
    
    # Puntos en un cuarto, máximo en Q1VBC, Q2VBC, Q3VBC o Q4VBC
    # Seleccionar los 10 partidos con más puntos en un cuarto
    max10_q1 = df_games_CopaRey.sort_values(by='Q1VBC',ascending=False).head(lh)
    max10_q2 = df_games_CopaRey.sort_values(by='Q2VBC',ascending=False).head(lh)
    max10_q3 = df_games_CopaRey.sort_values(by='Q3VBC',ascending=False).head(lh)
    max10_q4 = df_games_CopaRey.sort_values(by='Q4VBC',ascending=False).head(lh)
    # Seleccionar las 10 mejores de cada cuarto
    max10_q1['Cuarto'] = "Q1"
    max10_q2['Cuarto'] = "Q2"
    max10_q3['Cuarto'] = "Q3"
    max10_q4['Cuarto'] = "Q4"
    max10_quarters = pd.concat([max10_q1, max10_q2, max10_q3, max10_q4])
    # Ordenar por puntos en un cuarto
    max10_quarters['Puntos'] = max10_quarters[['Q1VBC', 'Q2VBC', 'Q3VBC', 'Q4VBC']].max(axis=1)
    max10_quarters = max10_quarters.sort_values(by='Puntos',ascending=False).head(lh)
    # Cambiar el nombre de las columnas
    max10_quarters = max10_quarters.rename(columns={'Q1VBC': 'Q1', 'Q2VBC': 'Q2', 'Q3VBC': 'Q3', 'Q4VBC': 'Q4'})
    # Seleccionar las columnas a mostrar
    columns_to_show = ['ID Temporada', 'Jornada', 'Fecha', 'Partido', 'Puntos', 'Cuarto', 'Enlace']
    st.write("Récords de puntos en un cuarto")
    st.dataframe(max10_quarters[columns_to_show], hide_index=True)
        
    # Rebotes
    max10_rebounds = df_games_CopaRey.sort_values(by='Rebotes VBC',ascending=False).head(lh)
    #Seleccionar las columnas a mostrar
    columns_to_show = ['ID Temporada', 'Jornada', 'Fecha', 'Partido', 'Rebotes VBC', 'Rebotes Rival', 'Enlace']
    st.write("Récords en rebotes")
    st.dataframe(max10_rebounds[columns_to_show], hide_index=True)
    
    # Asistencias 
    max10_assists = df_games_CopaRey.sort_values(by='Asistencias VBC',ascending=False).head(lh)
    #Seleccionar las columnas a mostrar
    columns_to_show = ['ID Temporada', 'Jornada', 'Fecha', 'Partido', 'Asistencias VBC', 'Asistencias Rival', 'Enlace']
    st.write("Récords en asistencias")
    st.dataframe(max10_assists[columns_to_show], hide_index=True)

    # Robos
    max10_steals = df_games_CopaRey.sort_values(by='Robos VBC',ascending=False).head(lh)
    #Seleccionar las columnas a mostrar
    columns_to_show = ['ID Temporada', 'Jornada', 'Fecha', 'Partido', 'Robos VBC', 'Robos Rival', 'Enlace']
    st.write("Récords en robos")
    st.dataframe(max10_steals[columns_to_show], hide_index=True)

    # Tapones
    max10_blocks = df_games_CopaRey.sort_values(by='Tapones VBC',ascending=False).head(lh)
    #Seleccionar las columnas a mostrar
    columns_to_show = ['ID Temporada', 'Jornada', 'Fecha', 'Partido', 'Tapones VBC', 'Tapones Rival', 'Enlace']
    st.write("Récords en tapones")
    st.dataframe(max10_blocks[columns_to_show], hide_index=True)

    # Valoración
    max10_val = df_games_CopaRey.sort_values(by='Val VBC',ascending=False).head(lh)
    #Seleccionar las columnas a mostrar
    columns_to_show = ['ID Temporada', 'Jornada', 'Fecha', 'Partido', 'Val VBC', 'Val Rival', 'Enlace']
    st.write("Récords en valoración")
    st.dataframe(max10_val[columns_to_show], hide_index=True)

    # Tiros de 1,2 y 3 puntos anotados
    # Tiros de 1 punto
    max10_t1a = df_games_CopaRey.sort_values(by='T1a VBC',ascending=False).head(lh)
    # Multiplicar por 100 para mostrar el porcentaje
    max10_t1a['T1% VBC'] = max10_t1a['T1% VBC']
    #Seleccionar las columnas a mostrar
    columns_to_show = ['ID Temporada', 'Jornada', 'Fecha', 'Partido', 'T1a VBC', 'T1% VBC', 'Enlace']
    st.write("Récords en tiros libres")
    st.dataframe(max10_t1a[columns_to_show], hide_index=True)

    # Tiros de 2 puntos
    max10_t2a = df_games_CopaRey.sort_values(by='T2a VBC',ascending=False).head(lh)
    # Multiplicar por 100 para mostrar el porcentaje
    max10_t2a['T2% VBC'] = max10_t2a['T2% VBC']
    #Seleccionar las columnas a mostrar
    columns_to_show = ['ID Temporada', 'Jornada', 'Fecha', 'Partido', 'T2a VBC', 'T2% VBC', 'Enlace']
    st.write("Récords en tiros de 2 puntos")
    st.dataframe(max10_t2a[columns_to_show], hide_index=True)

    # Tiros de 3 puntos
    max10_t3a = df_games_CopaRey.sort_values(by='T3a VBC',ascending=False).head(lh)
    # Multiplicar por 100 para mostrar el porcentaje
    max10_t3a['T3% VBC'] = max10_t3a['T3% VBC']
    #Seleccionar las columnas a mostrar
    columns_to_show = ['ID Temporada', 'Jornada', 'Fecha', 'Partido', 'T3a VBC', 'T3% VBC', 'Enlace']
    st.write("Récords en tiros de 3 puntos")
    st.dataframe(max10_t3a[columns_to_show], hide_index=True)

    # Porcentaje de acierto
    # Tiros de 1 punto
    max10_t1p = df_games_CopaRey.sort_values(by=['T1% VBC','T1a VBC'],ascending=False).head(lh)
    # Multiplicar por 100 para mostrar el porcentaje
    max10_t1p['T1% VBC'] = max10_t1p['T1% VBC']
    #Seleccionar las columnas a mostrar
    columns_to_show = ['ID Temporada', 'Jornada', 'Fecha', 'Partido', 'T1% VBC', 'T1a VBC', 'Enlace']
    st.write("Récords en porcentaje de tiros libres")
    st.dataframe(max10_t1p[columns_to_show], hide_index=True)

    # Tiros de 2 puntos
    max10_t2p = df_games_CopaRey.sort_values(by=['T2% VBC','T2a VBC'],ascending=False).head(lh)
    # Multiplicar por 100 para mostrar el porcentaje
    max10_t2p['T2% VBC'] = max10_t2p['T2% VBC']
    #Seleccionar las columnas a mostrar
    columns_to_show = ['ID Temporada', 'Jornada', 'Fecha', 'Partido', 'T2% VBC', 'T2a VBC', 'Enlace']
    st.write("Récords en porcentaje de tiros de 2 puntos")
    st.dataframe(max10_t2p[columns_to_show], hide_index=True)

    # Tiros de 3 puntos
    max10_t3p = df_games_CopaRey.sort_values(by=['T3% VBC','T3a VBC'],ascending=False).head(lh)
    # Multiplicar por 100 para mostrar el porcentaje
    max10_t3p['T3% VBC'] = max10_t3p['T3% VBC']
    #Seleccionar las columnas a mostrar
    columns_to_show = ['ID Temporada', 'Jornada', 'Fecha', 'Partido', 'T3% VBC', 'T3a VBC', 'Enlace']
    st.write("Récords en porcentaje de tiros de 3 puntos")
    st.dataframe(max10_t3p[columns_to_show], hide_index=True)

elif marco == "Estadísticas jugadores de una temporada":
    
    #Seleccionar una temporada, ordenar las temporadas de mayor a menor
    season = st.selectbox("Selecciona una temporada", df_games_CopaRey['ID Temporada'].sort_values(ascending=False).unique(), index=0)
    
    # Crear un marco para mostrar las estadísticas de los jugadores de la temporada actual
    st.subheader("Estadísticas jugadores de la temporada "+str(season))
    
    # Añadir radio button para seleccionar total o por partido
    col1, col2 = st.columns([1, 2])
    with col1:
        tipo_estadistica = st.radio("Tipo de estadística", ["Total", "Por Partido"], horizontal=True)
    
    # Añadir filtros
    st.write("Filtros")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Radio button para filtrar por victorias/derrotas
        resultado_filtro = st.radio("Resultado", ["Todos", "Victorias", "Derrotas"], horizontal=True)
    
    # Obtener el rango de jornadas de la temporada
    jornadas_temporada = df_games_CopaRey[df_games_CopaRey['ID Temporada'] == season]['Jornada'].unique()
    min_jornada = min(jornadas_temporada)
    max_jornada = max(jornadas_temporada)
    
    with col2:
        # Spinner para seleccionar jornada inicial
        jornada_inicio = st.number_input("Jornada inicial", min_value=min_jornada, max_value=max_jornada, value=min_jornada)
    
    with col3:
        # Spinner para seleccionar jornada final, debe ser mayor o igual que jornada_inicio
        jornada_fin = st.number_input("Jornada final", min_value=jornada_inicio, max_value=max_jornada, value=max_jornada)
    
    # Filtrar los datos de los jugadores para la temporada actual
    season_players = df_players_CopaRey[df_players_CopaRey['ID Temporada'] == season]
    
    # Filtrar por jornadas
    season_players = season_players[(season_players['Jornada'] >= jornada_inicio) & 
                                    (season_players['Jornada'] <= jornada_fin)]
    
    # Filtrar por resultado (victorias/derrotas)
    if resultado_filtro != "Todos":
        # Obtener los IDs de partidos que son victorias o derrotas
        victoria_valor = 1 if resultado_filtro == "Victorias" else 0
        partidos_filtrados = df_games_CopaRey[(df_games_CopaRey['ID Temporada'] == season) & 
                                          (df_games_CopaRey['VBC Victoria'] == victoria_valor)]['ID Partido'].unique()
        
        # Filtrar los datos de jugadores por estos partidos
        season_players = season_players[season_players['ID Partido'].isin(partidos_filtrados)]
    
    # Si no quedan partidos después del filtrado, mostrar mensaje y salir
    if len(season_players) == 0:
        st.warning("No hay datos disponibles para los filtros seleccionados.")
    else:
        # Crear un dataframe para almacenar las estadísticas de todos los jugadores
        todos_jugadores_stats = []
        
        # Contar partidos por jugador y puntos totales para ordenar
        partidos_por_jugador = season_players.groupby('ID Jugador')['ID Partido'].nunique()
        puntos_por_jugador = season_players.groupby('ID Jugador')['Puntos'].sum()

        # Crear un dataframe combinado para ordenamiento
        jugadores_stats = pd.DataFrame({
            'Partidos': partidos_por_jugador,
            'Puntos': puntos_por_jugador
        })

        # Ordenar primero por partidos (descendente) y luego por puntos (descendente)
        jugadores_stats = jugadores_stats.sort_values(by=['Partidos', 'Puntos'], ascending=[False, False])
        
        # Obtener la lista de jugadores ya ordenada
        jugadores = jugadores_stats.index.tolist()
        
        # Procesar cada jugador
        for jugador_id in jugadores:
            # Filtrar los datos del jugador
            jugador_stats = season_players[season_players['ID Jugador'] == jugador_id]
            
            # Si no hay estadísticas para este jugador (después del filtrado), continuar con el siguiente
            if len(jugador_stats) == 0:
                continue
                
            # Obtener el nombre del jugador usando el ID
            nombre_jugador = df_players_CopaRey[df_players_CopaRey['ID Jugador'] == jugador_id]['Nombre'].unique()[0]
            
            # Calcular acumulados y medias por partido
            partidos_jugados = jugador_stats['ID Partido'].nunique()
            
            # Calcular % de victorias de los partidos filtrados
            id_partidos_jugados = jugador_stats['ID Partido'].unique()
            victorias = len(df_games_CopaRey[df_games_CopaRey['ID Partido'].isin(id_partidos_jugados) & 
                                         (df_games_CopaRey['VBC Victoria'] == 1)])
            porcentaje_victorias = round(victorias * 100 / partidos_jugados, 1) if partidos_jugados > 0 else 0.0
            
            # Calcular porcentajes de tiro
            t1_porcentaje = round(jugador_stats['T1a'].sum() / jugador_stats['T1i'].sum() * 100, 1) if jugador_stats['T1i'].sum() > 0 else 0.0
            t2_porcentaje = round(jugador_stats['T2a'].sum() / jugador_stats['T2i'].sum() * 100, 1) if jugador_stats['T2i'].sum() > 0 else 0.0
            t3_porcentaje = round(jugador_stats['T3a'].sum() / jugador_stats['T3i'].sum() * 100, 1) if jugador_stats['T3i'].sum() > 0 else 0.0
            
            # Crear diccionario con las estadísticas del jugador
            jugador_row = {
                'Nombre': nombre_jugador,
                'Partidos': partidos_jugados,
                '% Victorias': porcentaje_victorias
            }
            
            # Añadir estadísticas totales o por partido según la selección
            if tipo_estadistica == "Total":
                jugador_row.update({
                    'Puntos': jugador_stats['Puntos'].sum(),
                    'Rebotes': jugador_stats['Rebotes'].sum(),
                    'Asistencias': jugador_stats['Asistencias'].sum(),
                    'Robos': jugador_stats['Robos'].sum(),
                    'Tapones': jugador_stats['Tapones'].sum(),
                    'Valoración': jugador_stats['Val'].sum(),
                    'T. Libres': jugador_stats['T1a'].sum(),
                    'T1%': t1_porcentaje,
                    'T2 puntos': jugador_stats['T2a'].sum(),
                    'T2%': t2_porcentaje,
                    'T3 puntos': jugador_stats['T3a'].sum(),
                    'T3%': t3_porcentaje
                })
            else:  # "Por Partido"
                jugador_row.update({
                    'Puntos': round(jugador_stats['Puntos'].sum() / partidos_jugados, 1),
                    'Rebotes': round(jugador_stats['Rebotes'].sum() / partidos_jugados, 1),
                    'Asistencias': round(jugador_stats['Asistencias'].sum() / partidos_jugados, 1),
                    'Robos': round(jugador_stats['Robos'].sum() / partidos_jugados, 1),
                    'Tapones': round(jugador_stats['Tapones'].sum() / partidos_jugados, 1),
                    'Valoración': round(jugador_stats['Val'].sum() / partidos_jugados, 1),
                    'T. Libres': round(jugador_stats['T1a'].sum() / partidos_jugados, 1),
                    'T1%': t1_porcentaje,
                    'T2 puntos': round(jugador_stats['T2a'].sum() / partidos_jugados, 1),
                    'T2%': t2_porcentaje,
                    'T3 puntos': round(jugador_stats['T3a'].sum() / partidos_jugados, 1),
                    'T3%': t3_porcentaje
                })
            
            todos_jugadores_stats.append(jugador_row)
        
        # Si después de procesar a todos los jugadores no hay estadísticas, mostrar mensaje
        if len(todos_jugadores_stats) == 0:
            st.warning("No hay datos disponibles para los filtros seleccionados.")
        else:
            # Crear dataframe con las estadísticas de todos los jugadores
            df_todos_jugadores = pd.DataFrame(todos_jugadores_stats)
            
            # Mostrar información sobre los filtros aplicados
            filtros_aplicados = []
            if resultado_filtro != "Todos":
                filtros_aplicados.append(f"Resultado: {resultado_filtro}")
            if jornada_inicio > min_jornada or jornada_fin < max_jornada:
                filtros_aplicados.append(f"Jornadas: {jornada_inicio} a {jornada_fin}")
            
            if filtros_aplicados:
                st.write(f"**Filtros aplicados:** {', '.join(filtros_aplicados)}")
            
            # Mostrar la tabla con todas las estadísticas directamente (sin dividir en columnas)
            st.dataframe(
                df_todos_jugadores,
                hide_index=True,
                column_config={
                    "Nombre": st.column_config.TextColumn(width="medium"),
                    "Partidos": st.column_config.NumberColumn(width="small"),
                    "% Victorias": st.column_config.NumberColumn(format="%.1f%%", width="small"),
                    "Puntos": st.column_config.NumberColumn(width="small"),
                    "Rebotes": st.column_config.NumberColumn(width="small"),
                    "Asistencias": st.column_config.NumberColumn(width="small"),
                    "Robos": st.column_config.NumberColumn(width="small"),
                    "Tapones": st.column_config.NumberColumn(width="small"),
                    "Valoración": st.column_config.NumberColumn(width="small"),
                    "T. Libres": st.column_config.NumberColumn(width="small"),
                    "T1%": st.column_config.NumberColumn(format="%.1f%%", width="small"),
                    "T2 puntos": st.column_config.NumberColumn(width="small"),
                    "T2%": st.column_config.NumberColumn(format="%.1f%%", width="small"),
                    "T3 puntos": st.column_config.NumberColumn(width="small"),
                    "T3%": st.column_config.NumberColumn(format="%.1f%%", width="small")
                }
            )
elif marco == "Estadísticas contra un rival":
    
    st.subheader("Estadísticas contra un rival")
    # Filtra los equipos
    # Selecciona los equipos únicos de la columna 'ID Rival' del DataFrame df_games_CopaRey
    # Lee dataframe de equipos de Copa del Rey primera columna IDs del equipo, segunda columna nombre del equipo

    equipos = df_games_CopaRey['Equipo Rival'].unique()
    # Crea un selectbox para seleccionar el rival
    rival = st.selectbox("Selecciona un rival", equipos, index=0)     # Esto asume que 'Equipo Rival' es el nombre del equipo y 'ID Rival' es su identificador único   
    # Filtra los partidos contra el rival seleccionado, utiliza el id del equipo
    id_rival = df_games_CopaRey[df_games_CopaRey['Equipo Rival'] == rival]['ID Rival'].unique()[0]

    # Selecciona todos los partidos contra el rival    
    partidos_rival = df_games_CopaRey[df_games_CopaRey['ID Rival']==id_rival]
    
    
    # Combinar las estadísticas de local y visitante
    stats_total = pd.DataFrame({
        'Partidos': [len(partidos_rival)],
        'Victorias': [len(partidos_rival[partidos_rival['VBC Victoria'] == 1])],
        'Derrotas': [len(partidos_rival[partidos_rival['VBC Victoria'] == 0])],
        'Puntos': [round(partidos_rival['Puntos VBC'].mean(), 1)],
        'Rebotes': [round(partidos_rival['Rebotes VBC'].mean(), 1)],
        'Asistencias': [round(partidos_rival['Asistencias VBC'].mean(), 1)],
        'Robos': [round(partidos_rival['Robos VBC'].mean(), 1)],
        'Tapones': [round(partidos_rival['Tapones VBC'].mean(), 1)],
        'Valoración': [round(partidos_rival['Val VBC'].mean(), 1)],
        'Puntos Rival': [round(partidos_rival['Puntos Rival'].mean(), 1)],
        'Rebotes Rival': [round(partidos_rival['Rebotes Rival'].mean(), 1)],
        'Asistencias Rival': [round(partidos_rival['Asistencias Rival'].mean(), 1)],
        'Robos Rival': [round(partidos_rival['Robos Rival'].mean(), 1)],
        'Tapones Rival': [round(partidos_rival['Tapones Rival'].mean(), 1)],
        'Valoración Rival': [round(partidos_rival['Val Rival'].mean(), 1)],
    })
    
    # Transponer las estadísticas totales
    stats_total = stats_total.T
    
    # Renombrar las columnas de las tablas transpuestas
    stats_total.columns = ['Total']
    
    st.write("Estadísticas")
    st.dataframe(stats_total, height=565, column_config={
            stats_total.index.name: st.column_config.TextColumn(width="medium"),
            "Total": st.column_config.TextColumn(width=50)})

elif marco == "Entrenadores":
    # Crear un marco para mostrar los entrenadores
    st.subheader("Entrenadores")
    # Buscar todos los entrenadores de VBC por ID Entrenador VBC (el nombre es la columna Entrenador VBC)
    # Calcula los que más partidos han dirigido, más victorias y más derrotas (local, visitante y total)
    entrenadores = df_games_CopaRey.groupby(['ID Entrenador VBC', 'Entrenador VBC']).agg(
        Partidos=('ID Partido', 'count'),
        Victorias=('VBC Victoria', lambda x: (x == 1).sum()),
        Derrotas=('VBC Victoria', lambda x: (x == 0).sum())
    ).reset_index()
    # Añadir porcentaje de victorias
    entrenadores['%'] = round((entrenadores['Victorias'] / entrenadores['Partidos']) * 100, 1)
    # Ordenar por número de partidos
    entrenadores = entrenadores.sort_values(by='Partidos', ascending=False)
    # Cambiar el nombre de las columnas y eliminar la columna ID Entrenador VBC
    entrenadores = entrenadores.rename(columns={'Entrenador VBC': 'Entrenador'})
    # Eliminar la columna ID Entrenador VBC para la visualización
    entrenadores_display = entrenadores.drop(columns=['ID Entrenador VBC'])
    
    # Filtrar los partidos como local 
    entrenadores_local = df_games_CopaRey[df_games_CopaRey['VBC Local'] == 1].groupby(['ID Entrenador VBC', 'Entrenador VBC']).agg(
        Partidos=('ID Partido', 'count'),
        Victorias=('VBC Victoria', lambda x: (x == 1).sum()),
        Derrotas=('VBC Victoria', lambda x: (x == 0).sum())
    ).reset_index()
    # Añadir porcentaje de victorias
    entrenadores_local['Porcentaje'] = round((entrenadores_local['Victorias'] / entrenadores_local['Partidos']) * 100, 1)
    # Ordenar por número de partidos
    entrenadores_local = entrenadores_local.sort_values(by='Partidos', ascending=False)
    # Cambiar el nombre de las columnas
    entrenadores_local = entrenadores_local.rename(columns={'Entrenador VBC': 'Entrenador'})
    # Eliminar la columna ID Entrenador VBC para la visualización
    entrenadores_local_display = entrenadores_local.drop(columns=['ID Entrenador VBC'])
    
    # Filtrar los partidos como visitante
    entrenadores_visitante = df_games_CopaRey[df_games_CopaRey['VBC Local'] == 0].groupby(['ID Entrenador VBC', 'Entrenador VBC']).agg(
        Partidos=('ID Partido', 'count'),
        Victorias=('VBC Victoria', lambda x: (x == 1).sum()),
        Derrotas=('VBC Victoria', lambda x: (x == 0).sum())
    ).reset_index()
    # Añadir porcentaje de victorias
    entrenadores_visitante['Porcentaje'] = round((entrenadores_visitante['Victorias'] / entrenadores_visitante['Partidos']) * 100, 1)
    # Ordenar por número de partidos
    entrenadores_visitante = entrenadores_visitante.sort_values(by='Partidos', ascending=False)
    # Cambiar el nombre de las columnas
    entrenadores_visitante = entrenadores_visitante.rename(columns={'Entrenador VBC': 'Entrenador'})
    # Eliminar la columna ID Entrenador VBC para la visualización
    entrenadores_visitante_display = entrenadores_visitante.drop(columns=['ID Entrenador VBC'])
    
    # Crear 3 columnas para mostrar los resultados
    col1, col2, col3 = st.columns(3)
    
    # Mostrar los resultados en las columnas
    with col1:
        st.write("Entrenadores (Total)")
        st.dataframe(entrenadores_display, hide_index=True, column_config={
            'Entrenador': st.column_config.TextColumn(width="medium"),
            'Partidos': st.column_config.NumberColumn(width="small"),
            'Victorias': st.column_config.NumberColumn(width="small"),
            'Derrotas': st.column_config.NumberColumn(width="small"),
            '%': st.column_config.NumberColumn(width="small", format="%.1f%% ")
        })
    
    with col2:
        st.write("Entrenadores como local")
        st.dataframe(entrenadores_local_display, hide_index=True, column_config={
            'Entrenador': st.column_config.TextColumn(width="medium"),
            'Partidos': st.column_config.NumberColumn(width="small"),
            'Victorias': st.column_config.NumberColumn(width="small"),
            'Derrotas': st.column_config.NumberColumn(width="small"),
            'Porcentaje': st.column_config.NumberColumn(width="small", format="%.1f%%")
        })
    
    with col3:
        st.write("Entrenadores como visitante")
        st.dataframe(entrenadores_visitante_display, hide_index=True, column_config={
            'Entrenador': st.column_config.TextColumn(width="medium"),
            'Partidos': st.column_config.NumberColumn(width="small"),
            'Victorias': st.column_config.NumberColumn(width="small"),
            'Derrotas': st.column_config.NumberColumn(width="small"),
            'Porcentaje': st.column_config.NumberColumn(width="small", format="%.1f%%")
        })