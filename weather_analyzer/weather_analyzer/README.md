# Weather Analyzer (Python) - 70% de la note finale

## Description du projet

Vous devez créer un programme Python qui analyse des fichiers CSV contenant des
données météorologiques et affiche des statistiques détaillées. Le programme
doit utiliser des **itérateurs**, des **décorateurs** et du **threading** pour
traiter les données efficacement.

## Spécifications techniques

### Structure des fichiers CSV

Les fichiers CSV générés par `weather-report` ont le format suivant :
```csv
Date,Station,Temperature,Pressure
2025-10-16,StationA,20,1015
2025-10-16,StationB,22,1013
```

### Fonctionnalités requises

#### 1. Itérateurs et générateurs

Créez un générateur `read_weather_data(filename)` qui :
- Lit un fichier CSV ligne par ligne
- Ignore la ligne d'en-tête
- Yield un dictionnaire pour chaque ligne avec les clés : `date`, `station`,
  `temperature`, `pressure`
- Convertit les valeurs numériques en `float`


#### 2. Décorateurs

Créez un décorateur personnalisé : `@timing` qui :

- Mesure le temps d'exécution d'une fonction
- Modifie la fonction pour qu'elle retourne le temps d'exécution en plus du
  résultat dans un tuple `(result, exec_time)`
- Le code doit être thread-safe

Vous devez utiliser ce décorateur pour calculer le temps d'exécution affiché dans
le rapport final.

#### 3. Threading

Créez une fonction `process_files_concurrently(filenames)` qui :
- Prend une liste de noms de fichiers
- Crée un thread pour traiter chaque fichier (maximum 10 threads)
- Chaque thread doit lire le fichier et calculer les statistiques
- Retourne un dictionnaire avec le nom des fichiers comme clés et les
  statistiques comme valeurs

#### 4. Calculs statistiques

Pour chaque fichier, calculez :
- Température moyenne
- Température minimale
- Température maximale
- Pression moyenne
- Nombre total de lectures
- Nombre de stations uniques

#### 5. Affichage des résultats

Affichez les résultats dans ce format :

```
=== Weather Analysis Report ===

--- Statistics by File ---
File: ../data/report1.csv
Processed in 0.03 seconds
  Records: 15
  Avg Temperature: 21.5°C
  Min Temperature: 15.0°C
  Max Temperature: 28.0°C
  Avg Pressure: 1015.3 hPa
  Unique Stations: 5

File: ../data/report2.csv
  ...

```

## Critères d'évaluation - Grille de correction (70 points)

### 1. Itérateurs et générateurs (20 points)
- [ ] Générateur `read_weather_data()` correctement implémenté avec `yield`
- [ ] Lecture ligne par ligne sans charger tout le fichier en mémoire
- [ ] Conversion correcte des types

### 2. Décorateurs (10 points)
- [ ] `@timing` correctement implémenté
- [ ] Mesure correcte du temps d'exécution

### 3. Threading (20 points)
- [ ] Un thread par fichier à traiter (maximum 10 threads)
- [ ] Le toutt est thread-safe

### 4. Calculs statistiques (10 points)
- [ ] Calcul de la température moyenne
- [ ] Calcul du min et max de température
- [ ] Calcul de la pression moyenne
- [ ] Comptage des lectures et stations uniques
- [ ] Statistiques globales correctes

### 5. Qualité du code et affichage (10 points)
- [ ] Code bien structuré et lisible
- [ ] Affichage des résultats au format demandé