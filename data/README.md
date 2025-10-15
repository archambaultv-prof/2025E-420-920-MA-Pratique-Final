# Data Directory

Ce répertoire contient les fichiers CSV générés par le programme `weather-report` et utilisés par le programme `weather-analyzer`.

## Structure des fichiers

Les fichiers CSV générés ont le format suivant :

```csv
Date,Station,Temperature,Pressure
2025-03-15,StationA,18.5,1013.2
2025-06-22,StationC,25.3,1015.8
2025-12-01,StationB,5.2,1020.1
```

### Colonnes :
- **Date** : Date au format YYYY-MM-DD
- **Station** : Nom de la station météorologique (StationA, StationB, etc.)
- **Temperature** : Température en degrés Celsius
- **Pressure** : Pression atmosphérique en hPa (hectopascals)

## Comment générer les fichiers

Depuis le répertoire racine du projet :

```bash
cd weather-report
cargo run >> ../data/report1.csv
cargo run >> ../data/report2.csv
cargo run >> ../data/report3.csv
```

## Utilisation par weather-analyzer

Le programme Python `weather-analyzer` lit tous les fichiers `report*.csv` de
ce répertoire pour effectuer ses analyses statistiques.

## Notes importantes

- Assurez-vous de générer au moins 3 fichiers CSV pour tester correctement le programme Python
- Chaque exécution de `cargo run` génère des données aléatoires différentes