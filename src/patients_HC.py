import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pathlib
import matplotlib._color_data as mcd
import matplotlib.patches as mpatch



jour=[25,27,28,29,30,31,'01','02','03','04','05']
heure=[17]
mois=['03','04']
Départements=["Essonne (91)",
"Hauts-de-Seine (92)",
"Paris (75)",
"Seine-et-Marne (77)",
"Seine-Saint-Denis (93)",
"Val-de-Marne (94)",
"Val-d'Oise (95)",
"Yvelines (78)"
]


condition_statut=["-", "Décès", "Hospitalisation", "Soins aux urgences", "Retour à domicile"]
condition_hospit=["-", "Hospitalisation conventionnelle", "Hospitalisation en SSR", "Hospitalisation réanimatoire (réa ou SI)", "Hospitalisation psychiatrique"]


cond=pathlib.Path("{}{}2020_{}h.csv".format(jour[-1],mois[-1],heure[-1])).exists()
test=False

def load(mois, jour, heure, condition_statut,condition_hospit):
    df_sivic = pd.DataFrame()
    print("loading")
    for m in mois:
        for j in jour:
            for h in heure:
                file = pathlib.Path("./Data_Sivic/{}{}2020_{}h.xls".format(j,m,h))

                if file.exists():


                    df_interim = pd.read_excel("./Data_Sivic/{}{}2020_{}h.xls".format(j,m, h))
                    df_interim=df_interim[['Numéro SINUS','SOMATIQUE\nStatut',"SOMATIQUE\nType d'hospitalisation","SOMATIQUE\nDépartement"]]
                    df_interim=df_interim.rename(columns={'Numéro SINUS': 'Patient', 'SOMATIQUE\nStatut': 'Statut_{}{}2020_{}h'.format(j,m,h),"SOMATIQUE\nType d'hospitalisation":'Hospit_{}{}2020_{}h'.format(j,m,h), "SOMATIQUE\nDépartement":"dpt"})

                    conditions = [
                    df_interim.iloc[:, 2] == condition_hospit[3],
                    df_interim.iloc[:, 2] == condition_hospit[1],
                    df_interim.iloc[:, 2] == condition_hospit[0],
                    df_interim.iloc[:, 2] == condition_hospit[2],
                    df_interim.iloc[:, 2] == condition_hospit[4]
                    ]
                    choix=[1,2,3,4,5]

                    conditions_statut = [
                        df_interim.iloc[:, 1] == condition_statut[1],
                        df_interim.iloc[:, 1] == condition_statut[0],
                        df_interim.iloc[:, 1] == condition_statut[2],
                        df_interim.iloc[:, 1] == condition_statut[3],
                        df_interim.iloc[:, 1] == condition_statut[4]
                    ]
                    choix_statut = [1, 2, 3, 4, 5]
                    df_interim.iloc[:, 1] = np.select(conditions_statut, choix_statut, default=0)
                    df_interim.iloc[:, 2] = np.select(conditions, choix, default=0)
                    df_sivic = pd.concat([df_sivic, df_interim], ignore_index=True)
            print("Done: ",j)

    return df_sivic



def get_date(mois, jour, heure):
    X=[]
    for m in mois:
        for j in jour:
            for h in heure:
                file = pathlib.Path("./Data_Sivic/{}{}2020_{}h.xls".format(j,m,h))
                if file.exists():
                    datetime_str = '{}/{} {}h'.format(j,m,h)
                    #datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
                    X += [datetime_str]
    return X

if not cond:
    df_sivic=load(mois, jour, heure, condition_statut,condition_hospit)
    df_sivic.to_csv("{}{}2020_{}h.csv".format(jour[-1],mois[-1],heure[-1]))

X=get_date(mois, jour, heure)
df_sivic=pd.read_csv("{}{}2020_{}h.csv".format(jour[-1],mois[-1],heure[-1]))
df_sivic_dpt=df_sivic
df_sivic=df_sivic[df_sivic["dpt"].isin(Départements)]

#df_sivic_dpt=df_sivic[["Patient","dpt"]]
#df_sivic=df_sivic.drop(["dpt"], axis=1)

