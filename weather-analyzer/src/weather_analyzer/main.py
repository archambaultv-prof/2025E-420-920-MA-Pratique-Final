
import os
import csv
import glob
import statistics
import threading
from met_dat_sat import MetDatSat

# Fonction pour calculer et afficher les statistiques globales
def print_global_stats(all_rows, numeric_cols):
    print("Statistiques globales sur toutes les stations et dates:")
    for col in numeric_cols:
        try:
            values = [float(row[col]) for row in all_rows if row[col] != '']
            if values:
                print(f"- {col} : min={min(values)}, max={max(values)}, moyenne={round(statistics.mean(values),2)}")
            else:
                print(f"- {col} : aucune donnée")
        except Exception as e:
            print(f"- {col} : erreur lors du calcul ({e})")

# Fonction pour calculer et afficher les statistiques par date
def print_stats_by_date(all_objs, numeric_cols):
    print("\nStatistiques par date:")
    dates = sorted(set(obj.date for obj in all_objs))
    for date in dates:
        print(f"\nDate : {date}")
        objs_date = [obj for obj in all_objs if obj.date == date]
        print_global_stats([obj.as_dict() for obj in objs_date], numeric_cols)
        
# Fonction pour calculer et afficher les statistiques par station
def print_stats_by_station(all_objs, numeric_cols):
    print("\nStatistiques par station:")
    stations = sorted(set(obj.station for obj in all_objs))
    for station in stations:
        print(f"\nStation : {station}")
        objs_station = [obj for obj in all_objs if obj.station == station]
        print_global_stats([obj.as_dict() for obj in objs_station], numeric_cols)

# Fonction pour lire un fichier CSV et créer des objets MetDatSat
def read_csv_file(file, all_objs):
    with open(file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                obj = MetDatSat(
                    row["Date"], row["Station"], row["Temperature"], row["Pressure"], row["Humidity"],
                    row["WindSpeed"], row["WindDirection"], row["Precipitation"], row["CloudCover"], row["Visibility"], row["UVIndex"]
                )
                all_objs.append(obj)
            except Exception as e:
                print(f"Erreur de conversion d'une ligne: {e}")

# Fonction pour créer des objets MetDatSat en utilisant le multithreading
def create_metdat_objects_threaded(csv_files):
    all_objs = []
    threads = []
    for file in csv_files:
        t = threading.Thread(target=read_csv_file, args=(file, all_objs))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return all_objs


def main() -> None:
    # Configuration des chemins
    # Recherche du dossier data à la racine du projet
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../../../"))
    default_data_dir = os.path.join(project_root, "data")
    data_dir = os.environ.get("DATA_PATH", default_data_dir)
    print(f"[DEBUG] Recherche des fichiers CSV dans : {data_dir}")
    csv_files = glob.glob(os.path.join(data_dir, "report*.csv"))
    if not csv_files:
        print("Aucun fichier CSV trouvé dans le dossier data.")
        return
    # Création des objets MetDatSat
    print(f"Analyse des fichiers : {', '.join([os.path.basename(f) for f in csv_files])}\n")
    all_objs = create_metdat_objects_threaded(csv_files)
    # Vérification s'il y a des données
    if not all_objs:
        print("Aucune donnée à analyser.")
        return
    # Colonnes à analyser
    numeric_cols = [
        "Temperature", "Pressure", "Humidity", "WindSpeed", "WindDirection",
        "Precipitation", "CloudCover", "Visibility", "UVIndex"
    ]
    # Affichage des statistiques via appel de fonctions
    print_global_stats([obj.as_dict() for obj in all_objs], numeric_cols)
    print_stats_by_date(all_objs, numeric_cols)
    print_stats_by_station(all_objs, numeric_cols)

if __name__ == "__main__":
    main()