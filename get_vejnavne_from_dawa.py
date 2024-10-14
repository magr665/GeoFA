import requests
import pandas as pd
"""
Dette script henter vejnavne fra Dataforsyningens API baseret på en given kommunekode og gemmer dem i en CSV-fil.
Moduler:
    requests: Håndterer HTTP-anmodninger for at hente data fra API'et.
    pandas: Bruges til at manipulere og analysere dataene.
Variabler:
    kommunekode (str): Kommunekoden for den ønskede kommune.
    url (str): URL til Dataforsyningens API med den specificerede kommunekode.
    response (requests.Response): HTTP-respons fra API'et.
    vejstykker (list): Liste over vejstykker hentet fra API'et.
    vejnavne (list): Liste over vejnavne og tilhørende data.
    df (pandas.DataFrame): DataFrame, der indeholder de behandlede vejnavne og tilhørende data.
Funktioner:
    Ingen funktioner defineret.
Arbejdsgang:
    1. Hent vejstykker fra Dataforsyningens API baseret på den angivne kommunekode.
    2. Ekstraher relevante data fra hvert vejstykke og opret en liste over vejnavne.
    3. Opret en pandas DataFrame fra listen over vejnavne.
    4. Tilføj en kolonne, der tæller forekomsten af hvert vejnavn.
    5. Hvis et vejnavn forekommer mere end én gang, tilføj postnumre til vejnavnet.
    6. Fjern tællekolonnen og sorter DataFrame efter vejnavn.
    7. Gem DataFrame som en CSV-fil med navnet 'd_vejnavne.csv'.
Output:
    En CSV-fil med vejnavne og tilhørende data, gemt som 'd_vejnavne.csv'.
"""

kommunekode = '0665' ########### indtal kommunekode her ###########
url = f"https://api.dataforsyningen.dk/vejstykker?kommunekode={kommunekode}"
response = requests.get(url)
vejstykker = response.json()

vejnavne = []
for vej in vejstykker:
    vejstykke = {
            'id': vej['id'],
            'vejkode': int(vej['kode']),
            'vejnavn': vej['navn'],
            'adresseringsnavn': vej['adresseringsnavn'],
            'vejkode0': vej['kode'],
            'cvf_vejkode': f"{int(kommunekode)}{vej['kode']}",
            'kommunekode': int(kommunekode),
            }
    postnumre = []
    for postnummer in vej['postnumre']:
        postnumre.append(f"{postnummer['nr']} {postnummer['navn']}")
    vejstykke['postnumre'] = ', '.join(postnumre)
    vejnavne.append(vejstykke)

df = pd.DataFrame(vejnavne)
df['vejnavn_count'] = df['vejnavn'].map(df['vejnavn'].value_counts())
df['vejnavn'] = df.apply(lambda row: f"{row['vejnavn']} ({row['postnumre']})" if row['vejnavn_count'] > 1 else row['vejnavn'], axis=1)
df.drop(columns=['vejnavn_count'], inplace=True)
df.sort_values(by='vejnavn', inplace=True)
df.to_csv('d_vejnavne.csv', index=False, encoding='utf-8', sep=';', quotechar='"', quoting=2)