#df_sivic=df_sivic.groupby(["Patient","dpt"], as_index=False).sum()
#df_dpt=df_sivic['dpt']
#df_sivic=df_sivic.iloc[:,3:].astype(int)
#df_sivic['dpt']=df_dpt
#columns=df_sivic.columns
#df_sivic=df_sivic[df_sivic["dpt"].isin(Départements)]

df_sivic_dpt=df_sivic_dpt.groupby(["Patient"], as_index=False).sum()
df_sivic=df_sivic.groupby(["Patient"], as_index=False).sum()
#df_sivic_dpt=df_sivic_dpt.groupby(["Patient","dpt"])

df_sivic_dpt=df_sivic_dpt.iloc[:,2:].astype(int)

df_sivic=df_sivic.iloc[:,2:].astype(int)
columns=df_sivic.columns

#nombre de nouvelles colonnes: dpt, etc
new_columns=0


#entrée en HC
for i in range(2,len(columns)-1,2):
    title=columns[i+1]
    title_bis=columns[i-1]
    title2='Entrée_réa'+title
    df_sivic[title2] = np.where((df_sivic[title] == 2.0) & (df_sivic[title_bis] != 2.0), 1, 0)

#entrée en HC depuis SU
for i in range(0,len(columns)-3-new_columns,2):
    title=columns[i+3]
    title_bis=columns[i]
    title2='Entrée_réa_SU'+title
    df_sivic[title2] = np.where((df_sivic[title] == 2.0) & (df_sivic[title_bis] == 4.0), 1, 0)

#entrée en HC depuis réa
for i in range(2,len(columns)-new_columns,2):
    title=columns[i+1]
    title_bis=columns[i-1]
    title2='Entrée_réa_HC'+title
    df_sivic[title2] = np.where((df_sivic[title] == 2.0) & ((df_sivic[title_bis] == 1.0)), 1, 0)

#entrée en HC depuis SSR
for i in range(2,len(columns)-new_columns,2):
    title=columns[i+1]
    title_bis=columns[i-1]
    title2='Entrée_réa_SSR'+title
    df_sivic[title2] = np.where((df_sivic[title] == 2.0) & (df_sivic[title_bis] == 4.0), 1, 0)

#Sortie de HC
for i in range(2,len(columns)-new_columns,2):
    title=columns[i+1]
    title_bis=columns[i-1]
    title2='Sortie_réa'+title
    df_sivic[title2] = np.where((df_sivic[title] != 2.0) & (df_sivic[title_bis] == 2.0), 1, 0)

#Sortie de HC_décès
for i in range(2,len(columns)-new_columns,2):
    title=columns[i]
    title_bis=columns[i-1]
    title2='Sortie_réa_dc'+title
    df_sivic[title2] = np.where((df_sivic[title] == 1.0) & (df_sivic[title_bis] == 2.0), 1, 0)

#Sortie de_HC vers réa
for i in range(2,len(columns)-new_columns,2):
    title=columns[i+1]
    title_bis=columns[i-1]
    title2='Sortie_réa_HC'+title
    df_sivic[title2] = np.where(((df_sivic[title] == 1.0)) & (df_sivic[title_bis] == 2.0), 1, 0)

#Sortie de HC vers SSR
for i in range(2,len(columns)-new_columns,2):
    title=columns[i+1]
    title_bis=columns[i-1]
    title2='Sortie_réa_SSR'+title
    df_sivic[title2] = np.where(((df_sivic[title] == 4.0)) & (df_sivic[title_bis] == 2.0), 1, 0)

#Sortie de Retour à domicile
for i in range(2,len(columns)-new_columns,2):
    title=columns[i]
    title_bis=columns[i-1]
    title2='Sortie_réa_RAD'+title
    df_sivic[title2] = np.where((df_sivic[title] == 5.0) & (df_sivic[title_bis] == 2.0), 1, 0)

df_sivic=df_sivic.sum()

hist=pd.DataFrame()
status=[]
hospit=[]


entree_HC=[0]
entree_HC_SSR=[0]
entree_HC_SU=[0]
entree_HC_rea=[0]

