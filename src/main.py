from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

def rowgetDataText(tr, coltag='td'):  # td (data) or th (header)
    return [td.get_text(strip=True) for td in tr.find_all(coltag)]

def tableDataText(table):
    """Parses a html segment started with tag <table> followed
    by multiple <tr> (table rows) and inner <td> (table data) tags.
    It returns a list of rows with inner columns.
    Accepts only one <th> (table header/data) in the first row.
    """

    rows = []
    trs = table.find_all('tr')
    headerow = rowgetDataText(trs[0], 'th')
    if headerow: # if there is a header row include first
        trs = trs[1:]
    for tr in trs: # for every table row
        rows.append(rowgetDataText(tr, 'td') ) # data row
    return pd.DataFrame(rows, columns =headerow)

jour=[20,23,24,25,26]
X=[]
df_HC=pd.DataFrame()

df_rea=pd.DataFrame()

Nb_lits_en_rea=4941

for j in jour:
    datetime_str = '03/{}/20'.format(j)

    datetime_object = datetime.strptime(datetime_str, '%m/%d/%y')
    X+=[datetime_object]
    with open("./Data_html/res_SIVIC_region_idf_{}032020.html".format(j)) as fp:
        soup=BeautifulSoup(fp,features="html.parser")
        df_interim=tableDataText(soup.find(summary="Procedure Print: Table WORK.T_HC"))
        df_interim['date']=datetime_object
        df_bis=df_interim.rename(columns={"Nb de patients enHC au {}/03/2020".format(j): "Nb de patients en HC", "Nb nouveaux patients en HC entrele {}/03/2020 et le {}/03/2020".format(j,j-1): "Nb nouveaux patients en HC"})
        df_HC=pd.concat([df_HC, df_bis], ignore_index=True)

        df_interim2 = tableDataText(soup.find(summary="Procedure Print: Table WORK.T_REA"))
        df_interim2['date'] = datetime_object
        df_bis2 = df_interim2.rename(columns={"Nb de patients enréa au {}/03/2020".format(j): "Nb de patients en réa",
                                            "Nb nouveaux patients en réaentre le {}/03/2020 et le {}/03/2020".format(j,
                                                                                                                    j - 1): "Nb nouveaux patients en réa"})
        df_rea = pd.concat([df_rea, df_bis2], ignore_index=True)


jour2=[27,28]
heure=[10,17]
df_rea2=pd.DataFrame()
df_HC2=pd.DataFrame()

for j in jour2:
    for h in heure:
        datetime_str = '03/{}/20 {}:00:00'.format(j, h)

        datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
        X += [datetime_object]
        df_test=pd.read_excel("./Data_csv/{}032020_{}h.xlsx".format(j,h), dtype={"dpt":"str"})
        df_test['date'] = datetime_object

        df_rea2=pd.concat([df_rea2,df_test[["dpt", "Hospitalisation_reanimatoire","date"]]])
        df_HC2 = pd.concat([df_HC2, df_test[["dpt", "Hospitalisation_conventionnelle", "date"]]])

df_rea2["Hospitalisation_reanimatoire"]=df_rea2["Hospitalisation_reanimatoire"].astype(str)
df_HC2["Hospitalisation_conventionnelle"]=df_HC2["Hospitalisation_conventionnelle"].astype(str)
df_rea2=df_rea2.rename(columns={'Hospitalisation_reanimatoire': 'Nb de patients en réa', 'dpt': 'Département'})
df_HC2=df_HC2.rename(columns={'Hospitalisation_conventionnelle': 'Nb de patients en HC', 'dpt': 'Département'})
df_rea=pd.concat([df_rea[["Département","Nb de patients en réa","date"]],df_rea2], ignore_index=True)
df_HC=pd.concat([df_HC[["Département","Nb de patients en HC","date"]],df_HC2], ignore_index=True)



# Graphes

axes = plt.gca()
Y_region_rea=df_rea.loc[df_rea['Département'] == 'Région IdF']['Nb de patients en réa']

Y_75_rea=df_rea.loc[df_rea['Département'] == '75']['Nb de patients en réa'].astype(int)

