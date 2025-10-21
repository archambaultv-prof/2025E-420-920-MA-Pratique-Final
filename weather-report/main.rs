use rand::prelude::*;
use rand::distributions::{Uniform, Distribution};
use std::fmt;

// 1. Enum pour les stations
#[derive(Clone, Copy)]
enum StationType {
    StationA, 
    StationB, 
    StationC, 
    StationD, 
    StationE, 
}

impl StationType {
    fn to_string(&self) -> String {
        match self{
            StationType::StationA => "StationA".to_string(), 
            StationType::StationB => "StationB".to_string(), 
            StationType::StationC => "StationC".to_string(), 
            StationType::StationD => "StationD".to_string(), 
            StationType::StationE => "StationE".to_string(),          
        }
    }   

// Pour choisir une station aléatoire
    fn random(rng: &mut ThreadRng) -> StationType {
        match rng.gen_range(0..5) {
            0 => StationType::StationA, 
            1 => StationType::StationB, 
            2 => StationType::StationC, 
            3 => StationType::StationD, 
            4 => StationType::StationE, 
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
            "{}, {}, {:.1}, {:.1}", 
            self.date, 
            self.station.to_string(), 
            self.temperature, 
            self.pressure
        )
    }
        
}

// 3. Génération de dates aléatoires
fn generate_random_date(rng: &mut ThreadRng) -> String {
    let year = rng.gen_range(2020..=2025); 
    let month = rng.gen_range(1..=12);
    // Determiner le nombre de jours dans le mois (je laisse tomber les accents, mon clavier me gosse.)
    let max_day = match month {
        2 => 28, 
        4 | 6 | 9 | 11 => 30, 
        _ => 31, 
    };
    let day = rng.gen_range(1..=max_day);
    format!("{:04}-{:02}-{:02}", year, month, day)
}

// 4. Generation de donnees aleatoires
fn generate_weather_record(rng: &mut ThreadRng) -> WeatherRecord {
    let date = generate_random_date(rng);
    let station = StationType::random(rng);
    let temperature = rng.gen_range(-10.0..=40.0);
    let pressure = rng.gen_range(980.0..=1050.0);
    WheatherRecord { 
        date, 
        station, 
        temperature, 
        pressure, 
    }
}

// 5. Fonction Main
fn main() {
    let mut rng = rand::thread_rng();

    println!("Date, Station, Temperature, Pressure");

    let num_records = rng.gen_range(10..=20);

    for _ in 0..num_records {
        let record = generate_weather_record(&mut rng);
        println!("{}", record.to_csv_line());
    }
}
