# 2025E-420-920-MA Pratique pour l'épreuve finale

L'épreuve finale est composée de deux parties distinctes:
- Un programme `weather-report` qui génère des rapports météo aléatoires. Ce
  programme est écrit en Rust et se trouve dans le dossier `weather-report`.
- Un programme `weather-analyzer` qui lit les fichiers CSV générés par
  `weather-report`, analyse les données et affiche des statistiques. Ce programme
  est écrit en Python et se trouve dans le dossier `weather-analyzer`.

## Structure du dépôt

- `weather-report/`: Contient le code source du programme `weather-report`.
- `weather-analyzer/`: Contient le code source du programme `weather-analyzer`.
- `data/`: Contient les fichiers CSV générés par `weather-report` et utilisés par
  `weather-analyzer`.

## Consignes

- Chaque sous-dossier (`weather-report` et `weather-analyzer`) contient son propre
  fichier `README.md` avec des instructions spécifiques.

## Instructions pour exécuter les programmes

À la fin de l'épreuve finale, vous devrez être capable d'exécuter les programmes
`weather-report` et `weather-analyzer` en utilisant les commandes suivantes:

```bash
cd weather-report
cargo run > ../data/report1.csv
cargo run > ../data/report2.csv
cargo run > ../data/report3.csv
cd ../weather-analyzer
uv run main
```

## Remise

Puisque ceci est une pratique, vous faites une duplication (fork) de ce dépôt
GitHub dans votre propre compte. À la fin, vous soumettez une pull request
depuis votre fork vers ce dépôt original.