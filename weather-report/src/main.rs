use rand::Rng;
use chrono::Local;

fn main() {
    // En-tête CSV
    println!("Date,Station,Temperature,Pressure");

    let stations = ["StationA", "StationB", "StationC", "StationD"];
    let mut rng = rand::thread_rng();

    let date = Local::now().format("%Y-%m-%d").to_string();

    // Génère 10 lignes aléatoires
    for _ in 0..10 {
        let station = stations[rng.gen_range(0..stations.len())];
        let temperature: f32 = rng.gen_range(-10.0..35.0); // °C
        let pressure: f32 = rng.gen_range(980.0..1030.0);  // hPa
        println!("{},{},{:.1},{:.1}", date, station, temperature, pressure);
    }
}
