
use rand::Rng;

enum StationType {
    MontrealWeather,
    QuebecCold,
    SherbrookeSunlight,
    HotOrCold,
    WeatherCanada,
}

impl StationType {
    fn to_string(&self) -> String {
        match self {
            StationType::MontrealWeather => "MontrealWeather".to_string(),
            StationType::QuebecCold => "QuebecCold".to_string(),
            StationType::SherbrookeSunlight => "SherbrookeSunlight".to_string(),
            StationType::HotOrCold => "HotOrCold".to_string(),
            StationType::WeatherCanada => "WeatherCanada".to_string(),
        }
    }
}

struct WeatherRecord {
    date: String,
    station: StationType,
    temperature: f32,
    pressure: f32,
}

impl WeatherRecord {
    fn to_csv_line(&self) -> String {
        format!("{},{},{:.1},{:.1}",
        self.date,
        self.station.to_string(),
        self.temperature,
        self.pressure)
    }
}


fn generate_random_date() -> String {
    let mut rng = rand::rng();
    let month = rng.random_range(1..=12);
    let year = rng.random_range(2020..=2025);
    
    let max_day = match month {
        2 => 28,
        4 | 6 | 9 | 11 => 30,
        _ => 31,
    };
    let day = rng.random_range(1..=max_day);
    
    format!("{:04}-{:02}-{:02}", year, month, day)
}


fn generate_weather_record() -> WeatherRecord {
    let mut rng = rand::rng();
    let date = generate_random_date();
    let station_num = rng.random_range(1..=5);
    let station = match station_num {
        1 => StationType::MontrealWeather,
        2 => StationType::QuebecCold,
        3 => StationType::SherbrookeSunlight,
        4 => StationType::HotOrCold,
        _ => StationType::WeatherCanada,
    };
    let temp = rng.random_range(-10.0..=40.0);
    let pressure = rng.random_range(980.0..=1050.0);
    
    WeatherRecord { date: date, station: station, temperature: temp, pressure: pressure }
}


fn main() {
    let nb_lines = rand::rng().random_range(10..=20);
    println!("Date,Station,Temperature,Pressure");
    for _ in 0..nb_lines {
        let line = generate_weather_record();
        println!("{}", line.to_csv_line());
    }
}
