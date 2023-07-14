# coding: utf-8
import pandas as pd
import leafmap.foliumap as leafmap
from folium.plugins import TimestampedGeoJson
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu #https://www.youtube.com/watch?v=hEPoto5xp3k

st.set_page_config(page_title="Portfolio_Manon_Le_Roux", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

url1="https://drive.google.com/file/d/1nEzC2VVAZynCOB6wsgXrloI8r1fMnYNG/view?usp=sharing"
url1='https://drive.google.com/uc?id=' + url1.split('/')[-2]
premierfevrier = pd.read_csv(url1)

    
# Déclaration des variables globales : 
accueil, page1, page2 = "Accueil", "1. Statistiques", "2. Maps dynamiques"
map1, map2, map3 = "Deplacements quantitatifs des velov", "Taux de remplissage des stations velov", "Quantité et taux de remplissage"
palette1, palette2 = ['#586065','#53c688','#53c688'], ["#26C6DA", "#F8BBD0", "#EC407A", "#AD1457", "#000000"]

with st.sidebar:
    st.title("Projet 2023 : Deplacements en velov")
    selected = option_menu(
        menu_title=None,
        options=[accueil, page1, page2],
        styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#44c7c0"}
        }
        )
    
    st.title("Contact :")
    st.caption(""" 
                    - GitHub : <https://github.com/manonbay/>
                    - Linkedin : <https://www.linkedin.com/in/manon-le-roux-data/> 
                    """)
    
if selected == accueil : 
    st.title('Déplacements des vélos en libre service de la ville de Lyon')
    st.markdown("Projet port-folio réalisé en 2023 sur 24h de données récupérées via l'API de la métropole de Lyon : [Documentation](https://www.data.gouv.fr/fr/datasets/historique-des-disponibilites-des-stations-velov-de-la-metropole-de-lyon/#discussion-63ee8ecd7b600fcdee918dfb)")
    st.markdown("**Stack technique :**")
    st.markdown("Jupyter/VScode, Python, Pandas, Streamlit, Folium , Leafmap, Plotly express")
    st.markdown("**Quelques lignes du fichier crée via les données de l'API pour réaliser ce projet :**")
    st.table(premierfevrier.iloc[23332:23345,:])
    
elif selected == page1 : 
    st.title("Statistiques sur les stations velov en service le 1er fevrier 2023")
    st.markdown("[Documentation de l'API utilisée](https://www.data.gouv.fr/fr/datasets/historique-des-disponibilites-des-stations-velov-de-la-metropole-de-lyon/#discussion-63ee8ecd7b600fcdee918dfb)")
    
    col1, col2 = st.columns(2)
    
    fig2 = px.line(premierfevrier[(premierfevrier["number"]== 10018) |
                            (premierfevrier["number"]== 10002)| 
                            (premierfevrier["number"]== 8004)],
            x="horodate",
            y="availabilities.all.types",
            color='number',
            color_discrete_sequence= ["grey", "pink", "green"], 
            labels={"horodate" : "heure", "availabilities.all.types" : "vélos disponibles", "number" : "n° de station"}, 
            title="Disponibilités des velovs dans quelques stations")

    capacite_stations = premierfevrier[["number", "capacity"]].drop_duplicates()
    fig3 = px.histogram(capacite_stations, 
                        title="Capacité maximale des stations velov", 
                        x="capacity", text_auto=True, 
                        barmode="group", 
                        color_discrete_sequence=['#DE3163'], 
                        nbins=12, 
                        labels={"capacity" : "capacite maximale"})
    fig3.update_layout(bargap=0.1)
    fig3.update_yaxes(title_text="nombre de stations")
    
    st.metric("**Stations en fonctionnement en fevrier 2023**", premierfevrier["number"].nunique())
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig2, use_container_width=True)
    col1.markdown("On observe une diminution du nombre de velov disponibles pour la station 10018 entre 7h et 10h,tandis que la station 10002 se remplie sur cet horaire. La station 8004 aura un remplissage relativement stable toute la journée")
    col2.plotly_chart(fig3, use_container_width=True)
    col2.markdown("187 stations velov ont une capacité maximale comprise entre 10 et 19 stationnements. Seule une station a une capacité comprise entre 110 et 119 places.")
    



