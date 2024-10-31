use crate::serenity_init::Context;

use poise::serenity_prelude as serenity;

pub fn bot_name(ctx: Context<'_>) -> String {
    ctx.cache().current_user().name.clone()
}

pub fn bot_avatar(ctx: Context<'_>) -> Option<String> {
    ctx.cache().current_user().avatar_url().clone()
}

pub fn bot_add_time(embed: serenity::CreateEmbed) -> serenity::CreateEmbed {
    let timestamp: serenity::Timestamp = chrono::Utc::now().to_rfc3339().parse().unwrap();
    let e = embed.timestamp(timestamp);
    e
}
