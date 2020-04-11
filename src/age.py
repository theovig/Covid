import numpy as np
import pandas as pd
import os
import os.path
from datetime import datetime,timedelta

EXPORTS_PATH = r"\\ars75filer05\N-COV19\16_Cellule données\DATAS\SIVIC\age"
LAST =None
BLAST=None

def explore():

    results=[(f, extract_path_date(f)) for f in os.listdir(EXPORTS_PATH) if f[-4:] == ".xls"]
    print(results)
    return results
print(explore())
def get_last():
    """
    Trouve le dernier export contenu dans le dossier data/exports_bruts
    :return: (path, date_export)
    """
    global LAST, BLAST
    if not(LAST is None):
        return LAST

    all = explore()
    last = all[0]
    blast = None

    for p in all :

        if p[1] > last[1]:
            blast = last
            last = p

    LAST = last
    BLAST = blast
    return last

def extract_path_date(f):
    """
    Extraction de la date contenue dans le nom du fichier
    :param path: chemin d'accès à l'extract spécifié
    :return: datetime
    """
    date= datetime.fromtimestamp(os.path.getmtime(os.path.join(EXPORTS_PATH, f)))
    return date

def load_last():
    last = get_last()
    df_sivic = pd.read_excel(EXPORTS_PATH + last[0], skiprows=2)
    return df_sivic

def change_age(df_sivic):
    print("Traitement des exceptions")
    df_sivic['Âge approximatif'] = df_sivic['Âge approximatif'].replace(
        regex={r'ans': '', r'mois': 0, r'semaine': 0, r'jour': 0, r'JOURS': 0, r'>80': 80, r'> 80': 80, r'SEM': 0,
               r'-': '', r'MOIS': 0, r'ANS': '', r'an': '', r'a': '', r'XX': '', r'X': '', r'NC': '',
               r'Age pproximtif': '', r',': '.'})
    df_sivic = df_sivic[df_sivic['Âge approximatif'] != 'Age approximatif']
    df_sivic = df_sivic[df_sivic['Âge approximatif'] != 'Age pproximtif']
    df_sivic = df_sivic[df_sivic['Âge approximatif'] != '']
    print("Traitement des NaN")
    df_sivic = df_sivic.dropna()
    df_sivic['Âge approximatif'] = df_sivic['Âge approximatif'].astype(float)
    df_sivic['Âge approximatif'] = df_sivic['Âge approximatif'].astype(int)
    print("Traitement des dates de naissance")
    df_sivic['Âge approximatif'] = np.where(df_sivic['Âge approximatif'] > 1900, 2020 - df_sivic['Âge approximatif'],
                                            df_sivic['Âge approximatif'])


print("Enregistrement du fichier")
#df_sivic.to_excel(r"\\ars75filer05\N-COV19\16_Cellule données\DATAS\SIVIC\exports_SI-VIC\{} {}/Export SIVIC_{}{}2020_SOM_Covid-19 - Suivi des hospitalisations au niveau national_age.xls".format(jour, mois,jour, mois))
