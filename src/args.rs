use clap::Parser;

#[derive(Parser, Debug)]
#[command(version,  about, long_about = None)]
pub struct BotArgs {
    #[arg(short, long, default_value = "config.json")]
    pub config_path: String,
}
