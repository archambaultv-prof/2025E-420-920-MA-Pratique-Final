
from __future__ import annotations
import sys
import csv
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, Iterable, Iterator, Tuple, Optional

# Iterateur
def read_weather_data(filename: str | Path) -> Iterator[dict]:
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if not row or len(row) < 4:
                continue
            date, station, temp, pres = row[0], row[1], row[2], row[3]
            try:
                yield {
                    "date": date,
                    "station": station,
                    "temperature": float(temp),
                    "pressure": float(pres),
                }
            except ValueError:
                continue

# Decorateur calcul de temps
def timing(fn):
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = fn(*args, **kwargs)
        dt = time.perf_counter() - t0
        return result, dt
    return wrapper

# Analyse de fichier
def compute_stats(records: Iterable[dict]) -> Dict[str, float | int]:
    count = 0
    sum_temp = 0.0
    sum_pres = 0.0
    min_temp = float("inf")
    max_temp = float("-inf")
    stations = set()

    for rec in records:
        t = rec["temperature"]
        p = rec["pressure"]
        sum_temp += t
        sum_pres += p
        if t < min_temp:
            min_temp = t
        if t > max_temp:
            max_temp = t
        stations.add(rec["station"])
        count += 1

    if count == 0:
        return {
            "count": 0,
            "avg_temp": None,
            "min_temp": None,
            "max_temp": None,
            "avg_pres": None,
            "unique_stations": 0,
        }

    
    return {
        "count": count,
        "avg_temp": sum_temp / count,
        "min_temp": min_temp,
        "max_temp": max_temp, 
        "avg_pres": sum_pres / count,
        "unique_stations": len(stations),
    }

@timing
def analyze_file(filename: str | Path) -> Dict[str, float | int]:
    return compute_stats(read_weather_data(filename))




# Threaded 
def process_files_concurrently(filenames: list[str | Path]) -> Dict[str, Tuple[dict, float]]:
    out: Dict[str, Tuple[dict, float]] = {}
    max_workers = min(10, max(1, len(filenames)))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {executor.submit(analyze_file, str(fn)): str(fn) for fn in filenames}
        for fut in as_completed(future_map):
            name = future_map[fut]
            try:
                stats, secs = fut.result()
                out[name] = (stats, secs)
            except Exception as e:
                out[name] = (
                    {
                        "count": 0,
                        "avg_temp": None,
                        "min_temp": None,
                        "max_temp": None,
                        "avg_pres": None,
                        "unique_stations": 0,
                        "error": str(e),
                    },
                    0.0,
                )
    return out

# Rapport

def print_report(results: Dict[str, Tuple[dict, float]]):
    print("=== Rapport d'analyse Meteo ===\n")
    print("--- Statistique par fichier ---")
    for name in sorted(results):
        stats, secs = results[name]
        print(f"File: {name}")
        if "error" in stats:
            print(f"  Error: {stats['error']}\n")
            continue

        print(f"Traité en {secs:.2f} secondes")
        print(f"  Records: {stats['count']}")

        if stats["avg_temp"] is None:
            print("  Moyenne Temperature: -")
            print("  Min Temperature: -")
            print("  Max Temperature: -")
            print("  Moyenne Pression: -")
        else:
            print(f"  Moyenne Temperature: {stats['avg_temp']:.1f}°C")
            print(f"  Min Temperature: {stats['min_temp']:.1f}°C")
            print(f"  Max Temperature: {stats['max_temp']:.1f}°C")
            print(f"  Moyenne Pression: {stats['avg_pres']:.1f} hPa")

        print(f"  Station Unique: {stats['unique_stations']}\n")



def main(argv: list[str] = sys.argv) -> int:
    if len(argv) > 1:
        files = [Path(p) for p in argv[1:]]
    else:
        data_dir = Path(__file__).resolve().parent.parent / "data"
        files = sorted(data_dir.glob("report*.csv"))
        if not files:
            print("no files")
           
            return 2
    results = process_files_concurrently(files)
    print_report(results)
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))