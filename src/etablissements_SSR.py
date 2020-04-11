import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pathlib


class Etablissements():

    Départements = ["Essonne (91)",
                    "Hauts-de-Seine (92)",
                    "Paris (75)",
                    "Seine-et-Marne (77)",
                    "Seine-Saint-Denis (93)",
                    "Val-de-Marne (94)",
                    "Val-d'Oise (95)",
                    "Yvelines (78)"
                    ]

    def __init__(self,jour, mois, heure):
        self.df_sivic=pd.DataFrame()
        self.X=[]
        self.jour=jour
        self.mois=mois
        self.heure=heure
        self.jour_arret = jour[-1]
        self.etablissements=[]
        self.new_etab=[]

    def load(self):
        print("loading")
        for m in self.mois:
            for j in self.jour:
                for h in self.heure:
                    file = pathlib.Path("./Data_Sivic/{}{}2020_{}h.xls".format(j,m,h))

                    if file.exists():
                        self.jour_arret=j

                        df_interim = pd.read_excel("./Data_Sivic/{}{}2020_{}h.xls".format(j,m, h))
                        df_interim=df_interim[['Numéro SINUS',"SOMATIQUE\nType d'hospitalisation","SOMATIQUE\nDépartement", "SOMATIQUE\nEtablissement actuel"]]
                        df_interim=df_interim.rename(columns={'Numéro SINUS': 'Patient',"SOMATIQUE\nType d'hospitalisation":'Hospit', "SOMATIQUE\nDépartement":"dpt","SOMATIQUE\nEtablissement actuel":"Etab_{}{}2020_{}h".format(j,m,h)})
                        self.df_sivic = pd.concat([self.df_sivic, df_interim], ignore_index=True)
                        print("Done: ",j,"/",m," à ", h,"h")

    def get_date(self):

        for m in self.mois:
            for j in self.jour:
                for h in self.heure:
                    file = pathlib.Path("./Data_Sivic/{}{}2020_{}h.xls".format(j,m,h))
                    if file.exists():
                        datetime_str = '{}/{}'.format(j,m)
                        #datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
                        self.X += [datetime_str]

    def load_and_save(self,cond):
        if not cond:
            self.load()
            self.df_sivic.to_csv("{}{}2020_{}h_etab.csv".format(self.jour_arret,mois[-1],heure[-1]))
        else:
            self.df_sivic = pd.read_csv("{}{}2020_{}h_etab.csv".format(self.jour_arret, mois[-1], heure[-1]))

    def count_etab(self):
        self.df_sivic = self.df_sivic[self.df_sivic["dpt"].isin(self.Départements)]
        self.df_sivic = self.df_sivic[self.df_sivic["Hospit"]=="Hospitalisation en SSR"]
        columns = self.df_sivic.columns
        for i in columns:
            if i[:4]=='Etab':
                self.etablissements+=[len(self.df_sivic[i].value_counts().notna())]

    def count_new_etab(self):
        for i in range(len(self.etablissements)-1):
            if self.etablissements[i+1]-self.etablissements[i]<0:
                self.new_etab += [0]
            else:
                self.new_etab+=[self.etablissements[i+1]-self.etablissements[i]]

    def plot_etab(self):
        plt.bar(self.X[1:], self.new_etab)

        plt.title("Nouveaux établissements SSR déclarants")
        plt.savefig('data/figures/plot_etab_SSR.png')
        plt.show()

    def compute(self, cond):
        self.load_and_save(cond)
        self.get_date()
        self.count_etab()
        self.count_new_etab()
        self.plot_etab()


jour=[25,27,28,29,30,31,'01','02','03','04','05','06','07']
heure=[17]
mois=['03','04']
cond = pathlib.Path("{}{}2020_{}h_etab.csv".format(jour[-1], mois[-1], heure[-1])).exists()

test = False
etab=Etablissements(jour, mois, heure)
etab.compute(cond)