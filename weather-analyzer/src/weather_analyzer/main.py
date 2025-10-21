from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from functools import wraps
from pathlib import Path
from typing import Dict, Generator, Iterable, List, Tuple
import csv
import sys
import time


# ============================
# 1) Itérateurs et générateurs
# ============================
def read_weather_data(filename: str | Path) -> Generator[dict, None, None]:
    
    file_path = Path(filename)
    with file_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        # Ignore l'en-tête
        try:
            next(reader)
        except StopIteration:
            return
        for row in reader:
            if not row or len(row) < 4:
                continue
            date, station, temperature, pressure = row[0], row[1], row[2], row[3]
            try:
                temp_f = float(str(temperature).strip())
                pres_f = float(str(pressure).strip())
            except ValueError:
                # Ignore les lignes invalides
                continue
            yield {
                "date": date.strip(),
                "station": str(station).strip(),
                "temperature": temp_f,
                "pressure": pres_f,
            }


# ==================
# 2) Décorateur time
# ==================
def timing(func):
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        return result, (end - start)

    return wrapper


# =====================
# 3) Calculs statistiques
# =====================
@dataclass
class FileStats:
    records: int
    avg_temperature: float | None
    min_temperature: float | None
    max_temperature: float | None
    avg_pressure: float | None
    unique_stations: int


def _compute_file_stats(filename: str | Path) -> FileStats:
    count = 0
    temp_sum = 0.0
    pres_sum = 0.0
    temp_min: float | None = None
    temp_max: float | None = None
    stations: set[str] = set()

    for rec in read_weather_data(filename):
        t = rec["temperature"]
        p = rec["pressure"]
        s = rec["station"]
        count += 1
        temp_sum += t
        pres_sum += p
        temp_min = t if temp_min is None or t < temp_min else temp_min
        temp_max = t if temp_max is None or t > temp_max else temp_max
        stations.add(s)

    avg_t = (temp_sum / count) if count > 0 else None
    avg_p = (pres_sum / count) if count > 0 else None

    return FileStats(
        records=count,
        avg_temperature=avg_t,
        min_temperature=temp_min,
        max_temperature=temp_max,
        avg_pressure=avg_p,
        unique_stations=len(stations),
    )


@timing
def compute_file_stats(filename: str | Path) -> FileStats:
    return _compute_file_stats(filename)


# ==================
# 4) Threading / pool
# ==================
def process_files_concurrently(filenames: Iterable[str | Path]) -> Dict[str, Tuple[FileStats, float]]:
    """Traite les fichiers en parallèle (max 10 threads).

    Retourne un dict: { "chemin": (stats: FileStats, exec_time_seconds: float) }
    """
    files = [str(Path(f)) for f in filenames]
    if not files:
        return {}
    results: Dict[str, Tuple[FileStats, float]] = {}
    max_workers = min(10, len(files))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {executor.submit(compute_file_stats, f): f for f in files}
        for fut in as_completed(future_map):
            path = future_map[fut]
            try:
                stats, exec_time = fut.result()
                results[path] = (stats, exec_time)
            except Exception:
                # En cas d'erreur sur un fichier, on enregistre des stats vides
                results[path] = (
                    FileStats(0, None, None, None, None, 0),
                    0.0,
                )
    return results


# ====================
# 5) Affichage du rendu
# ====================
def _format_float(v: float | None, suffix: str = "") -> str:
    return f"{v:.1f}{suffix}" if v is not None else "N/A"


def print_report(results: Dict[str, Tuple[FileStats, float]]) -> None:
    print("=== Weather Analysis Report ===\n")
    print("--- Statistics by File ---")

    # Affichage stable par ordre alphabétique des chemins
    for path in sorted(results.keys()):
        stats, exec_time = results[path]
        print(f"File: {path}")
        print(f"Processed in {exec_time:.2f} seconds")
        print(f"  Records: {stats.records}")
        print(f"  Avg Temperature: {_format_float(stats.avg_temperature, '°C')}")
        print(f"  Min Temperature: {_format_float(stats.min_temperature, '°C')}")
        print(f"  Max Temperature: {_format_float(stats.max_temperature, '°C')}")
        print(f"  Avg Pressure: {_format_float(stats.avg_pressure, ' hPa')}")
        print(f"  Unique Stations: {stats.unique_stations}")
        print()


# =====
# main
# =====
def _find_default_csvs() -> List[str]:
    # 1) Essaye ../data/*.csv relatif au CWD (usage typique à partir de weather-analyzer)
    cwd = Path.cwd()
    default_dir = (cwd / ".." / "data").resolve()
    csvs = sorted(str(p) for p in default_dir.glob("*.csv")) if default_dir.exists() else []
    if csvs:
        return csvs

    # 2) Fallback: relatif à ce fichier, remonte jusqu'à la racine du repo et cherche data/*.csv
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "data"
        if candidate.exists():
            csvs = sorted(str(p) for p in candidate.glob("*.csv"))
            if csvs:
                return csvs
    return []


def main() -> None:
    # Récupère les fichiers à traiter à partir des arguments, sinon auto-détection
    args = sys.argv[1:]
    files: List[str]
    if args:
        files = [str(Path(a)) for a in args]
    else:
        files = _find_default_csvs()
        if not files:
            print("No CSV files provided or found in ../data. Pass file paths as arguments.")
            return

    results = process_files_concurrently(files)
    print_report(results)