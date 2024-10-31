use crate::serenity_init::{Context, Error};

use log::{info, warn};

#[poise::command(category = "Admin", slash_command, prefix_command, guild_only)]
pub async fn register(ctx: Context<'_>) -> Result<(), Error> {
    match ctx.framework().options().owners.get(&ctx.author().id) {
        Some(_) => {
            warn!(
                "Command register have been invoked by {}",
                ctx.author().name
            );
            info!("Registering commands...");
            for i in 0..ctx.framework().options().commands.len() {
                info!("Command: {}", ctx.framework().options().commands[i].name);
            }

            poise::builtins::register_globally(ctx, &ctx.framework().options().commands).await?;
        }
        None => {
            warn!(
                "Command register have been invoked by {} who do not have permission",
                ctx.author().name
            );
        }
    }

    Ok(())
}
