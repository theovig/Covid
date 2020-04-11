import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


jour=[27]
heure=[10,14,17]
df_sivic=pd.DataFrame()
X=[]
l=[]
for j in jour:
    for h in heure:
        datetime_str = '03/{}/20 {}:00:00'.format(j,h)

        datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
        X+=[datetime_object]
        df_interim=pd.read_excel("./Data_Sivic/{}032020_{}h.xls".format(j,h))
        df_interim['date']=datetime_object
        df_interim['Âge approximatif']=df_interim['Âge approximatif'].replace(regex={r'ans':'',r'mois':0,r'semaine':0,r'jour':0,r'>80':80,r'> 80':80,r'SEM':0,r'-':'',r'ANS':'',r'an':'',r'a':'',r'XX':'',r'NC':'',r'Age pproximtif':''})
        df_interim['Âge approximatif'] = df_interim['Âge approximatif'][df_interim['Âge approximatif']!= 'Age approximatif']
        df_sivic = pd.concat([df_sivic, df_interim], ignore_index=True)
        l+=[df_interim]


df_age=df_interim[['Âge approximatif',"SOMATIQUE\nType d'hospitalisation","date"]]
df_age["Âge approximatif"]=df_age[df_age['Âge approximatif']!= '']
df_age["Âge approximatif"]=df_age["Âge approximatif"].dropna().astype(int)

df_ped=df_age[df_age["Âge approximatif"<20]]

print(df_ped.count())
print(df_ped)

df_rea=df_age[df_age["SOMATIQUE\nType d'hospitalisation"] == "Hospitalisation réanimatoire (réa ou SI)"]
print(df_rea.mean())
print(df_rea.median())


df_HC=df_age[(df_age["SOMATIQUE\nType d'hospitalisation"] == "Hospitalisation conventionnelle") | (df_age["SOMATIQUE\nType d'hospitalisation"] == "Hospitalisation en SSR") | (df_age["SOMATIQUE\nType d'hospitalisation"] == "Hospitalisation psychiatrique")]

print(df_HC.mean())
print(df_HC.median())

print(df_interim[df_interim["SOMATIQUE\nStatut"]=="Décès"].count())
df_depart=df_interim[df_interim["SOMATIQUE\nStatut"]=="Décès"].groupby("SOMATIQUE\nDépartement").count()
print(df_depart)

df_ancien=l[0]

print(df_ancien[df_sivic["SOMATIQUE\nStatut"]=="Décès"].count())
df_depart2=df_ancien[df_ancien["SOMATIQUE\nStatut"]=="Décès"].groupby("SOMATIQUE\nDépartement").count()
print(df_depart2)