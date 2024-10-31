use crate::commands::music::{Queue, Song};
use crate::serenity_init::{BotData, Context, Error};
use crate::utils::bot_info::{bot_add_time, bot_avatar};

use log::warn;
use poise::serenity_prelude as serenity;

#[poise::command(category = "Music", slash_command, prefix_command, guild_only)]
pub async fn queue(ctx: Context<'_>) -> Result<(), Error> {
    let bot_data: &BotData = ctx.data();
    let mut embed = serenity::CreateEmbed::new();

    embed = embed.title(format!("Music Queue of {}", ctx.guild().unwrap().name));
    embed = bot_add_time(embed);
    if let Some(avatar) = bot_avatar(ctx) {
        embed = embed.thumbnail(avatar);
    }

    match bot_data
        .music_queue
        .lock()
        .unwrap()
        .get(&ctx.guild_id().unwrap())
    {
        Some(queue) => {
            embed = embed.field(
                "Currently Playing:",
                queue
                    .currently_playing
                    .clone()
                    .unwrap_or(Song {
                        title: "None".to_string(),
                        ..Default::default()
                    })
                    .title
                    .clone(),
                false,
            );

            for (i, song) in queue.song_queue.iter().enumerate() {
                embed = embed.field(i.to_string(), song.title.clone(), true);
            }
        }
        None => {
            embed = embed.field("Currently Playing:", "None", false);
            embed = embed.field("", "No Songs in Queue", false);
        }
    }

    let msg = serenity::CreateMessage::new().embed(embed);
    if let Err(why) = ctx.channel_id().send_message(ctx.http(), msg).await {
        warn!("Failed to send message: {why}");
    }

    Ok(())
}
