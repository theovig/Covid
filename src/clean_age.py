from exports_utils import get_last_sivic, extract_path_date
import numpy as np
import datetime
import re
import pandas as pd

class Age():
    TODAY = datetime.date.today()
    def __init__(self, path):
        self.path=path

    def clean_age(self,txt:str):
        """
        Extraction de l'age en années à partir d'un texte
        :param txt: age en str
        :return: age en float ou NaN
        """
        trash = ['-','XX','X','NC','Age approximatif']
        if txt in trash :
            return np.NaN
        txt =  txt.replace(" ","").upper()
        if txt.isdigit():
            nb = float(txt)
            if nb < 1000 :
                return nb
            return self.TODAY.year - nb
        try:
            return float(txt)
        except ValueError:
            pass

        if "/" in txt :
            #Date probable
            try :
                date = datetime.datetime.strptime(txt,"%d/%m/%Y")
                return self.TODAY.year - date.year
            except:
                return np.NaN

        lm = re.findall('>(\d+)', txt)
        if len(lm) > 0:
            return int(lm[0])

        ans = -1.0
        lm = re.findall('(\d+)A', txt)
        if len(lm) > 0 :
            ans = int(lm[0])
        mois = -1
        lm = re.findall('(\d+)MOIS', txt)
        if len(lm) > 0:
            mois = int(lm[0])
        semaines = -1
        lm = re.findall('(\d+)S', txt)
        if len(lm) > 0:
            semaines = int(lm[0])
        jours = -1
        lm = re.findall('(\d+)JOUR', txt)
        if len(lm) > 0:
            jours = int(lm[0])

        if ans < 0 and (semaines >= 0 or mois >=0 or jours >= 0):
            ans = 0
        if semaines >= 0:
            ans += semaines/52.0
        if mois >= 0:
            ans += mois/12.0
        if jours >= 0:
            ans += jours/365.0
        if ans < -1 :
            return np.NaN
        return ans

    def open_extract(self) :
        df = pd.read_excel(self.path, skiprows=2)
        df["Âge approximatif"] =  df["Âge approximatif"].apply(self.clean_age)
        return df

EXPORTS_PATH ="exports_bruts/"
last,last_2=get_last_sivic()
age=Age(EXPORTS_PATH+last[0]).open_extract()
age.to_excel("Resultats/sivic_clean_age_{}_{}.xls".format(last[1].day,last[1].month))