import requests
import pandas as pd
"""
Dette script henter vejstykker fra DAWA API baseret på en given kommunekode og gemmer resultaterne i en CSV-fil.
Kommunekoden kan være en enkelt kode eller flere koder adskilt af '|'.
Hvis kommunekoden er '0000', hentes alle vejstykker.

Variabler:
- kommunekode: Streng, der indeholder en eller flere kommunekoder adskilt af '|'.
- url: Streng, der indeholder API URL'en til at hente vejstykker.
- response: Response objekt fra requests biblioteket, der indeholder API svaret.
- vejstykker: Liste af vejstykker hentet fra API'et.
- vejnavne: Liste af vejnavne med tilhørende informationer.
- df: DataFrame, der indeholder de hentede vejnavne og deres informationer.

Output:
- CSV-fil 'd_vejnavn.csv', der indeholder de hentede vejnavne og deres informationer.
"""

kommunekode = '0665|0671' # Indtast kommunekode her, hvis 0000 så bliver alle vejstykker hentet
# der kan indtastes flere kommunekoder adskilt af |, f.eks. "0101|0147" for København og Frederiksberg
# Hent data fra DAWA
url = f"https://api.dataforsyningen.dk/vejstykker"
if kommunekode != '0000':
    url += f"?kommunekode={kommunekode}"

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
            'cvf_vejkode': f"{vej['kommune']['kode']}{vej['kode']}",
            'kommunekode': vej['kommune']['kode'],
            'kommunenavn': vej['kommune']['navn'],
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
df.to_csv('d_vejnavn.csv', index=False, encoding='utf-8', sep=';', quotechar='"', quoting=2)
