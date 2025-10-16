use rand::Rng;

fn main() {
    println!("Date,Station,Temperature,Pressure");

    let mut records = Vec::<WeatherRecord>::new();

    for i in 0..19 {
        records.push(generate_weather_record());
        println!("{}",records[i].to_csv_line());
    }

}

enum StationType {
    StationA,
    StationB,
    StationC,
    StationD,
    StationE,
}

fn station_type_to_string(var:&StationType) -> String {
    match var {
        StationType::StationA => {
            String::from("StationA")
        }

        StationType::StationB => {
            String::from("StationB")
        }

        StationType::StationC => {
            String::from("StationC")
        }

        StationType::StationD => {
            String::from("StationD")
        }

        StationType::StationE => {
            String::from("StationE")
        }
    }
}

pub struct WeatherRecord {
    pub date: String,
    pub station: StationType,
    pub temperature: f32,
    pub pressure: f32
}

/*impl WeatherRecord {
    pub fn new (date:String, station:StationType, temp:f32, pressure:f32) ->Self {
        Self {
            date:date,
            station:station,
            temperature:temp,
            pressure:pressure
        }
    }
}
*/
impl WeatherRecord {
    pub fn to_csv_line(&self) -> String {
        format!("{},{},{},{}", 
            self.date, 
            station_type_to_string(&self.station),
            self.temperature,
            self.pressure
        )
    }
}



fn gen_rand_date() -> String {
    let mois_30 = vec!["04","06","09","11"];
    let mois_31=vec!["01","03","05","07","08","10","12"];
    let mois = vec!["01","02","03","04","05","06","07","08","09","10","11","12"];

    let mut rng = rand::thread_rng();

    let month = mois[rng.gen_range(0..11)];

    let day = 0;

    if mois_30.contains(&month) {
        let day = rng.gen_range(1..30);

    } else if mois_31.contains(&month) {
        let day =rng.gen_range(1..31);
    } else {
        let day = rng.gen_range(1..28);
    }

    let year = rng.gen_range(2020..2025);

    if day < 10 {
        format!("{}-{}-0{}", year, month, day)
    } else {
        format!("{}-{}-{}", year, month, day)
    }
}


fn generate_weather_record() -> WeatherRecord {
    let date = gen_rand_date();
    let mut station= StationType::StationA;

    let mut rng = rand::thread_rng();

    let rand_station = rng.gen_range(0..4);

    if rand_station ==0 {
        station = StationType::StationA;
    } else if rand_station ==1 {
        station = StationType::StationB;
    } else if rand_station ==2 {
        station= StationType::StationC;
    } else if rand_station == 3{
        station = StationType::StationD;
    } else {
        station=StationType::StationE;
    }

    let temp:f32 = rng.gen_range(-10.0..40.0);
    let pressure:f32 = rng.gen_range(980.0..1050.0);

    WeatherRecord { date: date, station: station, temperature: temp, pressure: pressure }

}