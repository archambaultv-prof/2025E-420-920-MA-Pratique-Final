use rand::Rng; // Pour générer des nombres aléatoires
use chrono::{NaiveDate, Duration};

// -------------------------------
// Définition de la structure
// -------------------------------
struct WeatherRecord {
    date: NaiveDate,
    station: String,
    temperature: f32,
    pressure: f32,
}

fn main() {
    let stations = vec!["StationA", "StationB", "StationC"];

    // Générer 10 lignes de données pour l'exemple
    let start_date = NaiveDate::from_ymd_opt(2025, 10, 16).unwrap();
    let mut rng = rand::thread_rng();

    println!("Date,Station,Temperature,Pressure");

    for i in 0..10 {
        let date = start_date + Duration::days(i); // dates consécutives
        let station = stations[rng.gen_range(0..stations.len())].to_string();
        let temperature = rng.gen_range(-10.0..35.0); // température aléatoire
        let pressure = rng.gen_range(980.0..1050.0);   // pression aléatoire

        let record = WeatherRecord {
            date,
            station,
            temperature,
            pressure,
        };

        println!(
            "{},{},{:.1},{:.1}",
            record.date, record.station, record.temperature, record.pressure
        );
    }
}
