use std::collections::BTreeMap;
use std::sync::{LazyLock, Mutex};
use std::time::SystemTime;

use crate::serenity_init::{Context, Error};
use crate::utils::xoshiro256::Xoshiro256;

#[derive(Clone, Copy)]
enum BotEightBallAnswer {
    Yes,
    No,
    Maybe,
    DontWannaAnswer,
    Dunno,
}

static QUESTIONS: LazyLock<Mutex<BTreeMap<String, BotEightBallAnswer>>> =
    LazyLock::new(|| Mutex::new(BTreeMap::new()));

#[poise::command(
    category = "General",
    rename = "8ball",
    slash_command,
    prefix_command,
    guild_only
)]
pub async fn eight_ball(ctx: Context<'_>, question: Vec<String>) -> Result<(), Error> {
    let mut x = Xoshiro256::new(
        SystemTime::now()
            .duration_since(SystemTime::UNIX_EPOCH)?
            .as_secs(),
    );

    let potential_answer = (x.next() % 5).into();
    if QUESTIONS.lock().unwrap().len() > 20 {
        QUESTIONS.lock().unwrap().pop_first();
    }

    let answer: BotEightBallAnswer = match QUESTIONS.lock().unwrap().get(&question.join(" ")) {
        Some(a) => a.to_owned(),
        None => {
            QUESTIONS
                .lock()
                .unwrap()
                .insert(question.join(" "), potential_answer);
            potential_answer
        }
    };

    let mut reply: String = "`".to_string() + &question.join(" ") + "`\n";
    match answer {
        BotEightBallAnswer::Yes => {
            reply += "Yes";
        }
        BotEightBallAnswer::No => {
            reply += "No";
        }
        BotEightBallAnswer::Maybe => {
            reply += "Maybe?";
        }
        BotEightBallAnswer::DontWannaAnswer => {
            reply += "I do not want to answer this one";
        }
        BotEightBallAnswer::Dunno => {
            reply += "I do not know";
        }
    }

    ctx.reply(reply).await?;
    Ok(())
}

impl From<u64> for BotEightBallAnswer {
    fn from(value: u64) -> Self {
        match value {
            0 => BotEightBallAnswer::Yes,
            1 => BotEightBallAnswer::No,
            2 => BotEightBallAnswer::Maybe,
            3 => BotEightBallAnswer::DontWannaAnswer,
            4 => BotEightBallAnswer::Dunno,
            _ => BotEightBallAnswer::Dunno,
        }
    }
}
