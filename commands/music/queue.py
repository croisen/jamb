from typing import Optional, List, Self
import random
import time

from utils.yt_vid import Video


class Queue:
    LS_NORMAL = 1
    LS_LOOP_1 = 2
    LS_LOOP_A = 3

    def __init__(self, guild_id: int, channel_id: int) -> Self:
        self.guild_id: int = guild_id
        self.channel_id: int = channel_id
        self.last_play_time: int = 0

        self.currently_playing: Optional[Video] = None
        self.queue: List[Video] = []
        self.loop_state: int = self.LS_NORMAL

    def shuffle(self) -> None:
        random.shuffle(self.queue)

    def next(self) -> None:
        self.last_play_time = time.time()
        match self.loop_state:
            case self.LS_NORMAL:
                self.currently_playing = self.queue.pop(0)
            case self.LS_LOOP_1:
                return
            case self.LS_LOOP_A:
                self.queue.append(self.currently_playing)
                self.currently_playing = self.queue.pop(0)

    def add(self, vid: Video) -> None:
        self.queue.append(vid)
