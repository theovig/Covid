"""
Definition de la classe EMSExport
"""

from exports_utils import *
from rapports_utils import *


class EMSExport :
    def __init__(self, file_name=None):
        """
        Constructeur de EMSExport
        :param file_name: Nom du fichier d'export brut à charger. Le dernier en date sera chargé si non précisé.
        """

        if file_name is None :
            self.df, self.df_es, self.df_bed, self.df_housses, self.date = load_last()
            #self.dfb, self.dateb =  load(get_before_last()[0])
            #self.df = pd.merge(self.df, self.dfb[["FINESS_GEO"]], on = "FINESS_GEO", how='inner' )
        #else :
            #self.df, self.df_es, self.df_bed, self.df_housses, self.date = load(file_name)

        self.gdf = None
        self.incators = None

    def get_gdf(self):
        """
        GeoDataframe de l'export. Il sera créé lors du premier appel de la fonction
        :return: GeoDataframe
        """
        if self.gdf is None :
            geom = [Point(x, y) for x, y in zip(self.df['X_RGF93'], self.df['Y_RGF93'])]
            self.gdf = gpd.GeoDataFrame(self.df, geometry=geom, crs="EPSG:2154")
            self.gdf = self.gdf.to_crs("EPSG:4326")  # Conversion du système Lambert 93 vers WGS84

        return self.gdf

    def save(self):
        """
        Sauvegarde en fichier excel (xlsx)
        :return:
        """
        name = self.date.strftime("%d%m%y %H%M%S") + ".xlsx"
        path = get_save_path(self.date)+"/"
        self.df.to_excel(path + name , index=False)

