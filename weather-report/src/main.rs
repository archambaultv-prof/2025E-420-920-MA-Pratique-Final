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

fn main() {
    // Test temporaire
    let s = StationType::StationC;
    println!("{}", s.to_string());
}
