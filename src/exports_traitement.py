import pandas as pd
import datetime
import re
import numpy as np



class Traitement():

    TODAY = datetime.date.today()
    DEP_IDF = [75, 77, 78, 91, 92, 93, 94, 95]
    path = "Resultats/"


    TB  =[
        ("STATUT_SOMATIQUE","Hospitalisation","count","Total_Hospitalisation"),
        ("TYPE_SOMATIQUE", "Hospitalisation conventionnelle","count","Hospitalisation_conventionnelle"),
        ("TYPE_SOMATIQUE","Hospitalisation réanimatoire (réa ou SI)","count","Hospitalisation_reanimatoire"),
        ("TYPE_SOMATIQUE","Hospitalisation en SSR","count","Hospitalisation_en_SSR"),
        ("TYPE_SOMATIQUE","Hospitalisation psychiatrique","count","Hospitalisation_psychiatrique"),
        ("STATUT_SOMATIQUE","Décès","count","nb_dc"),
        #"new_dc",
        ("TYPE_SOMATIQUE", "Hospitalisation conventionnelle","mean","moy_age_hc"),
        ("TYPE_SOMATIQUE", "Hospitalisation conventionnelle","median","median_age_hc"),
        ("TYPE_SOMATIQUE", "Hospitalisation réanimatoire (réa ou SI)","mean","moy_age_rea"),
        ("TYPE_SOMATIQUE", "Hospitalisation réanimatoire (réa ou SI)","median","median_age_rea")
    ]


    def __init__(self,path1, path2):
        self.path1=path1
        self.path2=path2

    def compute_row(self,df_dep, row):
        """
        Calcule les indicateurs de tb pour une zone géographique
        :param df_dep: Dataframe préfiltré sur une zone géographique
        :param row: Dict pour stocker la ligne
        :return: Dict avec les indicateurs complétés
        """
        for ctr_col, fltr, aggf, ncol in self.TB:
            def_cat = df_dep[df_dep[ctr_col] == fltr]
            if aggf == "count":
                row[ncol] = len(def_cat.index)
            else:
                row[ncol] = def_cat["AGE"].dropna().agg(aggf)
        return row

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


    def open_extract(self,path) :
        cols = ["Numéro SINUS","Âge approximatif","SOMATIQUE\nStatut","SOMATIQUE\nType d'hospitalisation",
                "SOMATIQUE\nDépartement", "SOMATIQUE\nEtablissement actuel"]
        df = pd.read_excel(path, skiprows=2, usecols=cols)
        df.columns = ["SINUS","AGE","STATUT_SOMATIQUE","TYPE_SOMATIQUE", "DEP", "ETABLISSEMENT"]

        #Netoyage DF
        df["AGE"] =  df["AGE"].apply(self.clean_age)
        df["DEP"] =  df["DEP"].apply(lambda x : int(re.findall("\((\d+)\)", x)[0]))
        #df = df.dropna()
        return df

    def build(self):
        df =  self.open_extract(self.path1)
        result = pd.DataFrame(columns=["dpt"]+[c for _,_,_,c in self.TB])
        for dep in self.DEP_IDF :
            df_dep = df[df["DEP"] == dep]
            row = self.compute_row(df_dep, {"dpt":dep})
            result = result.append(row, ignore_index=True)

        #TOUTE LA REGION
        df_dep = df[df["DEP"].isin(self.DEP_IDF)]
        row = self.compute_row(df_dep, {"dpt":"Région IdF"})
        result = result.append(row, ignore_index=True)
        #HORS REGION
        df_dep = df[~df["DEP"].isin(self.DEP_IDF)]
        row = self.compute_row(df_dep, {"dpt":"Hors Région IdF"})
        result = result.append(row, ignore_index=True)

        #DECES HIER
        df2 = self.open_extract(self.path2)
        df2_dc = df2[df2["STATUT_SOMATIQUE"] == "Décès"]
        nd = pd.DataFrame(columns = ["dpt", "new_dc"])
        for dep in self.DEP_IDF :
            deaths = len(df2_dc[df2_dc["DEP"] == dep].index)
            nd = nd.append({"dpt":dep, "new_dc":deaths}, ignore_index=True)
        deaths = len(df2_dc[df2_dc["DEP"].isin(self.DEP_IDF)].index)
        nd = nd.append({"dpt": "Région IdF", "new_dc": deaths}, ignore_index=True)
        deaths = len(df2_dc[~df2_dc["DEP"].isin(self.DEP_IDF)].index)
        nd = nd.append({"dpt": "Hors Région IdF", "new_dc": deaths}, ignore_index=True)

        result = pd.merge(result, nd, on = "dpt")


        result.to_excel(self.path+"sivic_dpt.xlsx", index=False)

        #Deuxième fichier
        df["nb_rea"] = df["TYPE_SOMATIQUE"].apply(lambda x : 1 if x == "Hospitalisation réanimatoire (réa ou SI)" else 0)
        df["nb_hc"] = df["TYPE_SOMATIQUE"].apply(lambda x: 1 if x == "Hospitalisation conventionnelle" else 0)
        df["nb_ssr"] = df["TYPE_SOMATIQUE"].apply(lambda x: 1 if x == "Hospitalisation en SSR" else 0)
        df["nb_psy"] = df["TYPE_SOMATIQUE"].apply(lambda x: 1 if x == "Hospitalisation psychiatrique" else 0)
        df["nb_dc"] = df["STATUT_SOMATIQUE"].apply(lambda x: 1 if x == "Décès" else 0)
        df = df.groupby(["ETABLISSEMENT","DEP"], as_index=False).agg(
            {c : "sum" for c in ["nb_rea","nb_hc","nb_ssr","nb_psy","nb_dc"]})


        df2["nb_rea2"] = df2["TYPE_SOMATIQUE"].apply(lambda x: 1 if x == "Hospitalisation réanimatoire (réa ou SI)" else 0)
        df2["nb_hc2"] = df2["TYPE_SOMATIQUE"].apply(lambda x: 1 if x == "Hospitalisation conventionnelle" else 0)
        df2["nb_ssr2"] = df2["TYPE_SOMATIQUE"].apply(lambda x: 1 if x == "Hospitalisation en SSR" else 0)
        df2["nb_psy2"] = df2["TYPE_SOMATIQUE"].apply(lambda x: 1 if x == "Hospitalisation psychiatrique" else 0)
        df2["nb_dc2"] = df2["STATUT_SOMATIQUE"].apply(lambda x: 1 if x == "Décès" else 0)
        df2 = df2.groupby(["ETABLISSEMENT", "DEP"], as_index=False).agg(
            {c: "sum" for c in ["nb_rea2", "nb_hc2", "nb_ssr2", "nb_psy2", "nb_dc2"]})

        df = pd.merge(df, df2, on = ["ETABLISSEMENT","DEP"], how="outer")
        df = df.fillna(0)
        df["new_rea"] = df["nb_rea"]- df["nb_rea2"]
        df["new_hc"] = df["nb_hc"] - df["nb_hc2"]
        df["new_ssr"] = df["nb_ssr"] - df["nb_ssr2"]
        df["new_psy"] = df["nb_psy"] - df["nb_psy2"]
        df["new_dc"] = df["nb_dc"] - df["nb_dc2"]

        df = df[["ETABLISSEMENT","DEP"]+["nb_rea","nb_hc","nb_ssr","nb_psy","nb_dc"]+["new_rea","new_hc","new_ssr","new_psy","new_dc"]]
        df=df[df["DEP"].isin(self.DEP_IDF)]
        df = df.rename(columns={"ETABLISSEMENT":"somatique_etablissement_actuel","DEP":"dpt"})

        df.to_excel(self.path+"sivic_es.xlsx", index=False)
        result=result.fillna(0)
        df=df.fillna(0)
        dict = {}
        for i in result.columns[1:]:
            dict[i] = int
        result = result.astype(dict)
        for i in result.index[:8]:
            result.at[i, "dpt"] = int(result.at[i, "dpt"])
        result["new_dc"] = result["nb_dc"] - result["new_dc"]

        return result, df