sortie_HC=[0]
sortie_HC_SSR=[0]
sortie_HC_dc=[0]
sortie_HC_rea=[0]
sortie_HC_RAD=[0]

psy=[0]

for i in df_sivic.index:

   if i[:2]=="St":
       status+=[df_sivic[i]]
   if i[0] == 'H':
       hospit += [df_sivic[i]]
   if i[:11]=='Entrée_réaH':
       entree_HC += [df_sivic[i]]
   if i[:13]=='Entrée_réa_HC':
       entree_HC_rea += [df_sivic[i]]
   if i[:13]=='Entrée_réa_SU':
       entree_HC_SU += [df_sivic[i]]
   if i[:14]=='Entrée_réa_SSR':
       entree_HC_SSR += [df_sivic[i]]
   if i[:11]=='Sortie_réaH':
       sortie_HC += [df_sivic[i]]
   if i[:13]=='Sortie_réa_HC':
       sortie_HC_rea += [df_sivic[i]]
   if i[:13]=='Sortie_réa_dc':
       sortie_HC_dc += [df_sivic[i]]
   if i[:14]=='Sortie_réa_SSR':
       sortie_HC_SSR += [df_sivic[i]]
   if i[:14]=='Sortie_réa_RAD':
       sortie_HC_RAD += [df_sivic[i]]



data_HC={
    'Entrées en HC':entree_HC,
    'Sortie de HC': sortie_HC
        }

data_entree={'Entrées en HC':entree_HC,
    'dont depuis SSR': entree_HC_SSR,
    'dont depuis rea': entree_HC_rea,
             'dont depuis Soin aux urgences':entree_HC_SU
             }

data_sortie={
    'Sorties de HC': sortie_HC,
    'dont décès': sortie_HC_dc,
    'dont vers réa':sortie_HC_rea,
    'dont RAD': sortie_HC_RAD,
    'dont vers SSR': sortie_HC_SSR
             }


def plot_HC(data_HC, X):
    df_final=pd.DataFrame(data_HC)
    df_final["date"]=X
    df_final=df_final.set_index("date")
    #my_colors = [(0, 0, 1), (0, 1, 0)] * len(X)

    ax=df_final.iloc[2:,:].plot.bar(color=['blue','firebrick'])
    for p in ax.patches:
        b = p.get_bbox()
        val = "{}".format(int(b.y1) + int(b.y0))
        ax.annotate(val, ((b.x0 + b.x1)/2 , int(b.y1)), ha='center', va='bottom')
    plt.xlabel('Date',rotation=0)
    plt.savefig('data/figures/plot_HC.png')
    plt.show()

def plot_HC_sortie(data_HC, X):
    df_final=pd.DataFrame(data_HC)
    df_final["date"]=X
    df_final=df_final.set_index("date")

    ax=df_final.iloc[2:,:].plot.bar(color=['firebrick','slategray','steelblue', 'gold','orange'])

    for p in ax.patches:
        b = p.get_bbox()
        val = "{}".format(int(b.y1) + int(b.y0))
        ax.annotate(val, ((b.x0 + b.x1)/2 , int(b.y1)), ha='center', va='bottom')
    plt.xlabel('Date',rotation=0)
    plt.savefig('data/figures/plot_HC_sortie.png')
    plt.show()

def plot_HC_entree(data_HC, X):
    df_final=pd.DataFrame(data_HC)
    df_final["date"]=X
    df_final=df_final.set_index("date")
    ax=df_final.iloc[2:,:].plot.bar(color=['blue', 'deepskyblue','rebeccapurple', 'crimson'])
    for p in ax.patches:
        b = p.get_bbox()
        val = "{}".format(int(b.y1) + int(b.y0))
        ax.annotate(val, ((b.x0 + b.x1)/2 , int(b.y1)), ha='center', va='bottom')
    plt.xlabel('Date',rotation=0)
    plt.savefig('data/figures/plot_HC_entree.png')
    plt.show()


plot_HC(data_HC, X)
plot_HC_entree(data_entree, X)
plot_HC_sortie(data_sortie, X)
