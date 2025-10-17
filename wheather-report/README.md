# Weather Report (Rust) - 30% de la note finale

## Description du projet

Vous devez créer un programme Rust qui génère des données météorologiques
aléatoires au format CSV. Le programme utilise la bibliothèque `rand` pour
générer des dates et des données aléatoires. Tout le code doit être dans **un
seul fichier `main.rs`**.

## Spécifications techniques

### Format de sortie CSV

Votre programme doit générer des données au format CSV avec cet en-tête :

```csv
Date,Station,Temperature,Pressure
```

Suivi de 10 à 20 lignes de données aléatoires, par exemple :

```csv
Date,Station,Temperature,Pressure
2025-03-15,StationA,18.5,1013.2
2025-06-22,StationC,25.3,1015.8
2025-12-01,StationB,5.2,1020.1
```

### Fonctionnalités requises

#### 1. Enum pour les stations

Créez un `enum StationType` avec au moins 5 stations différentes. Implémentez
une méthode pour convertir l'enum en `String`.

#### 2. Struct pour les enregistrements météo

Créez une `struct WeatherRecord` qui contient :
- `date` : String au format "YYYY-MM-DD"
- `station` : StationType
- `temperature` : f32 (en degrés Celsius)
- `pressure` : f32 (en hPa - hectopascals)


Implémentez une méthode `to_csv_line()` qui retourne une ligne CSV.

#### 3. Génération de dates aléatoires

Créez une fonction `generate_random_date()` qui :
- Génère une année entre 2020 et 2025
- Génère un mois entre 1 et 12
- Génère un jour valide pour ce mois (attention aux mois avec 28, 30 ou 31
  jours). Vous pouvez ignorer les années bissextiles pour février (toujours 28
  jours).
- Retourne une String au format "YYYY-MM-DD"
- Ajoute un zéro devant les mois/jours < 10 (ex: "2025-03-05")

#### 4. Génération de données aléatoires

Créez une fonction `generate_weather_record()` qui :
- Génère une date aléatoire (utilisez votre fonction)
- Choisit une station aléatoire parmi l'enum
- Génère une température aléatoire entre -10.0°C et 40.0°C
- Génère une pression aléatoire entre 980.0 hPa et 1050.0 hPa
- Retourne un `WeatherRecord`


#### 5. Fonction main

Dans la fonction `main()` :
1. Créez un générateur aléatoire.
2. Affichez l'en-tête CSV avec `println!`.
3. Générez entre 10 et 20 enregistrements aléatoires.
4. Affichez chaque enregistrement avec `println!`.

## Restrictions

- ❌ N'utilisez PAS de bibliothèques externes autres que `rand`
- ❌ N'utilisez PAS de fichiers multiples (tout dans `main.rs`)
- ❌ N'utilisez PAS de concepts avancés (lifetimes complexes, traits personnalisés, etc.)

## Critères d'évaluation - Grille de correction (30 points)

### 1. Enum StationType (5 points)
- [ ] Enum déclaré avec au moins 5 variantes
- [ ] Méthode `to_string()` implémentée correctement
- [ ] Utilisation correcte de l'enum dans le code

### 2. Struct WeatherRecord (8 points)
- [ ] Struct déclaré avec les 4 champs corrects (date, station, temperature, pressure)
- [ ] Types appropriés
- [ ] Méthode `to_csv_line()` implémentée
- [ ] Format CSV correct avec virgules

### 3. Génération de dates aléatoires (7 points)
- [ ] Fonction `generate_random_date()` créée
- [ ] Génération d'année aléatoire dans la plage 2020-2025
- [ ] Génération de mois aléatoire 1-12
- [ ] Gestion correcte des jours par mois (28/30/31)
- [ ] Format "YYYY-MM-DD" avec zéros devant (ex: "2025-03-05")

### 4. Génération de données aléatoires (5 points)
- [ ] Fonction `generate_weather_record()` créée
- [ ] Utilisation de `rand` pour générer tous les champs aléatoires
- [ ] Plages de valeurs correctes (temp: -10 à 40, pressure: 980 à 1050)
- [ ] Retourne un `WeatherRecord` valide

### 5. Fonction main et affichage (5 points)
- [ ] Affichage de l'en-tête CSV correct
- [ ] Génération d'un nombre aléatoire d'enregistrements (10-20)
- [ ] Boucle pour générer et afficher les enregistrements
- [ ] Utilisation correcte de `println!` pour chaque ligne