## Indholdsfortegnelse
1. [d_basis](#d_basis)
2. [tabeller]
    1. [d_basis](#d_basis)
    2. [d_spec](#d_spec)
3. [Python](#Python)
4. [Installation](#installation)
5. [Brug](#brug)
6. [Bidrag](#bidrag)
7. [Licens](#licens)

## d_basis
`d_basis` indeholder alle `d_basis` tabeller, dog ikke `d_vejnavn` og `d_postnr`, disse skal laves med de to dertil udviklede Python scripts.

## d_spec
`d_spec` indeholder alle `d_####_??` tabeller til de forskellige temaer.

## Python
Indeholder diverse scripts til bl.a. at hente data fra DAWA api

## Installation
For at installere projektet, følg disse trin:
1. Klon repositoryet: `git clone https://github.com/magr665/GeoFA.git`
2. Naviger til projektmappen: `cd GeoFA`
3. Installer nødvendige afhængigheder: `pip install -r requirements.txt`

## Brug
For at bruge tabellerne:
1. Kør de relevante Python scripts for at generere `d_vejnavn` og `d_postnr` tabeller.
2. Naviger til de ønskede tabeller i `d_basis` og `d_spec` mapperne.

## Bidrag
Vi byder bidrag velkommen! For at bidrage til projektet, følg venligst disse trin:
1. Fork repositoryet.
2. Opret en ny branch: `git checkout -b feature/dit-feature-navn`
3. Commit dine ændringer: `git commit -m 'Tilføj feature'`
4. Push til branchen: `git push origin feature/dit-feature-navn`
5. Opret en pull request.

## Licens
Dette projekt er licenseret under MIT-licensen. Se [LICENSE](../LICENSE) filen for detaljer.
