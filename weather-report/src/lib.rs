use pyo3::prelude::*;
use rand::Rng;

#[derive(Debug, Clone, Copy)]
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
            StationType::StationA => String::from("StationA"),
            StationType::StationB => String::from("StationB"),
            StationType::StationC => String::from("StationC"),
            StationType::StationD => String::from("StationD"),
            StationType::StationE => String::from("StationE"),
        }
    }
}

#[derive(Debug, Clone)]
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

/// Génère des données météorologiques aléatoires et retourne une liste de lignes CSV
#[pyfunction]
#[pyo3(signature = (num_records=None))]
fn generate_weather_data(num_records: Option<usize>) -> PyResult<Vec<String>> {
    let mut rng = rand::thread_rng();
    
    let count = match num_records {
        Some(n) => n,
        None => rng.gen_range(10..=20),
    };
    
    let mut result = vec!["Date,Station,Temperature,Pressure".to_string()];
    
    for _ in 0..count {
        let record = generate_weather_record();
        result.push(record.to_csv_line());
    }
    
    Ok(result)
}

/// Module Python exposant les fonctionnalités Rust
#[pymodule]
fn weather_report(_py: Python, m: &Bound<PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_weather_data, m)?)?;
    Ok(())
}
