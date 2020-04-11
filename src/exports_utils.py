"""
Fonctions de gestions des exports_bruts excels de la plateforme gestion COVID-19 EMS
"""
import os
import os.path
from datetime import datetime,timedelta
import locale
from exports_traitement import Traitement
locale.setlocale(locale.LC_TIME,'')

import pandas as pd

#from exports_dict import dictionnaire

#EXPORTS_PATH = "data/exports_bruts/"
EXPORTS_PATH ="exports_bruts/"
LAST_dpt =None
BLAST_dpt=None

LAST_es =None
BLAST_es=None

LAST_esms =None
BLAST_esms=None

LAST_bed =None
BLAST_bed=None

LAST_housses =None
BLAST_housses=None

LAST_sivic =None
BLAST_sivic=None

def extract_date(f,hour=17):
    """
    Extraction de la date contenue dans le nom du fichier
    :param path: chemin d'accès à l'extract spécifié
    :return: datetime
    """
    #date= datetime.fromtimestamp(os.path.getmtime(os.path.join(EXPORTS_PATH, f)))

    datetime_str = f[13:21]
    datetime_str=datetime_str[0:2]+"/"+datetime_str[2:4]+"/"+datetime_str[4:6]
    datetime_object = datetime.strptime(datetime_str, '%d/%m/%y')
    date=datetime_object.replace(hour=hour)
    return date

def extract_path_date(EXPORTS_PATH,f):
    """
    Extraction de la date contenue dans le nom du fichier
    :param path: chemin d'accès à l'extract spécifié
    :return: datetime
    """

    date= datetime.fromtimestamp(os.path.getmtime(os.path.join(EXPORTS_PATH, f)))
    return date


def explore():
    """
    Liste les différents exports_bruts contenus dans le dossier data/exports_bruts
    :return: List (path, date_export) par type de fichier lu
            --> indicateurs par établissement de santé ou par département
    """
    result_dpt=[]
    result_es = []
    results_bed=[]
    results_housses=[]
    results_esms=[]
    results_sivic=[]
    for f in os.listdir(EXPORTS_PATH):
        if f[:22]=="indicateurs_sivic_dpts":
            if os.path.isfile(os.path.join(EXPORTS_PATH, f)) and f[-5:] == ".xlsx":
                result_dpt += [(f, extract_path_date(EXPORTS_PATH,f))]

        if f[:20] == "indicateurs_sivic_es":
            if os.path.isfile(os.path.join(EXPORTS_PATH, f)) and f[-5:] == ".xlsx":
                result_es += [(f, extract_path_date(EXPORTS_PATH,f))]
        if f[9:13] == "Lits":
            if os.path.isfile(os.path.join(EXPORTS_PATH, f)) and f[-5:] == ".xlsx":
                results_bed += [(f, extract_path_date(EXPORTS_PATH,f))]
        #if = ESMS:
        if f[:4]=="Funé":
            if os.path.isfile(os.path.join(EXPORTS_PATH, f)) and f[-5:] == ".xlsx":
                results_housses += [(f, extract_path_date(EXPORTS_PATH,f))]
        if f[:6]=="Export":
            if os.path.isfile(os.path.join(EXPORTS_PATH, f)) and f[-4:] == ".xls":
                results_sivic += [(f, extract_path_date(EXPORTS_PATH,f))]

    return result_dpt, result_es,results_bed, results_esms,results_housses,results_sivic

def get_last_dpt():
    """
    Trouve le dernier export contenu dans le dossier data/exports_bruts
    :return: (path, date_export)
    """
    global LAST_dpt, BLAST_dpt
    if not(LAST_dpt is None):
        return LAST_dpt

    all = explore()[0]
    last = all[0]
    blast = None

    for p in all :

        if p[1] > last[1]:
            blast = last
            last = p

    LAST_dpt = last
    BLAST_dpt = blast
    return last


def get_last_sivic():
    """
    Trouve le dernier export contenu dans le dossier data/exports_bruts
    :return: (path, date_export)
    """
    global LAST_sivic, BLAST_sivic
    if not(LAST_sivic is None):
        return LAST_sivic

    all = explore()[5]
    last = all[0]
    blast = None

    for p in all :
        if p[1] > last[1]:
            blast = last
            last = p
    all.remove(last)
    last2 = all[0]
    for p in all :
        if p[1] > last2[1]:
            blast = last2
            last2 = p
    LAST_sivic = last
    BLAST_sivic = blast
    return last,last2

