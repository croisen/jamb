use std::fs::read_to_string;

use serde_json::{from_str, Value};

pub struct BotConfig {
    pub prefix: String,
    pub token: String,
}

pub fn make_config(config_path: &String) -> Option<BotConfig> {
    let data = read_to_string(config_path);
    if data.is_err() {
        eprint!("File: {}\n{}\n\n", config_path, data.unwrap_err());
        return None;
    }

    let json = from_str(&(data.unwrap()));
    if json.is_err() {
        eprint!("File: {}\n{}\n\n", config_path, json.unwrap_err());
        return None;
    }

    let c: Value = json.unwrap();
    let prefix = c["command-prefix"].as_str().unwrap_or("j!").to_string();
    let token = c["bot-token"].as_str().unwrap_or("No Token?").to_string();

    Some(BotConfig { prefix, token })
}
