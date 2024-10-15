import requests
import pandas as pd
"""
Denne script henter postnumre fra DAWA API baseret på en given kommunekode og gemmer dem i en CSV-fil.

Variabler:
- kommunekode: En streng, der indeholder kommunekoder adskilt af '|'. Hvis '0000', hentes alle postnumre.

Output:
- CSV-fil 'd_basis_postnr.csv', der indeholder de hentede postnumre og deres informationer.
"""

kommunekode = "0665|0671"  # Indtast kommunekode her, hvis 0000 så bliver alle postnumre hentet
# der kan indtastes flere kommunekoder adskilt af |, f.eks. "0665|0671" for Lemvig og Struer kommuner
# Get data from DAWA
url = "https://api.dataforsyningen.dk/postnumre"
if kommunekode != "0000":
    url += f"?kommunekode={kommunekode}"

response = requests.get(url)
postnumre = response.json()

# Extract relevant data
postnumre_data = []
for postnummer in postnumre:
    postnr = {
        "postnr": postnummer["nr"],
        "postnr_by": postnummer["navn"],
    }
    kommuner_data = []
    for kommune in postnummer["kommuner"]:
        kommuner_data.append(f"{kommune['kode']} {kommune['navn']}")
    postnr["kommuner"] = ", ".join(kommuner_data)

    postnumre_data.append(postnr)

# Create DataFrame
df = pd.DataFrame(postnumre_data)
df.sort_values(by="postnr_by", inplace=True)
df.to_csv("d_basis_postnr.csv", index=False, encoding="utf-8", sep=";", quotechar='"', quoting=2)