use crate::serenity_init::Context;

pub fn bot_name(ctx: Context<'_>) -> String {
    ctx.cache().current_user().name.clone()
}

pub fn bot_avatar(ctx: Context<'_>) -> Option<String> {
    ctx.cache().current_user().avatar_url().clone()
}