def get_last_es():
    """
    Trouve le dernier export contenu dans le dossier data/exports_bruts
    :return: (path, date_export)
    """
    global LAST_es, BLAST_es
    if not(LAST_es is None):
        return LAST_es

    all = explore()[1]
    last = all[0]
    blast = None

    for p in all :
        if p[1] > last[1]:
            blast = last
            last = p

    LAST_es = last
    BLAST_es = blast
    return last

#def get_before_last():
    """
    Trouve l'avant dernier export
    :return: (path, date_export)
    """
 #   global BLAST
  #  if BLAST is None :
   #     get_last()
    #return BLAST

def get_last_bed():
    """
    Trouve le dernier export contenu dans le dossier data/exports_bruts
    :return: (path, date_export)
    """
    global LAST_bed, BLAST_bed
    if not(LAST_bed is None):
        return LAST_bed

    all = explore()[2]
    last = all[0]
    blast = None

    for p in all :
        if p[1] > last[1]:
            blast = last
            last = p

    LAST_bed = last
    BLAST_bed = blast
    return last

def get_last_esms():
    """
    Trouve le dernier export contenu dans le dossier data/exports_bruts
    :return: (path, date_export)
    """
    global LAST_esms, BLAST_esms
    if not(LAST_esms is None):
        return LAST_esms

    all = explore()[3]
    last = all[0]
    blast = None

    for p in all :
        if p[1] > last[1]:
            blast = last
            last = p

    LAST_esms = last
    BLAST_esms = blast
    return last

def get_last_housses():
    """
    Trouve le dernier export contenu dans le dossier data/exports_bruts
    :return: (path, date_export)
    """
    global LAST_housses, BLAST_housses
    if not(LAST_housses is None):
        return LAST_housses

    all = explore()[4]
    last = all[0]
    blast = None

    for p in all :
        if p[1] > last[1]:
            blast = last
            last = p

    LAST_housses = last
    BLAST_housses = blast
    return last

def load(file_name):
    """
    Charge le fichier d'export spécifié
    :param file_name: Nom du fichier d'export brut
    :return: Dataframe, date
    """

    date = extract_path_date(file_name)
    df = pd.read_excel(EXPORTS_PATH + last[0], index_col="dpt")

    last_es = get_last_es()
    df_es = pd.read_excel(EXPORTS_PATH + last_es[0], index_col="dpt")

    last_bed = get_last_bed()
    df_bed = pd.read_excel(EXPORTS_PATH + last_bed[0], index_col="dpt")

    return df, df_es, def_bed, date

def load_last():
    """
    Charge le dernier export réalisé
    :return: Dataframe, Datetime
    """

    #last = get_last_dpt()
    #df = pd.read_excel(EXPORTS_PATH+last[0], index_col="dpt")
    #last_es = get_last_es()
    #df_es = pd.read_excel(EXPORTS_PATH + last_es[0], index_col="dpt")
    print("Démarrage")
    last_sivic,last2_sivic=get_last_sivic()
    print("Export de Sivic réalisé")
    df,df_es=Traitement(EXPORTS_PATH +last_sivic[0],EXPORTS_PATH +last2_sivic[0]).build()
    df=df.set_index("dpt")
    df_es=df_es.set_index("dpt")

    print("Sivic traité")

    date = extract_date(last_sivic[0])
    #date_1 = date - timedelta(days=1)
    date_1 = date.strftime("%d%m%y")+"20"

    last_bed = get_last_bed()
    df_bed = pd.read_excel(EXPORTS_PATH + last_bed[0],skiprows=2, index_col="Unnamed: 0")

    print("Cellule bed management traité")

    cols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    last_housses = get_last_housses()
    df_housses = pd.read_excel(EXPORTS_PATH + last_housses[0], skiprows=3,sheet_name=date_1,usecols=cols, index_col="Unnamed: 0")

    return df,df_es, df_bed,df_housses, date

#print(load_last(17))



