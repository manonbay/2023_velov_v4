
#1. imports 
import time 
import json
import requests
import pickle
import pandas as pd
import matplotlib.pyplot as plt 
from calendar import monthrange
from datetime import datetime


# #2. flows & tasks
# - chargement des données (requete api)
# - transformation des données
# - enregistrement des données (.pkl) / .parquet


def save_data_pkl(df) -> None : 
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    nom_fichier = f'dump{year}_{month}_15min'
    with open(nom_fichier + ".pkl", 'wb') as f: # nom du fichier à créer
        pickle.dump(df, f)

def clean_df(df) -> pd.DataFrame: 
    df=df[["horodate",
                "number", 
                "status",
                'total_stands.availabilities.bikes', 
                'total_stands.availabilities.electricalBikes',
                'total_stands.availabilities.stands',
                'total_stands.capacity']] 
    df.rename(columns={'total_stands.availabilities.bikes' : 'availabilities.all.types',
            'total_stands.availabilities.electricalBikes' : 'availabilities.electricalBikes',
            'total_stands.availabilities.stands' : "availabilities.stands", 
            'total_stands.capacity' :"capacity"}, inplace=True)
    return df

def load_monthly_data_from_API(year, month) -> pd.DataFrame:
    link_part1 = "https://download.data.grandlyon.com/ws/timeseries/jcd_jcdecaux.historiquevelov/all.json?horodate__gte="
    link_part2 = "&maxfeatures=600000"
    last_day_of_month = monthrange(year,month)[1]
    for day in range (1, monthrange(year,month)[1]) :
        if day != monthrange(year,month)[1] : 
            URL = f'{link_part1}{year}-{month}-{day}-&horodate__lte={year}-{month}-{day+1}{link_part2}'
        else :
            URL = f'{link_part1}{year}-{month}-{day}-&horodate__lte={year}-{(month+1)}-1{link_part2}'
        
        persistent_connexion = requests.Session()   
        response = persistent_connexion.get(URL)
        
        try : 
            response.raise_for_status() # à tester, retourne une erreur si response !=200
            data_endpoint = json.loads(response.text)
            historique_journalier = pd.json_normalize(data_endpoint, record_path="values")
            historique_journalier = clean_df(historique_journalier)
        
            if day==1 : #initialisation du df
                historique = historique_journalier
            else : 
                historique = pd.concat([historique,historique_journalier])
            del(historique_journalier)
        except KeyError as e : 
            print(f'{year}-{month}-{day} : KeyError', e)
        except json.decoder.JSONDecodeError as e :    
            print(f'{year}-{month}-{day} :JSONDecodeError', e)
    
    return historique    
        
if __name__ == '__main__':
    year=2023
    month=6
    dataframe_month = load_monthly_data_from_API(year=year, month=month)
    save_data_pkl(dataframe_month)
