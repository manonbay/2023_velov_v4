# coding: utf-8
import pandas as pd
import leafmap.foliumap as leafmap
from folium.plugins import TimestampedGeoJson
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu #https://www.youtube.com/watch?v=hEPoto5xp3k
pd.options.mode.chained_assignment = None

st.set_page_config(page_title="Portfolio_Manon_Le_Roux", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

url1='https://drive.google.com/file/d/1XpTdAZzxhpcXGQdiYn9zrNDAY7UIAN4y/view?usp=share_link'
url1='https://drive.google.com/uc?id=' + url1.split('/')[-2]
fevrier = pd.read_csv(url1)

url2='https://drive.google.com/file/d/1orC1m2x-xlf9OFbs_-yTARWkJ1c7kapx/view?usp=share_link'
url2='https://drive.google.com/uc?id=' + url2.split('/')[-2]
bornes_velov = pd.read_csv(url2)

# fevrier = pd.read_csv(r"C:\Users\manon\Dev\Projet3_velov\2023-02-allege15min.csv", index_col=0)
# bornes_velov = pd.read_csv(r"C:\Users\manon\Dev\Projet3_velov\bornes_velov_clean.csv")

fevrier.reset_index(inplace=True)

## df 1er fevrier 2023
premierfevrier = fevrier[fevrier["horodate"] < "2023-02-02"]
premierfevrier = premierfevrier.merge(bornes_velov, how="left", on="number")
premierfevrier["horodate"]= pd.to_datetime(fevrier["horodate"])


palette_bleu_rouge_noir = ["#26C6DA", "#F8BBD0", "#F48FB1", "#F06292","#EC407A", "#E91E63", "#D81B60", "#C2185B", "#AD1457", "#880E4F", "#000000"]
# indice 0=bleu, indice 10=noir, 1:9=degradé rouge

premierfevrier["couleurpardefaut"] = "0"
for i in range(len(premierfevrier)) :
    if premierfevrier["availabilities.all.types"].iloc[i] == 0  :
        premierfevrier["couleurpardefaut"].iloc[i] =  palette_bleu_rouge_noir[0] # bleu
    elif premierfevrier["availabilities.all.types"].iloc[i] <= premierfevrier["capacity"].iloc[i]/10*2 :
        premierfevrier["couleurpardefaut"].iloc[i] =  palette_bleu_rouge_noir[1]
    elif premierfevrier["availabilities.all.types"].iloc[i] <= premierfevrier["capacity"].iloc[i]/10*3 :
        premierfevrier["couleurpardefaut"].iloc[i] =  palette_bleu_rouge_noir[2]
    elif premierfevrier["availabilities.all.types"].iloc[i] <= premierfevrier["capacity"].iloc[i]/10*4 :
        premierfevrier["couleurpardefaut"].iloc[i] =  palette_bleu_rouge_noir[3]
    elif premierfevrier["availabilities.all.types"].iloc[i] <= premierfevrier["capacity"].iloc[i]/10*5 :
        premierfevrier["couleurpardefaut"].iloc[i] =  palette_bleu_rouge_noir[4]
    elif premierfevrier["availabilities.all.types"].iloc[i] <= premierfevrier["capacity"].iloc[i]/10*6 :
        premierfevrier["couleurpardefaut"].iloc[i] =  palette_bleu_rouge_noir[5]
    elif premierfevrier["availabilities.all.types"].iloc[i] <= premierfevrier["capacity"].iloc[i]/10*7 :
        premierfevrier["couleurpardefaut"].iloc[i] =  palette_bleu_rouge_noir[6]
    elif premierfevrier["availabilities.all.types"].iloc[i] <= premierfevrier["capacity"].iloc[i]/10*8 :
        premierfevrier["couleurpardefaut"].iloc[i] =  palette_bleu_rouge_noir[7]
    elif premierfevrier["availabilities.all.types"].iloc[i] <= premierfevrier["capacity"].iloc[i]/10*9 :
        premierfevrier["couleurpardefaut"].iloc[i] =  palette_bleu_rouge_noir[8]
    elif premierfevrier["availabilities.all.types"].iloc[i] == premierfevrier["capacity"].iloc[i] :
        premierfevrier["couleurpardefaut"].iloc[i] =  palette_bleu_rouge_noir[10] #noir
    else :
        premierfevrier["couleurpardefaut"].iloc[i] =  palette_bleu_rouge_noir[9] #rouge foncé

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
                    'fillColor': df['couleurpardefaut'].iloc[i],
                    'fillOpacity': 0.5,
                    'stroke': 'true',
                    'radius': df['availabilities.all.types'].iloc[i]
                }
            }
        }
        features.append(feature)
    return features
df_geojson = create_geojson_features(premierfevrier)

map_velov_2 = leafmap.Map(location=[45.758, 4.853],
                        zoom_start=12.5,
                        tiles ='CartoDB Positron',
                        draw_control=False,
                        measure_control=False)

TimestampedGeoJson(df_geojson,
                  period = 'PT15M',
                  transition_time=300,
                  duration = 'PT15M',
                  auto_play = True).add_to(map_velov_2)

