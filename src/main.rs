mod args;
mod commands;
mod config;
mod serenity_init;
mod utils;

use clap::Parser;
use fern::colors::{Color, ColoredLevelConfig};
use fern::Dispatch as LogDispatch;

static COLORS: ColoredLevelConfig = ColoredLevelConfig {
    warn: Color::Yellow,
    info: Color::Green,
    error: Color::Red,
    trace: Color::Blue,
    debug: Color::Cyan,
};

#[tokio::main]
async fn main() {
    LogDispatch::new()
        .format(|out, msg, record| {
            out.finish(format_args!(
                "[{} {} {}] {}",
                chrono::Utc::now().format("%b %d %Y - %H:%M:%S"),
                COLORS.color(record.level()),
                record.target(),
                msg
            ))
        })
        .level(log::LevelFilter::Warn)
        .level_for("jamb", log::LevelFilter::Info)
        .chain(std::io::stdout())
        .apply()
        .unwrap();

    let bot_args = args::BotArgs::parse();
    let o_bot_config = config::make_config(&bot_args.config_path);

    if o_bot_config.is_none() {
        eprintln!("Error reading config file: {}", bot_args.config_path);
        return;
    }

    let bot_config = o_bot_config.unwrap();
    serenity_init::init_run(bot_config).await;
}
