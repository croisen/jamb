use poise::serenity_prelude as serenity;

#[derive(Clone)]
pub struct Song {
    pub title: String,
    pub requester: serenity::UserId,
    pub raw_music_link: String,
    pub raw_thumbnail_link: String,
}

pub struct Queue {
    pub guild_id: serenity::GuildId,
    pub currently_playing: Option<Song>,
    pub song_queue: Vec<Song>,
    pub shuffle: bool,
    pub loop_one: bool,
    pub loop_all: bool,
}

impl Queue {
    pub fn new() -> Self {
        Self {
            ..Default::default()
        }
    }
}

impl Song {
    pub fn new() -> Self {
        Self {
            ..Default::default()
        }
    }
}

impl Default for Song {
    fn default() -> Self {
        Self {
            title: "None".to_string(),
            raw_music_link: "".to_string(),
            raw_thumbnail_link: "".to_string(),
            requester: serenity::UserId::new(1),
        }
    }
}

impl Default for Queue {
    fn default() -> Self {
        Self {
            guild_id: serenity::GuildId::new(1),
            currently_playing: None,
            shuffle: false,
            loop_all: false,
            loop_one: false,
            song_queue: vec![],
        }
    }
}