map_velov_2.add_colorbar(colors = palette_bleu_rouge_noir,
                       vmax=100,
                       caption="Pourcentage de remplissage de la station")
map_velov_2.add_basemap("Stamen.Toner", show=False)
map_velov_2.add_basemap("OpenStreetMap", show=False)

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
                    title="Répartition des stations velov lyonnaises selon leur capacité maximale", 
                    x="capacity", text_auto=True, 
                    barmode="group", 
                    color_discrete_sequence=['#DE3163'], 
                    nbins=12, 
                    labels={"capacity" : "capacite maximale"})
fig3.update_layout(bargap=0.1)
fig3.update_yaxes(title_text="nombre de stations")

# Streamlit : 

# noms des onglets : 
page1, page2, page3 = "1. Apprentissage des outils", "2. Ajout de statistiques plus complètes", "3. Utilisation SQLserver et AWS"    
with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Accueil", page1, page2, page3],
        styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#44c7c0"}, 
    }
        )


if selected == "Accueil" :
    st.title('Disponibilités des vélos en libre service de la ville de Lyon')
    st.markdown("Projet port-folio réalisé en mai 2023")
    st.markdown("")
    st.markdown("**Description des différentes pages et outils utilisés :**")
    col1, col2, col3 = st.columns(3)
    with col1 : 
        st.markdown("**1. Apprentissage des outils**")
        st.markdown("Graphiques sur 24h de données depuis un fichier .csv récupéré par API.")
        st.markdown("[Documentation de l'API utilisée](https://www.data.gouv.fr/fr/datasets/historique-des-disponibilites-des-stations-velov-de-la-metropole-de-lyon/#discussion-63ee8ecd7b600fcdee918dfb)")
    with col2 : 
        st.markdown("**2. Ajout de statistiques plus complètes**")
        st.markdown("Graphiques sur 3 mois avec différenciation des jours de semaine et de week-end, des vacances scolaires, de la météo")
    with col3 : 
        st.markdown("**3. Utilisation SQLserver et AWS**")
        st.markdown("Analyse sur un mois entier avec récupération des données dans une base de données SQL")
    col1, col2, col3 = st.columns(3) # réinitialisation de 3 colonnes afin que les textes soient tous à la même hauteur sur la page
    with col1 : 
        st.markdown("Outils : ")
        st.markdown("jupyter/vscode, streamlit, folium/leafmap, matplotlib/seaborn/plotly")
    with col2 : 
        st.markdown("Outils : ")
    with col3 : 
        st.markdown("Outils : ")
    st.markdown("")
    st.markdown("**Contexte :**")
    st.markdown("Il s'est avéré que l'API d'historique de la disponibilité des velovs des fournie par Le Grand Lyon ne contenait pas d'entrées pour tous les jours des mois observés (d'octobre 2022 à avril 2024). Pour cette raison j'ai décidé de ne traiter que les données disponibles et j'ai refusé de remplacer les données manquantes par des données de jours 'similaires' pour des raisons de pertinence et de représentativité des données")

    st.markdown("Il aurait peut-être été possible de récupérer une partie des données précedentes, de normaliser les données selon la flotte de vélos disponibles, des dates de vacances scolaires, du covid et des confinements,... mais c'est un travail de longue haleine qui ne correspondait pas à mon objectif de réaliser un simple portfolio")
    st.markdown("Manon Le Roux")
    st.markdown("06 50 59 59 21")
    st.markdown("https://www.linkedin.com/in/manon-le-roux-data/")
    st.markdown("https://github.com/wolbachia-fanclub")
    
if selected == page1 :
    st.header("* A. Matplotlib")
    # image= Image.open(r"C:\Users\manon\Dev\Projet3_velov\plt_seaborn_1fev.png")
    # st.image(image, caption="Remplissage de quelques stations selon les heures avec mise en évidence du remplissage des stations")
    # afficher en plt à la place ? https://www.youtube.com/watch?v=v0xnI-S7o7Qs
      
    st.header("* B. Plotly")
    st.metric("**Stations en fonctionnement en fevrier 2023**", premierfevrier["number"].nunique())     
    col1, col2= st.columns(2)
    col1.plotly_chart(fig2, use_container_width=True)
    col2.plotly_chart(fig3, use_container_width=True)

    st.header("* C. Folium/Leafmap")
    st.caption("Quantité de velos disponibles et taux de remplissage par station")
    map_velov_2.to_streamlit(scroling=True)
    # ajouter bouton vers le code sur github

# st.selectbox(#par tranches de 15min / 1h ?)

if selected == page2 : 
    st.markdown("Page en cours de construction")
#     st.header(f"Analyse {selected}")
#     # st.selectbox(#choisir semaine)
#     # st.selectbox(#par quels pas de temps ?)
    
if selected == page3 :

    st.markdown("Page en cours de construction")
#     st.header(f"Analyse {selected}")
#     st.header("Déplacements en velov sur le mois")
#     st.selectbox() # de nov 2022 à avril 2023
    
    
