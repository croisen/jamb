use crate::commands::*;
use crate::config::BotConfig;

use log::info;
use poise::serenity_prelude as serenity;

pub struct BotData {}

pub type Error = Box<dyn std::error::Error + Send + Sync>;
pub type Context<'a> = poise::Context<'a, BotData, Error>;

pub async fn init_run(conf: BotConfig) {
    let intents = serenity::GatewayIntents::all();
    let commands = vec![
        admin::logout(),
        admin::register(),
        general::eight_ball(),
        general::help(),
        general::ping(),
    ];

    let prefix_options = poise::PrefixFrameworkOptions {
        prefix: Some(conf.prefix),
        mention_as_prefix: true,
        ignore_bots: true,
        case_insensitive_commands: true,
        ..Default::default()
    };

    let framework = poise::Framework::<BotData, Error>::builder()
        .options(poise::FrameworkOptions {
            commands,
            prefix_options,
            initialize_owners: true,
            event_handler: |_ctx, ev, _fr_ctx, _bd| {
                match ev {
                    serenity::FullEvent::Ready { data_about_bot } => {
                        info!(
                            "Bot {}#{:#?} is now ready",
                            data_about_bot.user.name, data_about_bot.user.discriminator
                        );
                    }
                    _ => {}
                }

                Box::pin(async move { Ok(()) })
            },
            ..Default::default()
        })
        .setup(|_ctx, _ready, _fr| Box::pin(async move { Ok(BotData {}) }))
        .build();

    let client = serenity::ClientBuilder::new(conf.token, intents)
        .framework(framework)
        .await;
    client.unwrap().start().await.unwrap();
}
