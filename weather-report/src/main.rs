use rand::distributions::{Distribution, Uniform};
use rand::Rng;

// Enum pour les stations (au moins 5)
#[derive(Copy, Clone, Debug)]
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

    fn all() -> [StationType; 5] {
        [
            StationType::StationA,
            StationType::StationB,
            StationType::StationC,
            StationType::StationD,
            StationType::StationE,
        ]
    }
}

// Struct pour un enregistrement météo
struct WeatherRecord {
    date: String,          // YYYY-MM-DD
    station: StationType,  // enum
    temperature: f32,      // Celsius
    pressure: f32,         // hPa
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

// Génère une date aléatoire (2020-2025), mois 1-12, jour en fonction du mois
fn generate_random_date<R: Rng + ?Sized>(rng: &mut R) -> String {
    let year = Uniform::from(2020..=2025).sample(rng);
    let month = Uniform::from(1..=12).sample(rng);
    let max_day = match month {
        1 | 3 | 5 | 7 | 8 | 10 | 12 => 31,
        4 | 6 | 9 | 11 => 30,
        2 => 28, // ignore bissextiles comme permis
        _ => 30,
    };
    let day = Uniform::from(1..=max_day).sample(rng);
    format!("{year:04}-{month:02}-{day:02}")
}

// Génère un enregistrement météo aléatoire
fn generate_weather_record<R: Rng + ?Sized>(rng: &mut R) -> WeatherRecord {
    let stations = StationType::all();
    let idx = Uniform::from(0..stations.len()).sample(rng);
    let station = stations[idx];

    let temperature = Uniform::from(-100..=400) // on génère en dixièmes pour un f32 ensuite
        .sample(rng) as f32
        / 10.0; // -10.0 à 40.0

    let pressure = Uniform::from(9800..=10500)
        .sample(rng) as f32
        / 10.0; // 980.0 à 1050.0

    WeatherRecord {
        date: generate_random_date(rng),
        station,
        temperature,
        pressure,
    }
}

fn main() {
    let mut rng = rand::thread_rng();

    // En-tête
    println!("Date,Station,Temperature,Pressure");

    // Nombre aléatoire d'enregistrements entre 10 et 20
    let n = Uniform::from(10..=20).sample(&mut rng);
    for _ in 0..n {
        let rec = generate_weather_record(&mut rng);
        println!("{}", rec.to_csv_line());
    }
}