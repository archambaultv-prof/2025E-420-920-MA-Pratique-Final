use std::time::{SystemTime, UNIX_EPOCH};

// 1. Enum pour les stations
enum StationType {
    StationA,
    StationB,
    StationC,
    StationD,
    StationE,
}

impl StationType {
    fn random_station(rng: &mut SimpleRng) -> StationType {
        match rng.gen_range(0, 5) {  
            0 => StationType::StationA,
            1 => StationType::StationB,
            2 => StationType::StationC,
            3 => StationType::StationD,
            _ => StationType::StationE,
        }
    }
}

// Implémentation de to_string pour StationType
impl ToString for StationType {
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

// 2. Struct pour les enregistrements météo
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

// Générateur de nombres aléatoires simple
struct SimpleRng {
    state: u64,
}

impl SimpleRng {
    fn new() -> Self {
        let seed = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos() as u64;
        SimpleRng { state: seed }
    }
    
    fn next(&mut self) -> u64 {
        // Générateur linéaire congruentiel simple
        self.state = self.state.wrapping_mul(6364136223846793005).wrapping_add(1);
        self.state
    }
    
    fn gen_range(&mut self, low: usize, high: usize) -> usize {
        let range = (high - low) as u64;
        (low as u64 + self.next() % range) as usize
    }
    
    fn gen_range_f32(&mut self, low: f32, high: f32) -> f32 {
        let random_ratio = (self.next() % 1000) as f32 / 1000.0;
        low + random_ratio * (high - low)
    }
}

// 3. Génération de dates aléatoires
fn generate_random_date(rng: &mut SimpleRng) -> String {
    let year = rng.gen_range(2020, 2026); // 2020-2025
    let month = rng.gen_range(1, 13); // 1-12
    
    let day = match month {
        2 => rng.gen_range(1, 29), // Février - 28 jours (années non bissextiles)
        4 | 6 | 9 | 11 => rng.gen_range(1, 31), // Avril, juin, septembre, novembre - 30 jours
        _ => rng.gen_range(1, 32), // Autres mois - 31 jours
    };
    
    // Formatage avec zéros devant si nécessaire
    let month_str = if month < 10 {
        format!("0{}", month)
    } else {
        month.to_string()
    };
    
    let day_str = if day < 10 {
        format!("0{}", day)
    } else {
        day.to_string()
    };
    
    format!("{}-{}-{}", year, month_str, day_str)
}

// 4. Génération de données aléatoires
fn generate_weather_record(rng: &mut SimpleRng) -> WeatherRecord {
    let date = generate_random_date(rng);
    let station = StationType::random_station(rng);
    let temperature = rng.gen_range_f32(-10.0, 40.0);
    let pressure = rng.gen_range_f32(980.0, 1050.0);
    
    WeatherRecord {
        date,
        station,
        temperature,
        pressure,
    }
}

// 5. Fonction main
fn main() {
    let mut rng = SimpleRng::new();
    
    // Afficher l'en-tête CSV
    println!("Date,Station,Temperature,Pressure");
    
    // Générer entre 10 et 20 enregistrements aléatoires
    let num_records = rng.gen_range(10, 21);
    
    for _ in 0..num_records {
        let record = generate_weather_record(&mut rng);
        println!("{}", record.to_csv_line());
    }
}
