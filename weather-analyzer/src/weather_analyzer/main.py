from typing import Iterator, Dict, Any
import weather_report
import time
import glob
import os
from concurrent.futures import ThreadPoolExecutor

def generate_csv_files(directory: str = "data", num_files: int = 3) -> None:
    """Génère des fichiers CSV avec des données aléatoires de weather_report"""
    os.makedirs(directory, exist_ok=True)
    
    print(f"Génération de {num_files} fichiers CSV avec weather_report...\n")
    
    for i in range(1, num_files + 1):
        filename = os.path.join(directory, f"report{i}.csv")
        
        # Générer les données aléatoires
        weather_data = weather_report.generate_weather_data()
        
        # Écrire dans le fichier
        with open(filename, 'w') as f:
            for line in weather_data:
                f.write(line + '\n')
        
        print(f"✓ Créé: {filename}")

def discover_csv_files(directory: str = "data", pattern: str = "*.csv") -> list[str]:
    """Découvre automatiquement tous les fichiers CSV dans un répertoire"""
    files_path = os.path.join(directory, pattern)
    files = sorted(glob.glob(files_path))
    return files

def main() -> None:
    print("=== Weather Analysis Report ===\n")
    
    # 1. Générer les fichiers CSV avec weather_report
    generate_csv_files("data", num_files=3)
    print()
    
    # 2. Découvrir tous les fichiers CSV générés
    filenames = discover_csv_files("data")
    
    if not filenames:
        print("Aucun fichier CSV trouvé!")
        return
    
    print(f"Fichiers à analyser: {len(filenames)}\n")
    
    # 3. Traiter les fichiers concurremment
    results = process_files_concurrently(filenames)
    
    # 4. Afficher les résultats
    display_results(results)


# itération de weather data
def read_weather_data(filename: str) -> Iterator[Dict[str, Any]]:
    """Lit un fichier CSV et yield un dictionnaire pour chaque ligne"""
    try:
        with open(filename, 'r') as file:
            next(file)  # Ignorer l'en-tête
            for line in file:
                parts = line.strip().split(',')
                if len(parts) >= 4:
                    yield {
                        'date': parts[0],
                        'station': parts[1],
                        'temperature': float(parts[2]),
                        'pressure': float(parts[3])
                    }
    except FileNotFoundError:
        print(f"Fichier non trouvé: {filename}")


# décorateur pour mesurer le temps d'exécution
def timing(func):
    """Décorateur thread-safe qui mesure le temps d'exécution"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        exec_time = end_time - start_time
        return (result, exec_time)
    return wrapper


# Calculs statistiques (avec décorateur timing)
@timing
def calculate_statistics(filename: str) -> Dict[str, Any]:
    """Calcule les statistiques pour un fichier"""
    temperatures = []
    pressures = []
    stations = set()
    record_count = 0
    
    for record in read_weather_data(filename):
        temperatures.append(record['temperature'])
        pressures.append(record['pressure'])
        stations.add(record['station'])
        record_count += 1
    
    if not record_count:
        return {
            'filename': filename,
            'records': 0,
            'avg_temperature': 0,
            'min_temperature': 0,
            'max_temperature': 0,
            'avg_pressure': 0,
            'unique_stations': 0
        }
    
    return {
        'filename': filename,
        'records': record_count,
        'avg_temperature': sum(temperatures) / len(temperatures),
        'min_temperature': min(temperatures),
        'max_temperature': max(temperatures),
        'avg_pressure': sum(pressures) / len(pressures),
        'unique_stations': len(stations)
    }


# threading process_files_concurrently(filenames)
def process_files_concurrently(filenames: list[str]) -> Dict[str, Dict[str, Any]]:
    """
    Traite plusieurs fichiers concurremment (maximum 10 threads)
    Retourne un dictionnaire avec le nom des fichiers comme clés
    et les statistiques comme valeurs
    """
    results = {}
    
    # Utiliser ThreadPoolExecutor avec maximum 10 threads
    with ThreadPoolExecutor(max_workers=min(10, len(filenames))) as executor:
        futures = {}
        
        # Lancer les tâches
        for filename in filenames:
            future = executor.submit(calculate_statistics, filename)
            futures[filename] = future
        
        # Récupérer les résultats
        for filename, future in futures.items():
            stats, exec_time = future.result()  # Déballer (result, exec_time)
            stats['exec_time'] = exec_time
            results[filename] = stats
    
    return results


# afficher les resultats
def display_results(results: Dict[str, Dict[str, Any]]) -> None:
    """Affiche les résultats au format demandé"""
    print("--- Statistics by File ---")
    for filename, stats in results.items():
        print(f"\nFile: {filename}")
        print(f"Processed in {stats['exec_time']:.3f} seconds")
        print(f"  Records: {stats['records']}")
        print(f"  Avg Temperature: {stats['avg_temperature']:.1f}°C")
        print(f"  Min Temperature: {stats['min_temperature']:.1f}°C")
        print(f"  Max Temperature: {stats['max_temperature']:.1f}°C")
        print(f"  Avg Pressure: {stats['avg_pressure']:.1f} hPa")
        print(f"  Unique Stations: {stats['unique_stations']}")


if __name__ == "__main__":
    main()