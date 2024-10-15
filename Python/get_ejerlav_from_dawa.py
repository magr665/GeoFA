import requests
import geopandas as gpd

"""
Dette script henter og behandler geodata for kommuner og ejerlav fra DAWA API'et.

Variabler:
- kommunekode: En streng, der indeholder kommunekoder adskilt af '|'. Hvis '0000', hentes alle ejerlav.

Output:
- En CSV-fil 'd_basis_ejerlav.csv' med ejerlav data og tilhørende kommunedata.
"""

kommunekode = "0665|0671"  # Indtast kommunekode her, hvis 0000 så bliver alle ejerlav hentet
# der kan indtastes flere kommunekoder adskilt af |, f.eks. "0101|0147"
# Get data from DAWA

url = "https://api.dataforsyningen.dk/kommuner"
if kommunekode != "0000":
    url += f"?kode={kommunekode}"
url += "&format=geojson&srid=25832"
response = requests.get(url)
kommuner = response.json()
srid = f"srid={kommuner['crs']['properties']['name'].split(':')[-1]}"
kommuner_gdf = gpd.GeoDataFrame.from_features(kommuner['features'])

ejerlav_lst = []
url = f"https://api.dataforsyningen.dk/ejerlav?srid=25832&format=geojson"
ejerlav_response = requests.get(url)
ejerlav_json = ejerlav_response.json()
ejerlav_gdf = gpd.GeoDataFrame.from_features(ejerlav_json['features'])
ejerlav_clipped = gpd.clip(ejerlav_gdf, kommuner_gdf)
# Create a GeoDataFrame from the visueltcenter_x and visueltcenter_y in ejerlav_clipped
ejerlav_points = gpd.GeoDataFrame(
    ejerlav_clipped,
    geometry=gpd.points_from_xy(ejerlav_clipped.visueltcenter_x, ejerlav_clipped.visueltcenter_y),
    crs=kommuner_gdf.crs
)

ejerlav_with_kommuner = gpd.sjoin(ejerlav_points, kommuner_gdf[['geometry', 'kode', 'navn']], how='left', predicate='within')
ejerlav_with_kommuner = ejerlav_with_kommuner[~ejerlav_with_kommuner['index_right'].isna()]
ejerlav_with_kommuner = ejerlav_with_kommuner.drop(columns='geometry').rename(columns={'kode_right': 'kommunekode', 'navn_right': 'kommunenavn', 'kode_left': 'kode'})
ejerlav_clipped = ejerlav_clipped.merge(ejerlav_with_kommuner[['kode', 'kommunekode', 'kommunenavn']], on='kode', how='left')
ejerlav_clipped = ejerlav_clipped[ejerlav_clipped['kommunekode'].notna()]
ejerlav_clipped.drop(columns=['visueltcenter_x', 'visueltcenter_y', 'geometry'], inplace=True)
ejerlav_clipped.rename(columns={'kode': 'ejerlavskode', 'navn': 'ejerlavsnavn'}, inplace=True)
ejerlav_clipped.to_csv('d_basis_ejerlav.csv', index=False, encoding='utf-8', sep=';', quoting=2, quotechar='"')