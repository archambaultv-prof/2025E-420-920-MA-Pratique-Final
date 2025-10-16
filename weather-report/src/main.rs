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

// Définition de la structure WeatherRecord
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

// Fonction pour générer une date aléatoire valide
fn generate_random_date() -> String {
    let mut rng = rand::thread_rng();

    let year = rng.gen_range(2020..=2025);
    let month = rng.gen_range(1..=12);

    // Déterminer le nombre de jours dans le mois
    let days_in_month = match month {
        2 => 28,
        4 | 6 | 9 | 11 => 30,
        _ => 31,
    };

    let day = rng.gen_range(1..=days_in_month);

    // Retourne au format YYYY-MM-DD avec des zéros
    format!("{:04}-{:02}-{:02}", year, month, day)
}

fn main() {
    // Test temporaire : afficher 5 dates aléatoires
    for _ in 0..5 {
        println!("{}", generate_random_date());
    }
}