Y_77_rea=df_rea.loc[df_rea['Département'] == '77']['Nb de patients en réa'].astype(int)
Y_78_rea=df_rea.loc[df_rea['Département'] == '78']['Nb de patients en réa'].astype(int)
Y_91_rea=df_rea.loc[df_rea['Département'] == '91']['Nb de patients en réa'].astype(int)
Y_92_rea=df_rea.loc[df_rea['Département'] == '92']['Nb de patients en réa'].astype(int)
Y_93_rea=df_rea.loc[df_rea['Département'] == '93']['Nb de patients en réa'].astype(int)
Y_94_rea=df_rea.loc[df_rea['Département'] == '94']['Nb de patients en réa'].astype(int)
Y_95_rea=df_rea.loc[df_rea['Département'] == '95']['Nb de patients en réa'].astype(int)


plt.scatter(X,Y_region_rea)

plt.title('Nombre de patients en réanimation en IdF')
#plt.axhline(y=Nb_lits_en_rea, color='red')
plt.savefig('rea_idf.png')
plt.show()
plt.gca().legend()
plt.plot(X, Y_75_rea, 'b--',label='75')
plt.plot(X, Y_77_rea, 'g--',label='77')
plt.plot(X, Y_78_rea, 'r--',label='78')
plt.plot(X, Y_91_rea, 'c--',label='91')
plt.plot(X, Y_92_rea, 'm--',label='92')
plt.plot(X, Y_93_rea, 'y--',label='93')
plt.plot(X, Y_94_rea, 'k--',label='94')
plt.plot(X, Y_95_rea, 'p--',label='95')
for i in range (50,450,50):
    plt.axhline(y=i, color='grey')
#plt.axhline(y=Nb_lits_en_rea, color='red')
plt.legend()
plt.title('Nombre de patients en réanimation par département')
plt.savefig('rea_dep.png')
plt.show()



Y_region_HC=df_HC.loc[df_HC['Département'] == 'Région IdF']['Nb de patients en HC']
Y_75_HC=df_HC.loc[df_HC['Département'] == '75']['Nb de patients en HC'].str.replace(' ', '').astype(int)
Y_77_HC=df_HC.loc[df_HC['Département'] == '77']['Nb de patients en HC'].astype(int)
Y_78_HC=df_HC.loc[df_HC['Département'] == '78']['Nb de patients en HC'].astype(int)
Y_91_HC=df_HC.loc[df_HC['Département'] == '91']['Nb de patients en HC'].astype(int)
Y_92_HC=df_HC.loc[df_HC['Département'] == '92']['Nb de patients en HC'].astype(int)
Y_93_HC=df_HC.loc[df_HC['Département'] == '93']['Nb de patients en HC'].astype(int)
Y_94_HC=df_HC.loc[df_HC['Département'] == '94']['Nb de patients en HC'].astype(int)
Y_95_HC=df_HC.loc[df_HC['Département'] == '95']['Nb de patients en HC'].astype(int)


plt.scatter(X,Y_region_HC)

plt.title('Nombre de patients en HC en IdF')
#plt.axhline(y=Nb_lits_en_rea, color='red')
axes.xaxis.set_ticks(range(1))
plt.savefig('HC_idf.png')
plt.show()

plt.gca().legend()
plt.plot(X, Y_75_HC, 'b--',label='75')
plt.plot(X, Y_77_HC, 'g--',label='77')
plt.plot(X, Y_78_HC, 'r--',label='78')
plt.plot(X, Y_91_HC, 'c--',label='91')
plt.plot(X, Y_92_HC, 'm--',label='92')
plt.plot(X, Y_93_HC, 'y--',label='93')
plt.plot(X, Y_94_HC, 'k--',label='94')
plt.plot(X, Y_95_HC, 'p--',label='95')

for i in range (100,1200,100):
    plt.axhline(y=i, color='grey')
#plt.axhline(y=Nb_lits_en_rea, color='red')
plt.legend()
plt.title('Nombre de patients en HC par département')
plt.savefig('HC_dep.png')
plt.show()