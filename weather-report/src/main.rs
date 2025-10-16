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
    // Convertit une station en String
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
    // Convertit la structure en une ligne CSV
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

fn main() {
    // Test temporaire pour valider la struct et la méthode
    let record = WeatherRecord {
        date: "2025-03-15".to_string(),
        station: StationType::StationA,
        temperature: 18.5,
        pressure: 1013.2,
    };

    println!("{}", record.to_csv_line());
}