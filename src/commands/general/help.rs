use crate::serenity_init::{BotData, Context, Error};
use crate::utils::bot_info::{bot_avatar, bot_name};

use std::collections::BTreeMap;

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
        Some(cm_ca) => embed = help_one(ctx, cat, &mut embed, cm_ca).await?,
        None => embed = help_all(ctx, cat, &mut embed).await?,
    }

    if let Some(avatar_url) = bot_avatar(ctx) {
        embed = embed.thumbnail(avatar_url);
    }

    let timestamp: serenity::Timestamp = chrono::Utc::now().to_rfc3339().parse()?;
    embed = embed.title(format!("Help for {}", bot_name(ctx)));
    embed = embed.timestamp(timestamp);

    let msg = serenity::CreateMessage::new().embed(embed);

    if let Err(why) = ctx.channel_id().send_message(ctx.http(), msg).await {
        eprintln!("{why}");
    }

    Ok(())
}

async fn help_all<'aa>(
    ctx: Context<'_>,
    c: BTreeMap<Option<String>, Vec<&poise::Command<BotData, Error>>>,
    e: &'aa mut serenity::CreateEmbed,
) -> Result<serenity::CreateEmbed, Error> {
    let mut ee = e.clone();
    for category in c {
        ee = ee.field(category.0.unwrap_or("Uncategorised".to_string()), "", false);
        for command in category.1 {
            ee = ee.field("", format!("{}{}", ctx.prefix(), command.name), false);
        }
    }

    Ok(ee)
}

async fn help_one<'aa>(
    ctx: Context<'_>,
    c: BTreeMap<Option<String>, Vec<&poise::Command<BotData, Error>>>,
    e: &'aa mut serenity::CreateEmbed,
    cm_ca: String,
) -> Result<serenity::CreateEmbed, Error> {
    let mut ee = e.clone();
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
            ee = ee.field(
                ca.0.clone().unwrap_or("Uncategorised".to_string()),
                "",
                false,
            );

            for cm in ca.1 {
                ee = ee.field("", format!("{}{}", ctx.prefix(), cm.name), false);
            }

            if ca.1.len() == 0 {
                ee = ee.field("", "No commands for this category", false);
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
                    ee = ee.field("", format!("{}{}", ctx.prefix(), cmd.name), false);
                    ee = ee.field(
                        "",
                        format!(
                            "{}",
                            cmd.description
                                .clone()
                                .unwrap_or("No description".to_string())
                        ),
                        false,
                    );
                }
                None => {
                    ee = ee.field("", format!("Command {} not found", cm_ca), false);
                }
            }
        }
    }

    Ok(ee)
}
