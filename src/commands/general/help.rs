use crate::serenity_init::{BotData, Context, Error};
use crate::utils::bot_info::{bot_add_time, bot_avatar, bot_name};

use std::collections::BTreeMap;

use log::warn;
use poise::serenity_prelude as serenity;

#[poise::command(category = "General", slash_command, prefix_command, guild_only)]
pub async fn help(ctx: Context<'_>, cmd_or_cat: Option<String>) -> Result<(), Error> {
    let mut cat: BTreeMap<Option<String>, Vec<&poise::Command<BotData, Error>>> = BTreeMap::new();
    for i in 0..ctx.framework().options().commands.len() {
        let cc = &ctx.framework().options().commands[i];
        match cat.get_mut(&cc.category) {
            Some(cvec) => {
                cvec.push(cc);
            }
            None => {
                cat.insert(cc.category.clone(), vec![cc]);
            }
        }
    }

    let mut embed = serenity::CreateEmbed::new();
    match cmd_or_cat {
        Some(cm_ca) => embed = help_one(cat, embed, cm_ca).await?,
        None => embed = help_all(cat, embed).await?,
    }

    if let Some(avatar_url) = bot_avatar(ctx) {
        embed = embed.thumbnail(avatar_url);
    }

    embed = embed.title(format!("Help for {}", bot_name(ctx)));
    embed = bot_add_time(embed);

    let msg = serenity::CreateMessage::new().embed(embed);
    if let Err(why) = ctx.channel_id().send_message(ctx.http(), msg).await {
        warn!("Failed to send message: {why}");
    }

    Ok(())
}

async fn help_all(
    c: BTreeMap<Option<String>, Vec<&poise::Command<BotData, Error>>>,
    mut e: serenity::CreateEmbed,
) -> Result<serenity::CreateEmbed, Error> {
    for category in c {
        let mut commands = "".to_string();
        let mut c_iter = category.1.iter();
        let mut cc = c_iter.next();
        // No need to check if there's something as a command should exist
        // as long as the category exists
        loop {
            commands += &cc.unwrap().name;
            cc = c_iter.next();
            if cc.is_some() {
                commands += ", ";
            } else {
                break;
            }
        }

        e = e.field(
            category.0.unwrap_or("Uncategorised".to_string()),
            "`".to_string() + &commands + "`",
            false,
        );
    }

    Ok(e)
}

async fn help_one(
    c: BTreeMap<Option<String>, Vec<&poise::Command<BotData, Error>>>,
    mut e: serenity::CreateEmbed,
    cm_ca: String,
) -> Result<serenity::CreateEmbed, Error> {
    let mut cget = None;
    for cat in &c {
        if cat
            .0
            .clone()
            .unwrap_or("Uncategorised".to_string())
            .eq_ignore_ascii_case(&cm_ca)
        {
            cget = Some(cat);
        }
    }

    match cget {
        Some(ca) => {
            let mut commands = "".to_string();
            let mut c_iter = ca.1.iter();
            let mut cc = c_iter.next();
            // No need to check if there's something as a command should exist
            // as long as the category exists
            loop {
                commands += &cc.unwrap().name;
                cc = c_iter.next();
                if cc.is_some() {
                    commands += ", ";
                } else {
                    break;
                }
            }

            if ca.1.len() == 0 {
                e = e.field(
                    ca.0.clone().unwrap_or("Uncategorised".to_string()),
                    "No commands for this category",
                    false,
                );
            } else {
                e = e.field(
                    ca.0.clone().unwrap_or("Uncategorised".to_string()),
                    "`".to_string() + &commands + "`",
                    false,
                );
            }
        }
        None => {
            let mut cm = None;
            for ca in c {
                for cm_com in ca.1 {
                    if cm_com.name.eq_ignore_ascii_case(&cm_ca) {
                        cm = Some(cm_com);
                        break;
                    }
                }
            }

            match cm {
                Some(cmd) => {
                    e = e.field(
                        cmd.name.clone(),
                        format!(
                            "{}",
                            cmd.help_text.clone().unwrap_or("No help info".to_string())
                        ),
                        false,
                    );
                }
                None => {
                    e = e.field(cm_ca, "Command not found", false);
                }
            }
        }
    }

    Ok(e)
}
