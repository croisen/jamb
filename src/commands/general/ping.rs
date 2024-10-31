use crate::serenity_init::{Context, Error};

#[poise::command(category = "General", slash_command, prefix_command, guild_only)]
pub async fn ping(ctx: Context<'_>) -> Result<(), Error> {
    ctx.reply("Pong!").await?;
    Ok(())
}
