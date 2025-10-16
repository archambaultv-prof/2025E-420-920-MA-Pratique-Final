use rand::Rng;

#[derive(Debug, Clone, Copy)]
enum StationType {
    StationA,
    StationB,
    StationC,
    StationD,
    StationE,
}
// Implémentation d'une méthode pour convertir StationType en chaîne de caractères
impl StationType {
    fn to_string(&self) -> String {
        match self {
            StationType::StationA => String::from("StationA"),
            StationType::StationB => String::from("StationB"),
            StationType::StationC => String::from("StationC"),
            StationType::StationD => String::from("StationD"),
            StationType::StationE => String::from("StationE"),
        }
    }
}


// Structure représentant un relevé météorologique
struct WeatherRecord {
    date: String, // Format: "YYYY-MM-DD"
    station: StationType,
    temperature: f32, // en Celsius
    pressure: f32,    // en hPa
}
// Implémentation d'une méthode pour convertir WeatherRecord en ligne CSV
impl WeatherRecord {
    fn to_csv_line(&self) -> String {
        format!(
            "{},{},{:.1},{:.1}",
            self.date,
            self.station.to_string(),
            self.temperature,
            self.pressure
        )
    }
}



// Fonction pour générer une date aléatoire entre 2020 et 2025
fn generate_random_date() -> String {
    let mut rng = rand::thread_rng();
    let year = rng.gen_range(2020..=2025);
    let month = rng.gen_range(1..=12);
    let max_day = match month {
        2 => 28,
        4 | 6 | 9 | 11 => 30,
        _ => 31,
    };
    let day = rng.gen_range(1..=max_day);
    format!("{:04}-{:02}-{:02}", year, month, day)
}


// Fonction pour générer un relevé météorologique aléatoire
fn generate_weather_record() -> WeatherRecord {
    let mut rng = rand::thread_rng();
    let stations = [
        StationType::StationA,
        StationType::StationB,
        StationType::StationC,
        StationType::StationD,
        StationType::StationE,
    ];
    let station = stations[rng.gen_range(0..stations.len())];
    let temperature = rng.gen_range(-10.0..40.0);
    let pressure = rng.gen_range(980.0..1050.0);
    WeatherRecord {
        date: generate_random_date(),
        station,
        temperature,
        pressure,
    }
}

fn main() {
    // 1. Générateur aléatoire
    let mut rng = rand::thread_rng();
    
    // 2. En-tête CSV
    println!("Date,Station,Temperature,Pressure");
    
    // Génère entre 10 et 20 enregistrements et les afficher
    let num_records = rng.gen_range(10..=20);
    for _ in 0..num_records {
        let record = generate_weather_record();
        println!("{}", record.to_csv_line());
    }
}