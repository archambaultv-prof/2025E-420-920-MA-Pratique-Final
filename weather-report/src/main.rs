use rand::Rng;

enum Station {
    StationA,
    StationB,
    StationC,
    StationD,
    StationE,
}
struct WeatherRecord {
    // date : String au format "YYYY-MM-DD"
    date: String,
    station: Station,
    temperature: f32,
    pressure: f32,
}

impl WeatherRecord {
    fn new() -> Self {
        let date = generate_random_date();
        let station = match rand::rng().random_range(1..=5) {
            1 => Station::StationA,
            2 => Station::StationB,
            3 => Station::StationC,
            4 => Station::StationD,
            5 => Station::StationE,
            _ => panic!("invalid station"),
        };

        let temperature = rand::rng().random_range(-10.0..=40.0);
        let pressure = rand::rng().random_range(980.0..=1050.0);

        Self {
            date,
            station,
            temperature,
            pressure,
        }
    }

    fn to_csv_line(&self) {
        println!(
            "{},{},{:.1},{:.1}",
            self.date,
            self.station_to_string(),
            self.temperature,
            self.pressure
        )
    }

    fn station_to_string(&self) -> &str {
        match self.station {
            Station::StationA => "StationA",
            Station::StationB => "StationB",
            Station::StationC => "StationC",
            Station::StationD => "StationD",
            Station::StationE => "StationE",
        }
    }
}

fn generate_weather_record() -> WeatherRecord {
    WeatherRecord::new()
}

fn generate_random_date() -> String {
    let year = rand::rng().random_range(2020..=2025);
    let month = rand::rng().random_range(1..=12);
    let day = match month {
        1 | 3 | 5 | 7 | 8 | 10 | 12 => rand::rng().random_range(1..=31),
        2 => rand::rng().random_range(1..=28),
        _ => rand::rng().random_range(1..=30),
    };

    format!("{:04}-{:02}-{:02}", year, month, day)
}

fn main() {
    let nb_records = rand::rng().random_range(10..=20);
    let mut records: Vec<WeatherRecord> = vec![];

    loop {
        if records.len() >= nb_records {
            break;
        };
        let rec = generate_weather_record();
        records.push(rec);
    }

    println!("Date,Station,Temperature,Pressure");
    for r in records {
        r.to_csv_line();
    }
}
