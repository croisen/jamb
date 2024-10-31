use crate::serenity_init::{Context, Error};

use log::warn;

#[poise::command(category = "Admin", slash_command, prefix_command, guild_only)]
pub async fn logout(ctx: Context<'_>) -> Result<(), Error> {
    match ctx.framework().options().owners.get(&ctx.author().id) {
        Some(_) => {
            ctx.reply("Now logging out").await?;
            warn!(
                "Logout have been invoked by {}#{:#?}",
                ctx.author().name,
                ctx.author().discriminator
            );
            // Had to ask Gemini about this
            // Though there are still some stuff that is left over
            // When exiting via main
            ctx.framework().shard_manager().shutdown_all().await;
        }
        None => {
            ctx.reply("You can't make me logout").await?;
            warn!(
                "Logout have been invoked by {}#{:#?} without permission",
                ctx.author().name,
                ctx.author().discriminator
            );
        }
    }

    Ok(())
}
