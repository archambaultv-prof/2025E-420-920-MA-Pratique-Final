use rand::prelude::*; 
use rand::rngs::ThreadRng;

// 1. Enum pour les stations
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

    fn random(rng: &mut ThreadRng) -> StationType {
        match rng.random_range(0..5) {
            0 => StationType::StationA,
            1 => StationType::StationB,
            2 => StationType::StationC,
            3 => StationType::StationD,
            _ => StationType::StationE,
        }
    }
}

// 2. Struct WeatherRecord
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

// 3. Génération de dates aléatoires

fn generate_random_date(rng: &mut ThreadRng) -> String {
    let year = rng.random_range(2020..=2025);
    let month = rng.random_range(1..=12);
    let day = match month {
        2 => rng.random_range(1..=28),
        4 | 6 | 9 | 11 => rng.random_range(1..=30),
        _ => rng.random_range(1..=31),
    };
    format!("{:04}-{:02}-{:02}", year, month, day)
}

// 4. Génération d’un enregistrement météo

fn generate_weather_record(rng: &mut ThreadRng) -> WeatherRecord {
    let date = generate_random_date(rng);
    let station = StationType::random(rng);
    let temperature = rng.random_range(-10.0..=40.0);
    let pressure = rng.random_range(980.0..=1050.0);

    WeatherRecord {
        date,
        station,
        temperature,
        pressure,
    }
}

// 
// 5. Fonction principale
fn main() {
    let mut rng = ThreadRng::default(); 

    println!("Date,Station,Temperature,Pressure");

    let n_records = rng.random_range(10..=20);

    for _ in 0..n_records {
        let record = generate_weather_record(&mut rng);
        println!("{}", record.to_csv_line());
    }
}
