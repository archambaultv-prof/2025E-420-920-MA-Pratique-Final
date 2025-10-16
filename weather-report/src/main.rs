use rand::Rng;
use std::env;
use std::fs::File;
use std::io::{Write, BufWriter, stdin, stdout};

fn main() {
    let stations = ["Station_A", "Station_B", "Station_C", "Station_D", "Station_E"];
    let data_path = env::var("DATA_PATH").unwrap_or_else(|_| "../data".to_string());

    // Demande la date à l'utilisateur (facilite la creation de plusieurs rapports)
    println!("Entrez la date du rapport (format AAAAMMJJ, ex: 20251016): ");
    let mut input = String::new();
    stdout().flush().unwrap();
    stdin().read_line(&mut input).expect("Erreur de lecture");
    let date_str = input.trim();
    // Vérifie le format de la date 
    if date_str.len() != 8 || !date_str.chars().all(|c| c.is_digit(10)) {
        println!("Format de date invalide. Utilisez AAAAMMJJ.");
        return;
    }

    let file_path = format!("{}/report{}.csv", data_path, date_str);
    let file = File::create(&file_path).expect("Impossible de créer le fichier CSV");
    let mut writer = BufWriter::new(file);
    writeln!(writer, "Date,Station,Temperature,Pressure,Humidity,WindSpeed,WindDirection,Precipitation,CloudCover,Visibility,UVIndex").unwrap();
    let mut rng = rand::thread_rng();
    for station in stations.iter() {
        let temp = rng.gen_range(-10..35); // Température entre -10 et 35°C
        let pressure = rng.gen_range(980..1030); // Pression entre 980 et 1030 hPa
        let humidity = rng.gen_range(20..100); // Humidité entre 20% et 100%
        let wind_speed = rng.gen_range(0..100); // Vitesse du vent entre 0 et 100 km/h
        let wind_direction = rng.gen_range(0..360); // Direction du vent entre 0° et 360°
        let precipitation = rng.gen_range(0..50); // Précipitations entre 0 et 50 mm
        let cloud_cover = rng.gen_range(0..100); // Couverture nuageuse entre 0% et 100%
        let visibility = rng.gen_range(1..20); // Visibilité entre 1 et 20 km
        let uv_index = rng.gen_range(0..11); // Indice UV entre 0 et 11
        writeln!(writer, "{},{},{},{},{},{},{},{},{},{},{}", date_str, station, temp, pressure, humidity, wind_speed, wind_direction, precipitation, cloud_cover, visibility, uv_index).unwrap();
    }
    println!("Rapport météo généré dans : {}", file_path);
}
