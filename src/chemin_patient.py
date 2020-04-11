import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import*
import os
import os.path
import datetime
from exports_utils import extract_path_date



class Chemin_patient():
    EXPORTS_PATH = "data_from_sivic/"
    TODAY = datetime.date.today()
    CSV_PATH="csv/"

    Départements = ["Essonne (91)",
                    "Hauts-de-Seine (92)",
                    "Paris (75)",
                    "Seine-et-Marne (77)",
                    "Seine-Saint-Denis (93)",
                    "Val-de-Marne (94)",
                    "Val-d'Oise (95)",
                    "Yvelines (78)"
                    ]

    condition_statut = ["-", "Décès", "Hospitalisation", "Soins aux urgences", "Retour à domicile"]
    condition_hospit = ["-", "Hospitalisation conventionnelle", "Hospitalisation en SSR",
                        "Hospitalisation réanimatoire (réa ou SI)", "Hospitalisation psychiatrique"]

    def __init__(self,jour, mois, heure):
        self.jour=jour
        self.mois=mois
        self.heure=heure
        self.df_sivic=pd.DataFrame()
        self.columns=None
        self.X=[]
        self.jour_arret=jour[-1]

        self.new_columns=0

        self.status = []
        self.hospit = []
        self.rea_nouveaux = [0]
        self.nouveau_morts = [0]
        self.hc_nouveaux = [0]
        self.SSR = [0]
        self.psy = [0]

        self.entree_rea = [0]
        self.entree_rea_HC = [0]
        self.entree_rea_SU = [0]
        self.entree_rea_SSR = [0]
        self.entree_rea_NR=[0]

        self.sortie_rea = [0]
        self.sortie_rea_HC = [0]
        self.sortie_rea_dc = [0]
        self.sortie_rea_SSR = [0]
        self.sortie_rea_RAD = [0]
        self.sortie_rea_NR = [0]

        self.entree_SSR = [0]
        self.entree_SSR_HC = [0]
        self.entree_SSR_SU = [0]
        self.entree_SSR_rea = [0]
        self.entree_SSR_NR = [0]

        self.entree_HC = [0]
        self.entree_HC_SSR = [0]
        self.entree_HC_SU = [0]
        self.entree_HC_rea = [0]
        self.entree_HC_NR = [0]

        self.sortie_HC = [0]
        self.sortie_HC_SSR = [0]
        self.sortie_HC_dc = [0]
        self.sortie_HC_rea = [0]
        self.sortie_HC_RAD = [0]
        self.sortie_HC_NR = [0]

        self.sortie_SSR = [0]
        self.sortie_SSR_HC = [0]
        self.sortie_SSR_dc = [0]
        self.sortie_SSR_rea = [0]
        self.sortie_SSR_RAD = [0]
        self.sortie_SSR_NR = [0]

        self.data_dc=None
        self.data_rea=None
        self.data_entree_rea=None
        self.data_sortie_rea=None

        self.data_SSR = None
        self.data_entree_SSR = None
        self.data_sortie_SSR = None

        self.data_HC = None
        self.data_entree_HC = None
        self.data_sortie_HC = None

    def load(self):
        print("loading")
        for m in self.mois:
            for j in self.jour:
                for h in self.heure:
                    file = pathlib.Path("./Data_Sivic/{}{}2020_{}h.xls".format(j,m,h))

                    if file.exists():
                        self.jour_arret=j

                        df_interim = pd.read_excel("./Data_Sivic/{}{}2020_{}h.xls".format(j,m, h))
                        df_interim=df_interim[['Numéro SINUS','SOMATIQUE\nStatut',"SOMATIQUE\nType d'hospitalisation","SOMATIQUE\nDépartement"]]
                        df_interim=df_interim.rename(columns={'Numéro SINUS': 'Patient', 'SOMATIQUE\nStatut': 'Statut_{}{}2020_{}h'.format(j,m,h),"SOMATIQUE\nType d'hospitalisation":'Hospit_{}{}2020_{}h'.format(j,m,h), "SOMATIQUE\nDépartement":"dpt"})

                        conditions = [
                        df_interim.iloc[:, 2] == self.condition_hospit[3],
                        df_interim.iloc[:, 2] == self.condition_hospit[1],
                        df_interim.iloc[:, 2] == self.condition_hospit[0],
                        df_interim.iloc[:, 2] == self.condition_hospit[2],
                        df_interim.iloc[:, 2] == self.condition_hospit[4]
                        ]
                        choix=[1,2,3,4,5]

                        conditions_statut = [
                            df_interim.iloc[:, 1] == self.condition_statut[1],
                            df_interim.iloc[:, 1] == self.condition_statut[0],
                            df_interim.iloc[:, 1] == self.condition_statut[2],
                            df_interim.iloc[:, 1] == self.condition_statut[3],
                            df_interim.iloc[:, 1] == self.condition_statut[4]
                        ]
                        choix_statut = [1, 2, 3, 4, 5]
                        df_interim.iloc[:, 1] = np.select(conditions_statut, choix_statut, default=0)
                        df_interim.iloc[:, 2] = np.select(conditions, choix, default=0)
                        self.df_sivic = pd.concat([self.df_sivic, df_interim], ignore_index=True)
                        print("Done: ",j,"/",m," à ", h,"h")

    def load_2(self):
        paths = sorted(Path(self.EXPORTS_PATH).iterdir(), key=os.path.getmtime)

        for f in paths:
            df_interim = pd.read_excel(self.EXPORTS_PATH+f.name,skiprows=2)
            datetime_str = f.name[13:21]
            j=datetime_str[0:2]

            m=datetime_str[2:4]
            h=17
            df_interim = df_interim[
                ['Numéro SINUS', 'SOMATIQUE\nStatut', "SOMATIQUE\nType d'hospitalisation", "SOMATIQUE\nDépartement"]]
            df_interim = df_interim.rename(
                columns={'Numéro SINUS': 'Patient', 'SOMATIQUE\nStatut': 'Statut_{}{}2020_{}h'.format(j, m, h),
                         "SOMATIQUE\nType d'hospitalisation": 'Hospit_{}{}2020_{}h'.format(j, m, h),
                         "SOMATIQUE\nDépartement": "dpt"})

            conditions = [
                df_interim.iloc[:, 2] == self.condition_hospit[3],
                df_interim.iloc[:, 2] == self.condition_hospit[1],
                df_interim.iloc[:, 2] == self.condition_hospit[0],
                df_interim.iloc[:, 2] == self.condition_hospit[2],
                df_interim.iloc[:, 2] == self.condition_hospit[4]
            ]
            choix = [1, 2, 3, 4, 5]

            conditions_statut = [
                df_interim.iloc[:, 1] == self.condition_statut[1],
                df_interim.iloc[:, 1] == self.condition_statut[0],
                df_interim.iloc[:, 1] == self.condition_statut[2],
                df_interim.iloc[:, 1] == self.condition_statut[3],
                df_interim.iloc[:, 1] == self.condition_statut[4]
            ]
            choix_statut = [1, 2, 3, 4, 5]
            df_interim.iloc[:, 1] = np.select(conditions_statut, choix_statut, default=0)
            df_interim.iloc[:, 2] = np.select(conditions, choix, default=0)
            self.df_sivic = pd.concat([self.df_sivic, df_interim], ignore_index=True)
            print("Done: ", j, "/", m, " à ", h, "h")

    def get_date(self):
        paths = sorted(Path(self.EXPORTS_PATH).iterdir(), key=os.path.getmtime)

        for f in paths:
            datetime_str = f.name[13:21]
            j = datetime_str[0:2]

            m = datetime_str[2:4]
            h = 17
            # datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
            self.X += ['{}/{}'.format(j, m)]
        #for m in self.mois:
         #   for j in self.jour:
          #      for h in self.heure:
           #         file = pathlib.Path("./Data_Sivic/{}{}2020_{}h.xls".format(j,m,h))
            #        if file.exists():
             #           datetime_str = '{}/{}'.format(j,m)
              #          #datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
               #         self.X += [datetime_str]

    def get_last_csv(self):
        """
        Trouve le dernier export contenu dans le dossier data/exports_bruts
        :return: (path, date_export)
        """
        all=[]
        for f in os.listdir(self.CSV_PATH):
            all+=[(f, extract_path_date(self.CSV_PATH,f))]

        last = all[0]
        blast=None

        for p in all:
            if p[1] > last[1]:
                blast = last
                last = p

        return last

    def load_and_save(self):


        file = self.get_last_csv()[0]
        if self.TODAY.day !=extract_path_date(self.CSV_PATH,file).day:
            self.load_2()
            self.df_sivic.to_csv(self.CSV_PATH+self.TODAY.strftime('%d_%m')+".csv")
        else:
            self.df_sivic=pd.read_csv(self.CSV_PATH + self.TODAY.strftime('%d_%m')+".csv")
        #if not cond:
         #   self.load()
          #  self.df_sivic.to_csv("csv/{}{}2020_{}h.csv".format(self.jour_arret,mois[-1],heure[-1]))
        #else:
         #   self.df_sivic = pd.read_csv("csv/{}{}2020_{}h.csv".format(self.jour_arret, mois[-1], heure[-1]))


    def clean_dpt(self):
        df_sivic_dpt = self.df_sivic
        df_sivic_dpt = df_sivic_dpt.groupby(["Patient"], as_index=False).sum()
        df_sivic_dpt = df_sivic_dpt.iloc[:, 2:].astype(int)

        self.df_sivic = self.df_sivic[self.df_sivic["dpt"].isin(self.Départements)]
        self.df_sivic=self.df_sivic.groupby(["Patient"], as_index=False).sum()

        self.df_sivic=self.df_sivic.iloc[:,2:].astype(int)
        self.columns=self.df_sivic.columns

    def create_indicators(self):
        #Ceux qui sont mort en réa
        for i in range(2,len(self.columns)-self.new_columns,2):
            title=self.columns[i]
            title_bis=self.columns[i-1]
            title2='Rea_'+title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 1.0) & (self.df_sivic[title_bis] == 1.0), 1, 0)

        #Ceux qui sont mort en HC
        for i in range(2,len(self.columns)-self.new_columns,2):
            title=self.columns[i]
            title_bis=self.columns[i-1]
            title2='Autres_'+title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 1.0) & (self.df_sivic[title_bis] == 2.0), 1, 0)

        #Ceux qui sont mort en SSR
        for i in range(2,len(self.columns)-self.new_columns,2):
            title=self.columns[i]
            title_bis=self.columns[i-1]
            title2='Y'+title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 1.0) & (self.df_sivic[title_bis] == 4.0), 1, 0)

        #Ceux qui sont mort en psy
        for i in range(2,len(self.columns)-self.new_columns,2):
            title=self.columns[i]
            title_bis=self.columns[i-1]
            title2='Psy_'+title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 1.0) & (self.df_sivic[title_bis] == 5.0), 1, 0)


        #Les nouveaux morts
        for i in range(0,len(self.columns)-2-self.new_columns,2):
            title=self.columns[i]
            title_bis=self.columns[i+2]
            title2='Nvx_'+title
            self.df_sivic[title2] = np.where((self.df_sivic[title] != 1.0) & (self.df_sivic[title_bis] == 1.0), 1, 0)

        #entrée en réa
        for i in range(2,len(self.columns)-1,2):
            title=self.columns[i+1]
            title_bis=self.columns[i-1]
            title2='Entrée_réa'+title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 1.0) & (self.df_sivic[title_bis] != 1.0), 1, 0)

        #entrée en réa depuis SU
        for i in range(0,len(self.columns)-3-self.new_columns,2):
            title=self.columns[i+3]
            title_bis=self.columns[i]
            title2='Entrée_réa_SU'+title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 1.0) & (self.df_sivic[title_bis] == 4.0), 1, 0)

        #entrée en réa depuis HC
        for i in range(2,len(self.columns)-self.new_columns,2):
            title=self.columns[i+1]
            print(title)
            title_bis=self.columns[i-1]
            title2='Entrée_réa_HC'+title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 1.0) & ((self.df_sivic[title_bis] == 2.0)), 1, 0)

        #entrée en réa depuis SSR
        for i in range(2,len(self.columns)-self.new_columns,2):
            title=self.columns[i+1]
            title_bis=self.columns[i-1]
            title2='Entrée_réa_SSR'+title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 1.0) & (self.df_sivic[title_bis] == 4.0), 1, 0)

        # entrée en réa depuis NR
        for i in range(2, len(self.columns) - self.new_columns, 2):
            title = self.columns[i + 1]
            title_bis_2 =self.columns[i-2]
            title_bis = self.columns[i - 1]
            title2 = 'Entrée_réa_NR' + title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 1.0) & (self.df_sivic[title_bis] == 3.0)&self.df_sivic[title_bis_2] == 2.0, 1,0)

        #Sortie de réa
        for i in range(2,len(self.columns)-self.new_columns,2):
            title=self.columns[i+1]
            title_bis=self.columns[i-1]
            title2='Sortie_réa'+title
            self.df_sivic[title2] = np.where((self.df_sivic[title] != 1.0) & (self.df_sivic[title_bis] == 1.0), 1, 0)

        #Sortie de réa_décès
        for i in range(2,len(self.columns)-self.new_columns,2):
            title=self.columns[i]
            title_bis=self.columns[i-1]
            title2='Sortie_réa_dc'+title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 1.0) & (self.df_sivic[title_bis] == 1.0), 1, 0)

        #Sortie de réa_HC
        for i in range(2,len(self.columns)-self.new_columns,2):
            title=self.columns[i+1]
            title_bis=self.columns[i-1]
            title2='Sortie_réa_HC'+title
            self.df_sivic[title2] = np.where(((self.df_sivic[title] == 2.0)) & (self.df_sivic[title_bis] == 1.0), 1, 0)

        #Sortie de réa_SSR
        for i in range(2,len(self.columns)-self.new_columns,2):
            title=self.columns[i+1]
            title_bis=self.columns[i-1]
            title2='Sortie_réa_SSR'+title
            self.df_sivic[title2] = np.where(((self.df_sivic[title] == 4.0)) & (self.df_sivic[title_bis] == 1.0), 1, 0)

        # Sortie de réa_NR
        for i in range(2, len(self.columns) - self.new_columns, 2):
            title = self.columns[i + 1]
            title_bis_2=self.columns[i]
            title_bis = self.columns[i - 1]
            title2 = 'Sortie_réa_NR' + title
            self.df_sivic[title2] = np.where(((self.df_sivic[title] == 3.0)&self.df_sivic[title_bis_2] == 2.0) & (self.df_sivic[title_bis] == 1.0), 1,0)

        #Sortie de Retour à domicile
        for i in range(2,len(self.columns)-self.new_columns,2):
            title=self.columns[i]
            title_bis=self.columns[i-1]
            print(title)
            print(title_bis)
            title2='Sortie_réa_RAD'+title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 5.0) & (self.df_sivic[title_bis] == 1.0), 1, 0)

        # entrée en SSR
        for i in range(2, len(self.columns) - self.new_columns, 2):
            title = self.columns[i + 1]
            title_bis = self.columns[i - 1]
            title2 = 'Entrée_SSR' + title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 4.0) & (self.df_sivic[title_bis] != 4.0), 1, 0)

        # entrée en SSR depuis SU
        for i in range(0, len(self.columns) - 3 - self.new_columns, 2):
            title = self.columns[i + 3]
            title_bis = self.columns[i]
            title2 = 'Entrée_SSR_SU' + title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 4.0) & (self.df_sivic[title_bis] == 4.0), 1, 0)

        # entrée en SSR depuis HC
        for i in range(2, len(self.columns) -self.new_columns, 2):
            title = self.columns[i + 1]
            title_bis = self.columns[i - 1]
            title2 = 'Entrée_SSR_HC' + title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 4.0) & ((self.df_sivic[title_bis] == 2.0)), 1, 0)

        # entrée en SSR depuis réa
        for i in range(2, len(self.columns) - self.new_columns, 2):
            title = self.columns[i + 1]
            title_bis = self.columns[i - 1]
            title2 = 'Entrée_SSR_réa' + title
            self.df_sivic[title2] = np.where(( self.df_sivic[title] == 4.0) & ( self.df_sivic[title_bis] == 1.0), 1, 0)

        # entrée en SSR depuis NR
        for i in range(2, len(self.columns) - self.new_columns, 2):
            title = self.columns[i + 1]
            title_bis_2=self.columns[i-2]
            title_bis = self.columns[i - 1]
            title2 = 'Entrée_SSR_NR' + title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 3.0) & (self.df_sivic[title_bis] == 1.0)&self.df_sivic[title_bis_2] == 2.0, 1,
                                                 0)

        # Sortie de SSR
        for i in range(2, len(self.columns) - self.new_columns, 2):
            title = self.columns[i + 1]
            title_bis = self.columns[i - 1]
            title2 = 'Sortie_SSR' + title
            self.df_sivic[title2] = np.where(( self.df_sivic[title] != 4.0) & ( self.df_sivic[title_bis] == 4.0), 1, 0)

        # Sortie de SSR_décès
        for i in range(2, len(self.columns) - self.new_columns, 2):
            title = self.columns[i]
            title_bis = self.columns[i - 1]
            title2 = 'Sortie_SSR_dc' + title
            self.df_sivic[title2] = np.where(( self.df_sivic[title] == 1.0) & ( self.df_sivic[title_bis] == 4.0), 1, 0)

        # Sortie de SSR_HC
        for i in range(2, len(self.columns) - self.new_columns, 2):
            title = self.columns[i + 1]
            title_bis = self.columns[i - 1]
            title2 = 'Sortie_SSR_HC' + title
            self.df_sivic[title2] = np.where(((self.df_sivic[title] == 2.0)) & (self.df_sivic[title_bis] == 4.0), 1, 0)

        # Sortie de SSR réa
        for i in range(2, len(self.columns) - self.new_columns, 2):
            title = self.columns[i + 1]
            title_bis = self.columns[i - 1]
            title2 = 'Sortie_SSR_réa' + title
            self.df_sivic[title2] = np.where(((self.df_sivic[title] == 1.0)) & (self.df_sivic[title_bis] == 4.0), 1, 0)

        # Sortie de SSR NR
        for i in range(2, len(self.columns) - self.new_columns, 2):
            title = self.columns[i + 1]
            title_bis_2=self.columns[i]
            title_bis = self.columns[i - 1]
            title2 = 'Sortie_SSR_NR' + title
            self.df_sivic[title2] = np.where(((self.df_sivic[title] == 3.0)) & (self.df_sivic[title_bis] == 4.0)& (self.df_sivic[title_bis_2] == 2.0), 1,
                                                 0)


        # Sortie de Retour à domicile
        for i in range(2, len(self.columns) - self.new_columns, 2):
            title = self.columns[i]
            title_bis = self.columns[i - 1]
            title2 = 'Sortie_SSR_RAD' + title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 5.0) & (self.df_sivic[title_bis] == 4.0), 1, 0)

        # entrée en HC
        for i in range(2, len(self.columns)-self.new_columns, 2):
            title = self.columns[i + 1]
            title_bis = self.columns[i - 1]
            title2 = 'Entrée_HC' + title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 2.0) & (self.df_sivic[title_bis] != 2.0), 1, 0)

        # entrée en HC depuis SU
        for i in range(0, len(self.columns) - 3 - self.new_columns, 2):
            title = self.columns[i + 3]
            title_bis = self.columns[i]
            title2 = 'Entrée_HC_SU' + title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 2.0) & (self.df_sivic[title_bis] == 4.0), 1, 0)

        # entrée en HC depuis réa
        for i in range(2, len(self.columns) - self.new_columns, 2):
            title = self.columns[i + 1]
            title_bis = self.columns[i - 1]
            title2 = 'Entrée_HC_réa' + title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 2.0) & ((self.df_sivic[title_bis] == 1.0)), 1, 0)

        # entrée en HC depuis SSR
        for i in range(2, len(self.columns) - self.new_columns, 2):
            title = self.columns[i + 1]
            title_bis = self.columns[i - 1]
            title2 = 'Entrée_HC_SSR' + title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 2.0) & (self.df_sivic[title_bis] == 4.0), 1, 0)

        # entrée en HC depuis NR
        for i in range(2, len(self.columns) - self.new_columns, 2):
            title = self.columns[i + 1]
            title_bis_2=self.columns[i-2]
            title_bis = self.columns[i - 1]
            title2 = 'Entrée_HC_NR' + title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 2.0) & (self.df_sivic[title_bis] == 3.0)& (self.df_sivic[title_bis_2] == 2.0), 1,
                                                 0)

        # Sortie de HC
        for i in range(2, len(self.columns) - self.new_columns, 2):
            title = self.columns[i + 1]
            title_bis = self.columns[i - 1]
            title2 = 'Sortie_HC' + title
            self.df_sivic[title2] = np.where((self.df_sivic[title] != 2.0) & (self.df_sivic[title_bis] == 2.0), 1, 0)

        # Sortie de HC_décès
        for i in range(2, len(self.columns) - self.new_columns, 2):
            title = self.columns[i]
            title_bis = self.columns[i - 1]
            title2 = 'Sortie_HC_dc' + title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 1.0) & (self.df_sivic[title_bis] == 2.0), 1, 0)

        # Sortie de_HC vers réa
        for i in range(2, len(self.columns) - self.new_columns, 2):
            title = self.columns[i + 1]
            title_bis = self.columns[i - 1]
            title2 = 'Sortie_HC_réa' + title
            self.df_sivic[title2] = np.where(((self.df_sivic[title] == 1.0)) & (self.df_sivic[title_bis] == 2.0), 1, 0)

        # Sortie de HC vers SSR
        for i in range(2, len(self.columns) - self.new_columns, 2):
            title = self.columns[i + 1]
            title_bis = self.columns[i - 1]
            title2 = 'Sortie_HC_SSR' + title
            self.df_sivic[title2] = np.where(((self.df_sivic[title] == 4.0)) & (self.df_sivic[title_bis] == 2.0), 1, 0)

        # Sortie de HC vers NR
        for i in range(2, len(self.columns) - self.new_columns, 2):
            title = self.columns[i + 1]
            title_bis_2 = self.columns[i]
            title_bis = self.columns[i - 1]
            title2 = 'Sortie_HC_NR' + title
            self.df_sivic[title2] = np.where(((self.df_sivic[title] == 3.0)) & (self.df_sivic[title_bis] == 2.0) & (self.df_sivic[title_bis_2] == 2.0), 1,
                                                 0)

        # Sortie de Retour à domicile
        for i in range(2, len(self.columns) - self.new_columns, 2):
            title = self.columns[i]
            title_bis = self.columns[i - 1]
            title2 = 'Sortie_HC_RAD' + title
            self.df_sivic[title2] = np.where((self.df_sivic[title] == 5.0) & (self.df_sivic[title_bis] == 2.0), 1, 0)

        self.df_sivic = self.df_sivic.sum()

    def create_data(self):

        for i in self.df_sivic.index:

            if i[:2]=="St":
                self.status+=[self.df_sivic[i]]
            if i[0] == 'H':
                self.hospit += [self.df_sivic[i]]
            if i[0] == 'R':
                self.rea_nouveaux += [self.df_sivic[i]]
            if i[0] == 'N':
                self.nouveau_morts += [self.df_sivic[i]]
            if i[0] == 'A':
                self.hc_nouveaux += [self.df_sivic[i]]
            if i[0] == 'Y':
                self.SSR += [self.df_sivic[i]]
            if i[0] == 'P':
                self.psy += [self.df_sivic[i]]
            if i[:11]=='Entrée_réaH':
                self.entree_rea += [self.df_sivic[i]]
            if i[:13]=='Entrée_réa_HC':
                self.entree_rea_HC += [self.df_sivic[i]]
            if i[:13]=='Entrée_réa_SU':
                self.entree_rea_SU += [self.df_sivic[i]]
            if i[:14]=='Entrée_réa_SSR':
                self.entree_rea_SSR += [self.df_sivic[i]]
            if i[:11]=='Sortie_réaH':
                self.sortie_rea += [self.df_sivic[i]]
            if i[:13]=='Sortie_réa_HC':
                self.sortie_rea_HC += [self.df_sivic[i]]
            if i[:13]=='Sortie_réa_dc':
                self.sortie_rea_dc += [self.df_sivic[i]]
            if i[:14]=='Sortie_réa_SSR':
                self.sortie_rea_SSR += [self.df_sivic[i]]
            if i[:14]=='Sortie_réa_RAD':
                self.sortie_rea_RAD += [self.df_sivic[i]]
            if i[:13]=='Entrée_réa_NR':
                self.entree_rea_NR += [self.df_sivic[i]]
            if i[:13]=='Sortie_réa_NR':
                self.sortie_rea_NR += [self.df_sivic[i]]

            if i[:10] == 'Entrée_HCH':
                self.entree_HC += [self.df_sivic[i]]
            if i[:13] == 'Entrée_HC_réa':
                self.entree_HC_rea += [self.df_sivic[i]]
            if i[:12] == 'Entrée_HC_SU':
                self.entree_HC_SU += [self.df_sivic[i]]
            if i[:13] == 'Entrée_HC_SSR':
                self.entree_HC_SSR += [self.df_sivic[i]]
            if i[:10] == 'Sortie_HCH':
                self.sortie_HC += [self.df_sivic[i]]
            if i[:13] == 'Sortie_HC_réa':
                self.sortie_HC_rea += [self.df_sivic[i]]
            if i[:12] == 'Sortie_HC_dc':
                self.sortie_HC_dc += [self.df_sivic[i]]
            if i[:13] == 'Sortie_HC_SSR':
                self.sortie_HC_SSR += [self.df_sivic[i]]
            if i[:13] == 'Sortie_HC_RAD':
                self.sortie_HC_RAD += [self.df_sivic[i]]
            if i[:12] == 'Entrée_HC_NR':
                self.entree_HC_NR += [self.df_sivic[i]]
            if i[:12] == 'Sortie_HC_NR':
                self.sortie_HC_NR += [self.df_sivic[i]]

            if i[:11] == 'Entrée_SSRH':
                self.entree_SSR += [self.df_sivic[i]]
            if i[:13] == 'Entrée_SSR_HC':
                self.entree_SSR_HC += [self.df_sivic[i]]
            if i[:13] == 'Entrée_SSR_SU':
                self.entree_SSR_SU += [self.df_sivic[i]]
            if i[:14] == 'Entrée_SSR_réa':
                self.entree_SSR_rea += [self.df_sivic[i]]
            if i[:11] == 'Sortie_SSRH':
                self.sortie_SSR += [self.df_sivic[i]]
            if i[:13] == 'Sortie_SSR_HC':
                self.sortie_SSR_HC += [self.df_sivic[i]]
            if i[:13] == 'Sortie_SSR_dc':
                self.sortie_SSR_dc += [self.df_sivic[i]]
            if i[:14] == 'Sortie_SSR_réa':
                self.sortie_SSR_rea += [self.df_sivic[i]]
            if i[:14] == 'Sortie_SSR_RAD':
                self.sortie_SSR_RAD += [self.df_sivic[i]]
            if i[:13] == 'Entrée_SSR_NR':
                self.entree_SSR_NR += [self.df_sivic[i]]
            if i[:13] == 'Sortie_SSR_NR':
                self.sortie_SSR_NR += [self.df_sivic[i]]

    def data_for_plots_rea_décès(self):

        self.data_dc={#'Nombre en réa':  hospit,
            'Nombre de nouveaux décès': self.nouveau_morts,
            #'Nombre de morts cumulé':self.status,
            'dont en réa': self.rea_nouveaux,
            'dont en HC': self.hc_nouveaux,
            'dont en psy': self.psy,
            'dont en SSR': self.SSR
            }
        self.data_rea={
        'Entrées en réa':self.entree_rea,
        'Sortie de réa': self.sortie_rea
            }

        self.data_entree_rea={'Entrées en réa':self.entree_rea,
        'dont depuis HC': self.entree_rea_HC,
        #'dont depuis SSR': self.entree_rea_SSR,
        'Autre modalité':np.add(self.entree_rea_SSR,np.add(self.entree_rea_SU,self.entree_rea_NR))
        #'dont depuis Soin aux urgences':self.entree_rea_SU,
        #'Non renseigné': self.entree_rea_NR
             }

        self.data_sortie_rea={
        'Sorties de réa': self.sortie_rea,
        'dont décès': self.sortie_rea_dc,
        'dont vers HC':self.sortie_rea_HC,
        'dont RAD': self.sortie_rea_RAD,
        'Autre modalité': np.add(self.sortie_rea_SSR,self.sortie_rea_NR)

             }

    def data_for_plots_SSR(self):
        self.data_SSR = {
            'Entrées en SSR': self.entree_SSR,
            'Sortie de SSR': self.sortie_SSR
        }

        self.data_entree_SSR = {'Entrées en SSR': self.entree_SSR,
                       'dont depuis HC': self.entree_SSR_HC,
                       'Autre modalité': np.add(self.entree_SSR_rea,np.add(self.entree_SSR_SU,self.entree_SSR_NR))
                       }

        self.data_sortie_SSR = {
            'Sorties de SSR': self.sortie_SSR,
            'dont décès': self.sortie_SSR_dc,
            'dont vers HC': self.sortie_SSR_HC,
            'dont RAD': self.sortie_SSR_RAD,
            'Autre modalité': np.add(self.sortie_SSR_rea,self.sortie_SSR_NR)
        }



    def data_for_plots_HC(self):
        self.data_HC = {
            'Entrées en HC': self.entree_HC,
            'Sortie de HC': self.sortie_HC
        }

        self.data_entree_HC = {'Entrées en HC': self.entree_HC,
                       #'dont depuis SSR': self.entree_HC_SSR,
                       'dont depuis rea': self.entree_HC_rea,
                        'Autre modalité':np.add(self.entree_HC_SSR,np.add(self.entree_HC_SU, self.entree_HC_NR))
                       #'dont depuis Soin aux urgences': self.entree_HC_SU,
                               #'Non renseigné': self.entree_HC_NR
                       }

        self.data_sortie_HC = {
            'Sorties de HC': self.sortie_HC,
            'dont décès': self.sortie_HC_dc,
            'dont vers réa': self.sortie_HC_rea,
            'dont RAD': self.sortie_HC_RAD,
            'dont vers SSR': self.sortie_HC_SSR,
            'Non renseigné': self.sortie_HC_NR
        }


    def compute(self):
        self.load_and_save()
        self.get_date()
        self.clean_dpt()
        self.create_indicators()
        self.create_data()
        print("X",len(self.X))
        self.data_for_plots_rea_décès()
        self.data_for_plots_SSR()
        self.data_for_plots_HC()

    def plot_dc(self):

        df_final=pd.DataFrame(self.data_dc)
        print(len(df_final))
        df_final["date"]=self.X
        df_final=df_final.set_index("date")
        #my_colors = [(0, 0, 1), (0, 1, 0)] * len(X)

        ax=df_final.iloc[2:,:].plot.bar()
        for p in ax.patches:
            b = p.get_bbox()
            val = "{}".format(int(b.y1) + int(b.y0))
            ax.annotate(val, ((b.x0 + b.x1)/2 , int(b.y1)), ha='center', va='bottom')
        plt.xlabel('Date',rotation=0)
        plt.savefig('figures/plot_décès.png')
        plt.show()

    def plot_entree_sorties(self,name, data):
        df_final=pd.DataFrame(data)
        df_final["date"]=self.X
        df_final=df_final.set_index("date")
        #my_colors = [(0, 0, 1), (0, 1, 0)] * len(X)

        ax=df_final.iloc[2:,:].plot.bar(color=['blue','firebrick'])
        for p in ax.patches:
            b = p.get_bbox()
            val = "{}".format(int(b.y1) + int(b.y0))
            ax.annotate(val, ((b.x0 + b.x1)/2 , int(b.y1)), ha='center', va='bottom')
        plt.xlabel('Date',rotation=0)
        plt.savefig('figures/plot_{}.png'.format(name))
        plt.show()

    def plot_sortie(self, name, data):
        df_final=pd.DataFrame(data)
        df_final["date"]=self.X
        df_final=df_final.set_index("date")

        ax=df_final.iloc[2:,:].plot.bar(color=['firebrick','slategray','steelblue', 'gold','orange','black'])

        for p in ax.patches:
            b = p.get_bbox()
            val = "{}".format(int(b.y1) + int(b.y0))
            ax.annotate(val, ((b.x0 + b.x1)/2 , int(b.y1)),ha='center', va='bottom')
        plt.xlabel('Date',rotation=0)
        plt.savefig('figures/plot_{}_sortie.png'.format(name))
        plt.show()

    def plot_entree(self, name,data):
        df_final=pd.DataFrame(data)
        df_final["date"]=self.X
        df_final=df_final.set_index("date")
        ax=df_final.iloc[2:,:].plot.bar(color=['blue', 'deepskyblue','rebeccapurple', 'crimson','black'])
        for p in ax.patches:
            b = p.get_bbox()
            val = "{}".format(int(b.y1) + int(b.y0))
            ax.annotate(val, ((b.x0 + b.x1)/2 , int(b.y1)),  va='bottom')
        plt.xlabel('Date',rotation=0)
        plt.savefig('figures/plot_{}_entree.png'.format(name))
        plt.show()

    def plot_rea(self):
        self.plot_entree_sorties("Réa", self.data_rea)
        self.plot_entree("Réa",self.data_entree_rea)
        self.plot_sortie("Réa", self.data_sortie_rea)

    def plot_HC(self):
        self.plot_entree_sorties("HC", self.data_HC)
        self.plot_entree("HC",self.data_entree_HC)
        self.plot_sortie("HC", self.data_sortie_HC)

    def plot_SSR(self):
        self.plot_entree_sorties("SSR", self.data_SSR)
        self.plot_entree("SSR",self.data_entree_SSR)
        self.plot_sortie("SSR", self.data_sortie_SSR)

    def write_excel(self,name, data, data_entree, data_sortie):

        df_final=pd.DataFrame(data)
        df_final["date"]=self.X
        df_final=df_final.set_index("date")
        df_final_1=pd.DataFrame(data_entree)
        df_final_1["date"]=self.X
        df_final_1=df_final_1.set_index("date")
        df_final_2=pd.DataFrame(data_sortie)
        df_final_2["date"]=self.X
        df_final_2=df_final_2.set_index("date")

        writer = pd.ExcelWriter('excel/{}.xlsx'.format(name), engine='xlsxwriter')
        df_final.to_excel(writer, sheet_name='Entree_sorties')
        df_final_1.to_excel(writer, sheet_name='Detail entrees')
        df_final_2.to_excel(writer, sheet_name='Detail sorties')
        df_final.to_csv('excel/{}.csv'.format(name+"_entree_sorties"))
        df_final_1.to_csv('excel/{}.csv'.format(name+"_detail entrees"))
        df_final_2.to_csv('excel/{}.csv'.format(name+"_detail sorties"))
        writer.save()

    def write_rea(self):
        self.write_excel("Réa", self.data_rea, self.data_entree_rea, self.data_sortie_rea)

    def write_SSR(self):
        self.write_excel("SSR", self.data_SSR, self.data_entree_SSR, self.data_sortie_SSR)

    def write_HC(self):
        self.write_excel("HC", self.data_HC, self.data_entree_HC, self.data_sortie_HC)


jour=[25,27,28,29,30,31,'01','02','03','04','05','06','07','08','09','10','11','12']
heure=[17]
mois=['03','04']


#cond = pathlib.Path("{}{}2020_{}h.csv".format(jour[-1], mois[-1], heure[-1])).exists()
#test = False

chemin=Chemin_patient(jour, mois, heure)
chemin.compute()

chemin.write_HC()
chemin.write_rea()
chemin.write_SSR()

#chemin.plot_dc()
#chemin.plot_rea()
#chemin.plot_HC()
#chemin.plot_SSR()