if selected == page2 : 
    col1, col2 = st.columns([0.7,0.3])
    map_number = col1.selectbox("Quelle carte dynamique du 1er fevrier 2023 souhaitez-vous afficher ?", options =[map1, map2, map3])
    pas_de_temps = col2.radio("Par quel pas de temps souhaitez vous afficher la carte", ("Tranches de 15 minutes","Tranches de 30 minutes","Tranches d'une heure"), key="pas")
    if pas_de_temps=="Tranches de 15 minutes" :
        pas_choisi = "PT15M"
    elif pas_de_temps=="Tranches de 30 minutes" :
        pas_choisi = "PT30M"
    else : 
        pas_choisi = "PT1H"
        
    if map_number == map1 :
        
        def create_geojson_features(df):
            features = []
            
            for i in range(len(df)):
                feature = {
                    'type': 'Feature',
                    'geometry': {
                        'type':'Point', 
                        'coordinates': [df['longitude'].iloc[i], df['latitude'].iloc[i]]
                    },
                    'properties': {
                        'time': df["horodate"].iloc[i].__str__(),
                        'style': {'color' : ''},
                        'icon': 'circle',
                        'iconstyle':{
                            'fillColor': df['couleur_carte_quanti'].iloc[i],
                            'fillOpacity': 0.4,
                            'stroke': 'true',
                            'radius': df['availabilities.all.types'].iloc[i] # dependant de la quantité de velov en station
                        }
                    }
                }
                features.append(feature)
            return features
        

        df_geojson = create_geojson_features(premierfevrier)

        map_velov = leafmap.Map(location=[45.758, 4.853],
                                zoom_start=12.5,
                                tiles ='CartoDB Positron',
                                draw_control=False,
                                measure_control=False)
        
        TimestampedGeoJson(data=df_geojson,
                        period = pas_choisi,
                        duration = "PT15M",
                        auto_play = True).add_to(map_velov)

        map_velov.add_title("Deplacements quantitatifs des velov", font_size="20px", align="center")
        map_velov.add_basemap("Stamen.Toner", show=False)
        map_velov.add_basemap("OpenStreetMap", show=False)
        col1, col2 = st.columns([0.8,0.2])
        with col1: 
            map_velov.to_streamlit(scroling=True,height=500)
        with col2 : 
            col2.caption("")
            col2.caption("")
            col2.caption("")
            col2.caption("La taille du cercle est proportionnelle au nombre de velov présents")

    elif map_number == map2 : 

        def create_geojson_features(df):
            features = []
        
            for i in range(len(df)):
                feature = {
                    'type': 'Feature',
                    'geometry': {
                        'type':'Point', 
                        'coordinates': [df['longitude'].iloc[i], df['latitude'].iloc[i]]
                    },
                    'properties': {
                        'time': df["horodate"].iloc[i].__str__(),
                        'style': {'color' : ''},
                        'icon': 'circle',
                        'iconstyle':{
                            'fillColor': df["couleur_carte_taux"].iloc[i],
                            'fillOpacity': 0.4,
                            'stroke': 'true',
                            'radius': ((df['capacity'].iloc[i])/2) #je divise le radius par 2 sinon la map est illisible
                        }
                    }
                }
                features.append(feature)
            return features
        df_geojson = create_geojson_features(premierfevrier)

        map_velov = leafmap.Map(location=[45.758, 4.853],
                                zoom_start=12.5,
                                tiles ='CartoDB Positron',
                                draw_control=False,
                                measure_control=False)

        TimestampedGeoJson(df_geojson,
                        period = pas_choisi,
                        duration = "PT15M",
                        auto_play = True).add_to(map_velov)

        map_velov.add_title("Taux de remplissage des stations velov",
                            font_size="20px",
                            align="center")

        map_velov.add_colorbar(colors=palette2,
                            index=[0,0.05,0.5,0.95,1],
                            categorical=False,
                            caption="pourcentage de remplissage")

        map_velov.add_basemap("Stamen.Toner", show=False)
        map_velov.add_basemap("OpenStreetMap", show=False)

        col1, col2 = st.columns([0.8,0.2])
        with col1: 
            map_velov.to_streamlit(scroling=True,height=500)
        with col2 : 
            col2.caption("")
            col2.caption("")
            col2.caption("")
            col2.caption("La taille des cercles est fixe et dépend de la capacité maximale de chaque station, leur couleur est dépendante du taux de remplissage des stations")        

        
    elif map_number == map3 : 

        def create_geojson_features(df):
            features = []
            
            for i in range(len(df)):
                feature = {
                    'type': 'Feature',
                    'geometry': {
                        'type':'Point', 
                        'coordinates': [df['longitude'].iloc[i], df['latitude'].iloc[i]]
                    },
                    'properties': {
                        'time': df["horodate"].iloc[i].__str__(),
                        'style': {'color' : ''},
                        'icon': 'circle',
                        'iconstyle':{
                            'fillColor': df['couleur_carte_quanti_taux'].iloc[i],
                            'fillOpacity': 0.4,
                            'stroke': 'true',
                            'radius': df['availabilities.all.types'].iloc[i]
                        }
                    }
                }
                features.append(feature)
            return features
        df_geojson = create_geojson_features(premierfevrier)

        # Création de la map
        map_velov = leafmap.Map(location=[45.758, 4.853],
                                zoom_start=12.5,
                                tiles ='CartoDB Positron',
                                draw_control=False,
                                measure_control=False)
        TimestampedGeoJson(df_geojson,
                        period = pas_choisi,
                        duration = "PT15M",
                        auto_play = True).add_to(map_velov)

        # # Ajout du titre sur la map
        map_velov.add_title("Representation double",
                            font_size="20px",
                            align="center")

        map_velov.add_colorbar(colors=palette2,
                            index=[0,0.05,0.5,0.95,1],
                            categorical=False,
                            caption="pourcentage de remplissage")

        map_velov.add_basemap("Stamen.Toner", show=False)
        map_velov.add_basemap("OpenStreetMap", show=False)

        col1, col2 = st.columns([0.8,0.2])
        with col1: 
            map_velov.to_streamlit(scroling=True,height=500)
        with col2 : 
            col2.caption("")
            col2.caption("")
            col2.caption("")
            col2.caption("Cette map est la moins lisible mais nous pouvons y lire deux informations à la fois : la taille des cercles est relative au nombre de velov présents dans chaque station, leur couleur est relative au taux de remplissage des stations")  

