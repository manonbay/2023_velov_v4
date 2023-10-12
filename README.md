# 2023_velov_v4

API utilisée : https://www.data.gouv.fr/fr/datasets/historique-des-disponibilites-des-stations-velov-de-la-metropole-de-lyon
Requirement.txt : Contient les versions des librairies utilisées

1_requeteAPI.ipynb : création de la requête de l'API ainsi que la génération d'un fichier pickle mensuel (anciennement .csv)
2_maps_creation.ipynb : création des cartes dynamiques à partir d'un fichier csv journalier et d'un csv de geolocalisation (import .csv en .pickle à modifier)
3_stats.ipynb : statistiques simples

velov_app_v4.py :  fichier source pour l'application streamlit : <https://2023velov.streamlit.app/>

