import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pathlib


class Sejour():

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
        self.rea=[]
        self.HC=[]
        self.SSR=[]

    def load(self):
        print("loading")
        for m in self.mois:
            for j in self.jour:
                for h in self.heure:
                    file = pathlib.Path("./Data_Sivic/{}{}2020_{}h.xls".format(j,m,h))

                    if file.exists():
                        self.jour_arret=j

                        df_interim = pd.read_excel("./Data_Sivic/{}{}2020_{}h.xls".format(j,m, h))
                        df_interim=df_interim[['Numéro SINUS',"SOMATIQUE\nType d'hospitalisation","SOMATIQUE\nDépartement"]]
                        df_interim=df_interim.rename(columns={'Numéro SINUS': 'Patient',"SOMATIQUE\nType d'hospitalisation":'Hospit_{}{}2020_{}h'.format(j,m,h), "SOMATIQUE\nDépartement":"dpt"})
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
            self.df_sivic.to_csv("{}{}2020_{}h_sejour.csv".format(self.jour_arret,mois[-1],heure[-1]))
        else:
            self.df_sivic = pd.read_csv("{}{}2020_{}h_sejour.csv".format(self.jour_arret, mois[-1], heure[-1]))

    def count_sejours(self):
        self.df_sivic = self.df_sivic[self.df_sivic["dpt"].isin(self.Départements)]
        columns = self.df_sivic.columns
        for i in columns:
            if i[:6]=='Hospit':
                self.rea+=[self.df_sivic[i].value_counts()["Hospitalisation réanimatoire (réa ou SI)"]]
                self.HC+=[self.df_sivic[i].value_counts()["Hospitalisation conventionnelle"]]
                self.SSR += [self.df_sivic[i].value_counts()["Hospitalisation en SSR"]]

    def plot_sejours(self):
        plt.plot(self.X, self.rea,label="Séjours en réanimation")
        plt.plot(self.X, self.SSR, label="Séjours en SSR")
        plt.plot(self.X, self.HC, label="Séjours en HC")
        plt.legend()
        plt.title('Evolution des séjours')
        plt.savefig('data/figures/plot_sejours.png')
        plt.show()

    def compute(self, cond):
        self.load_and_save(cond)
        self.get_date()
        self.count_sejours()
        self.plot_sejours()


jour=[25,27,28,29,30,31,'01','02','03','04','05','06','07']
heure=[17]
mois=['03','04']
cond = pathlib.Path("{}{}2020_{}h_sejour.csv".format(jour[-1], mois[-1], heure[-1])).exists()

test = False
sejour=Sejour(jour, mois, heure)
sejour.compute(cond)