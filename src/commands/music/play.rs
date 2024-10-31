use crate::commands::music::{Queue, Song};
use crate::serenity_init::{BotData, Context, Error};
use crate::utils::bot_info::{bot_add_time, bot_avatar};

use log::warn;
use poise::serenity_prelude as serenity;

#[poise::command(category = "Music", slash_command, prefix_command, guild_only)]
pub async fn play(ctx: Context<'_>, song: Vec<String>) -> Result<(), Error> {
    let bot_data: &BotData = ctx.data();
    let mut embed = serenity::CreateEmbed::new();
    let song_name = song.join(" ");

    embed = embed.title(format!("Music Queue of {}", ctx.guild().unwrap().name));
    embed = bot_add_time(embed);
    if let Some(avatar) = bot_avatar(ctx) {
        embed = embed.thumbnail(avatar);
    }

    embed = embed.field("Added:", &song_name, false);

    bot_data.music_queue.lock().unwrap().insert(
        ctx.guild_id().unwrap(),
        Queue {
            guild_id: ctx.guild_id().unwrap(),
            song_queue: vec![Song {
                title: song_name,
                requester: ctx.author().id,
                ..Default::default()
            }],
            ..Default::default()
        },
    );

    let msg = serenity::CreateMessage::new().embed(embed);
    if let Err(why) = ctx.channel_id().send_message(ctx.http(), msg).await {
        warn!("Failed to send message: {why}");
    }

    Ok(())
}
