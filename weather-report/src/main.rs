use rand::Rng;

// Définition de l'enum StationType
enum StationType {
    StationA,
    StationB,
    StationC,
    StationD,
    StationE,
}

impl StationType {
    fn to_string(&self) -> String {
        match self {
            StationType::StationA => "StationA".to_string(),
            StationType::StationB => "StationB".to_string(),
            StationType::StationC => "StationC".to_string(),
            StationType::StationD => "StationD".to_string(),
            StationType::StationE => "StationE".to_string(),
        }
    }
}

// Structure pour un enregistrement météo
struct WeatherRecord {
    date: String,
    station: StationType,
    temperature: f32,
    pressure: f32,
}

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

// Génère une date aléatoire au format YYYY-MM-DD
fn generate_random_date() -> String {
    let mut rng = rand::thread_rng();
    let year = rng.gen_range(2020..=2025);
    let month = rng.gen_range(1..=12);
    let days_in_month = match month {
        2 => 28,
        4 | 6 | 9 | 11 => 30,
        _ => 31,
    };
    let day = rng.gen_range(1..=days_in_month);
    format!("{:04}-{:02}-{:02}", year, month, day)
}

// Génère un WeatherRecord complet avec données aléatoires
fn generate_weather_record() -> WeatherRecord {
    let mut rng = rand::thread_rng();

    let station = match rng.gen_range(0..5) {
        0 => StationType::StationA,
        1 => StationType::StationB,
        2 => StationType::StationC,
        3 => StationType::StationD,
        _ => StationType::StationE,
    };

    WeatherRecord {
        date: generate_random_date(),
        station,
        temperature: rng.gen_range(-10.0..=40.0),
        pressure: rng.gen_range(980.0..=1050.0),
    }
}

fn main() {
    let mut rng = rand::thread_rng();
    let count = rng.gen_range(10..=20); // entre 10 et 20 lignes

    println!("Date,Station,Temperature,Pressure");

    for _ in 0..count {
        let record = generate_weather_record();
        println!("{}", record.to_csv_line());
    }
}