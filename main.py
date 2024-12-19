#!/usr/bin/env python3

import asyncio

from utils import bot_config, ffmpeg, logger, path_stuff


async def main():
    sc_dir = path_stuff.get_script_dir(__file__)
    config_file = sc_dir / "config.json"
    log_dir = sc_dir / "logs"

    logger.setup_logging(log_dir)
    ffmpeg_path = ffmpeg.download_ffmpeg(sc_dir / "ffmpeg")
    bot = bot_config.CroiBot(config_file, ffmpeg_path)
    await bot.start_bot()


if __name__ == "__main__":
    asyncio.run(main())
