
use rand::Rng;




#[derive(Copy, Clone, Debug)]
enum StationType {StationA, StationB, StationC, StationD, StationE,}

struct WeatherRecord {
    date: String,
    station: StationType,
    temperature: f32,
    pressure: f32,
}

fn station_to_str(station: &StationType) -> String {
    match station {
        StationType::StationA => "StationA".to_string(),
        StationType::StationB => "StationB".to_string(),
        StationType::StationC => "StationC".to_string(),
        StationType::StationD => "StationD".to_string(),
        StationType::StationE => "StationE".to_string(),
    }
}

fn generate_random_date(rng: &mut rand::rngs::ThreadRng) -> String {
    let year = rng.gen_range(2023..=2025);
    let month = rng.gen_range(1..=12);
    let day = match month {
        2 => 28,
        4 | 6 | 9 | 11 => 30,
        _ => 31,
    };
    let day = rng.gen_range(1..=day);
    format!("{:04}-{:02}-{:02}", year, month, day)
}

fn generate_record(rng: &mut rand::rngs::ThreadRng) -> WeatherRecord {
    let stations = [
        StationType::StationA,
        StationType::StationB,
        StationType::StationC,
        StationType::StationD,
        StationType::StationE,
    ];
    WeatherRecord {
        date: generate_random_date(rng),
        station: stations[rng.gen_range(0..stations.len())],
        temperature: rng.gen_range(-30.0..=40.0),
        pressure: rng.gen_range(800.0..=1100.0),
    }
}

fn to_csv_line(record: &WeatherRecord) -> String {
    format!("{},{},{:.1},{:.1}",record.date,station_to_str(&record.station), record.temperature, record.pressure)
}
fn main() {

    let mut rng = rand::thread_rng();
    println!("Date, Station, Temperature, Pressure");

    let n = rng.gen_range(10..=20);
    for _ in 0..n {
        let record = generate_record(&mut rng);
        println!("{}", to_csv_line(&record))

    }
}

