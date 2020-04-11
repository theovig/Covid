import pandas as pd

from exports import EMSExport
from rapports_utils import *
from datetime import timedelta

class Indicators():
    SAVE_DIR = "data/indicateurs/"
    DEPARTEMENTS = [75, 92, 93, 94, 91, 78, 95, 77]


    def __init__(self, export : EMSExport):
        self.export = export
        self.date = self.export.date
        self.df = self.export.df
        self.df_es=self.export.df_es

        self.df_bed=self.export.df_bed

        self.df_housses=self.export.df_housses
        self.d = {}

    def compute_simple(self):
        """
        Calcul des indicateurs de base
        """
        self.d = {}
        #self.d["#DATE"] = self.date.strftime("%d/%m/%y")
        self.d["DATE_JOUR"]=self.date.strftime("%A %d %B")
        date_1=self.date-timedelta(days=1)
        self.d["DAT_1"] = date_1.strftime("%d/%m")
        self.d["#HEURE"] = self.date.strftime("%H")

    def compute_age(self):
        """
        Calcul des indicateurs d'age
        """
        self.d["#MOY_AGE_HC"]=str(self.df.at["Région IdF","moy_age_hc"])
        self.d["#MOY_AGE_REA"] = str(self.df.at["Région IdF", "moy_age_rea"])
        self.d["#MED_AGE_HC"] = str(self.df.at["Région IdF", "median_age_hc"])
        self.d["#MED_AGE_REA"] = str(self.df.at["Région IdF", "median_age_rea"])

    def compute_lit_dispo(self):
        """
        Calcul des indicateurs d'age
        """
        self.d["BED_TOT_moins"]=str(int(self.df_bed.at["Covid Moins","Total"][2]+self.df_bed.at["Covid Moins","Total"][3]))
        self.d["BED_TOT_plus"] = str(int(self.df_bed.at["Covid Plus", "Total"][2] + self.df_bed.at["Covid Plus", "Total"][3]))

        df_bed_dpt=self.df_bed.iloc[:,:-1]
        for i in df_bed_dpt.columns:
            self.d["BED_TOT_+{}".format(i[-3:-1])]=str(int(self.df_bed.at["Covid Plus", i][2] + self.df_bed.at["Covid Plus", i][3]))
            self.d["BED_TOT_-{}".format(i[-3:-1])] = str(int(
                self.df_bed.at["Covid Moins", i][2] + self.df_bed.at["Covid Moins", i][3]))


    def compute_lits(self):
        """
        Calcul des indicateurs de lits
        """
        self.d["#LIT_REA"] = str(self.df.at["Région IdF", "Hospitalisation_reanimatoire"])
        self.d["#LIT_HC"] = str(self.df.at["Région IdF", "Hospitalisation_conventionnelle"])
        self.d["#LIT_SSR"] = str(self.df.at["Région IdF", "Hospitalisation_en_SSR"])
        self.d["#LIT_PSY"] = str(self.df.at["Région IdF", "Hospitalisation_psychiatrique"])
        self.d["#LIT_TOT"] = str(self.df.at["Région IdF", "Total_Hospitalisation"])

        for i in self.DEPARTEMENTS:
            self.d["LIT_{}_REA".format(i)] = str(self.df.at[i, "Hospitalisation_reanimatoire"])

    def compute_deces(self):
        """
        Calcul des indicateurs de décès
        """
        tot=self.df.at["Région IdF", "nb_dc"]
        nouveaux=self.df.at["Région IdF", "new_dc"]
        variation=nouveaux/(tot-nouveaux)*100

        self.d["#DEC_TOT"] = str(int(tot))
        self.d["#DEC_NV"] = str(int(nouveaux))
        self.d["#VAR_DEC"] = str(int(variation))

        for i in self.DEPARTEMENTS:
            tot = self.df.at[i, "nb_dc"]
            nouveaux = self.df.at[i, "new_dc"]
            variation = nouveaux/(tot - nouveaux)*100
            self.d["DEC_TOT_{}".format(i)] = str(int(tot))
            self.d["DEC_{}_NV".format(i)] = str(int(nouveaux))
            self.d["VAR_{}_DEC".format(i)] = str(int(variation))

    def compute_nv_rea(self):
        """
        Calcul des établissements qui récupère le plus de personnes en réa entre deux extracts,
        ainsi que la variation totale et par département
        """
        df_rea=self.df_es[["somatique_etablissement_actuel","new_rea"]]
        self.d["#VAR_TOT_REA"]=str(df_rea["new_rea"].sum())
        df_rea=df_rea.sort_values("new_rea",ascending=False).iloc[:10,:]
        for i in range(10):
            self.d["#NOM_NV_REA_{}".format(i)]=df_rea.iat[i,0]
            self.d["#NUM_NV_REA_{}".format(i)] = str(int(df_rea.iat[i, 1]))

        df_rea_dpt=self.df_es["new_rea"]
        df_rea_dpt=df_rea_dpt.groupby("dpt").sum()
        ind=0
        for i in df_rea_dpt.index:
            self.d["DPT_NV_REA_{}".format(i)] = str(df_rea_dpt.iat[ind])
            ind += 1
            lits=int(self.d["LIT_{}_REA".format(i)])
            nv=int(float(self.d["DPT_NV_REA_{}".format(i)]))
            var=int(round(nv/(lits-nv)*100,0))
            self.d["#DPT_VAR_NV_REA_{}".format(i)]=str(int(var))

    def compute_var_rea(self):
        """
        Calcul de la variation totale en réa en pourcentage
        """
        var=int(float(self.d["#VAR_TOT_REA"]))/(int(float(self.d["#LIT_REA"]))-int(float(self.d["#VAR_TOT_REA"])))*100
        self.d["#REA_VAR_TOT"]=str(int(round(var)))


    def compute_fune_housses(self):
        print(self.df_housses.columns)
        self.df_housses=self.df_housses.rename(columns={"Unnamed: 8": "ESMS", "Unnamed: 9": "TOTAL DPT","Unnamed: 10":"AP-HP","Unnamed: 11":"Hors AP-HP", "Unnamed: 12":"ESMS.1", "Unnamed: 13": "TOTAL_ES", "Unnamed: 14":"TOTAL DPT.1"})
        self.d["CH_MORTU_TOT"]=str(int(self.df_housses.at["TOTAL REG", "TOTAL DPT"]))
        self.d["CH_MORTU_ESMS"] = str(int(self.df_housses.at["TOTAL", "ESMS"]))
        self.d["CH_MORTU_MOBILE"] = str(int(self.df_housses.at["TOTAL", "mobile"]))
        self.d["HOUSSES_TOT"] = str(int(self.df_housses.at["TOTAL REG", "TOTAL DPT.1"]))
        self.d["HOUSSES_ESMS"] = str(int(self.df_housses.at["TOTAL", "ESMS.1"]))
        self.df_housses["TOTAL DPT"] = self.df_housses["TOTAL DPT"].astype(float)
        i=0
        for dpt,row in self.df_housses.iterrows():
            if i > 7 :
                break
            i+=1
            self.d["CH_MORTU_{}_TOT".format(dpt)] = str(int(row["TOTAL DPT"]))
            self.d["CH_MORTU_{}_ESMS".format(dpt)] = str(int(row["ESMS"]))
            self.d["CH_MORTU_{}_MOBILE".format(dpt)] = str(int(row["mobile"]))
            self.d["HOUSSES_{}_TOT".format(dpt)] = str(int(row["TOTAL DPT.1"]))
            self.d["HOUSSES_{}_ESMS".format(dpt)] = str(int(row["ESMS.1"]))


    def compute_nv_dc(self):
        """
        Calcul des établissements qui ont le plus de décès entre deux extracts
        """
        df_dc=self.df_es[["somatique_etablissement_actuel","new_dc"]]
        df_dc=df_dc.sort_values("new_dc",ascending=False).iloc[:10,:]
        for i in range(10):
            self.d["NOM_NV_DC_{}".format(i)]=df_dc.iat[i,0]
            self.d["NUM_NV_DC_{}".format(i)] = str(int(df_dc.iat[i, 1]))

    def compute_all(self):
        """
        Calcul tous les indicateurs
        """
        self.compute_simple()
        self.compute_lits()
        self.compute_age()
        self.compute_deces()
        self.compute_nv_rea()
        self.compute_nv_dc()
        self.compute_lit_dispo()
        self.compute_fune_housses()
        self.compute_var_rea()

    def save(self):
        """
        Enregistrement dans la base des indicateurs
        """
        df = pd.DataFrame(columns=[c for c in self.d])
        df = df.append([self.d])
        df.to_excel(self.SAVE_DIR + "bdd.xlsx")


    def publish_rapport(self):
        """
        Création du rapport de situation
        """

        #word_autocomplete(self.date, self.d)
        ppt_autocomplete(self. date, self.d)
        #xls_autocomplete(self.date, self.d)

i=Indicators(EMSExport())
i.compute_all()
i.publish_rapport()