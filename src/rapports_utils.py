"""
Fonction de gestion des rapports générés par le logiciel
"""

import os
import os.path

BASE_SAVE_DIR ="Resultats/"
#BASE_SAVE_DIR =r"\\ars75filer05\N-COV19\16_Cellule données\THEO\Resultats"

def get_save_path(date):
    """
    Retourne le dossier de sauvegarde étant donné une date.
    Si le dossier pour la date donnée n'existe pas il sera créé.
    :return: Chemin du dossier
    """
    path =  BASE_SAVE_DIR + date.strftime("%d%m%y")

    if not(os.path.exists(path) and os.path.isdir(path)):
        #Si le dossier n'existe pas on le crée
        os.mkdir(path)

    return path

def ppt_autocomplete(date, indicators):
    """
    Cree et complete un rapport de situation ppt
    :param date: date de l'extraction
    :param indicators: dictionnaire d'indicateurs
    """
    io ='modele_nv_ppt.xml'
    file = str(open(io, 'r', encoding="utf8").read())

    for indic in indicators :
        file = file.replace(indic, indicators[indic])


    name = date.strftime("%d%m%y %H") + "h Reporting DG.xml"
    path = get_save_path(date) + "/"

    rfile = open(path + name, "w", encoding="utf8")
    rfile.write(file)
    rfile.close()

def word_autocomplete(date, indicators):
    """
    Cree et complete un rapport de situation
    :param date: date de l'extraction
    :param indicators: dictionnaire d'indicateurs
    """
    io = BASE_SAVE_DIR+'modele.xml'
    file = str(open(io, 'r', encoding="utf8").read())

    for indic in indicators :
        file = file.replace(indic, indicators[indic])


    name = date.strftime("%d%m%y %H%M%S") + ".xml"
    path = get_save_path(date) + "/"

    rfile = open(path + name, "w", encoding="utf8")
    rfile.write(file)
    rfile.close()

def xls_autocomplete(date, indicators):
    """
    Cree et complete un rapport de situation ppt
    :param date: date de l'extraction
    :param indicators: dictionnaire d'indicateurs
    """
    print("Ecriture du ppt")
    io = BASE_SAVE_DIR+'modele_xls.xml'
    file = str(open(io, 'r', encoding="utf8").read())

    for indic in indicators :
        file = file.replace(indic, indicators[indic])


    name = date.strftime("%d%m%y REPORTING CRAPS DG") + ".xml"
    path = get_save_path(date) + "/"

    rfile = open(path + name, "w", encoding="utf8")
    rfile.write(file)
    rfile.close()

CAT_PH = [
    182,183,186,188,189,190,192,194,195,196,198,221,238,246,249,252,
    253,255,370,377,379,382,390,395,396,437,445,446,448,449,461,464,
    209,354]