use rand::Rng;
 #[derive(Clone, Copy)]
enum StationType {
    StationA,
    StationB,
    StationC,
    StationD,
    StationE,
}
impl   StationType {
    fn as_string(&self) -> &str {
        match self {
            StationType::StationA => "StationA",
            StationType::StationB => "StationB",
            StationType::StationC => "StationC",
            StationType::StationD => "StationD",
            StationType::StationE => "StationE",
        }
    }
    
}

struct WeatherRecord{
    date: String,
    station: StationType,
    temperature: f32,
    pressure: f32,
}
impl WeatherRecord {
    fn to_csv_line(&self) -> String {
        format!("{},{},{:.1},{:.1}", self.date, self.station.as_string(), self.temperature, self.pressure)
    }
}

fn generate_weather_record() -> WeatherRecord {
    let mut rng = rand::rng();
    let stations = [
        StationType::StationA,
        StationType::StationB,
        StationType::StationC,
        StationType::StationD,
        StationType::StationE,
    ];
    let station = stations[rng.random_range(0..stations.len())];
    let temperature = rng.random_range(-100.0..401.0)/10.0;
    let pressure = rng.random_range(9800.0..10501.0)/10.0;
    WeatherRecord {
        date: generate_random_date(),
        station,
        temperature,
        pressure,
    }
}
    


fn generate_random_date()-> String {
    let mut rng = rand::rng();
    let year = rng.random_range(2020..=2025);
    let month = rng.random_range(1..=12);
    if month == 2 {
        let day = rng.random_range(1..=28);
        return format!("{:04}-{:02}-{:02}", year, month, day);
    }
    else if month == 4 || month == 6 || month == 9 || month == 11 {
        let day = rng.random_range(1..=30);
        return format!("{:04}-{:02}-{:02}", year, month, day);
    }
    let day = rng.random_range(1..=31);
    format!("{:04}-{:02}-{:02}", year, month, day)
}

fn main() { 
    let entete = "Date,Station,Temperature,Pressure";
    let roll = rand::rng().random_range(10..=20);
    println!("{}", entete);
    for _ in 0..roll {
        let record = generate_weather_record();
        println!("{}", record.to_csv_line());
       

    }
}
