#!/usr/bin/env python3

import asyncio
import logging
import platform
import os

from utils import bot_config, ffmpeg, logger, path_stuff, phantomjs


async def main():
    sc_dir = path_stuff.get_script_dir(__file__)
    config_file = sc_dir / "config.json"
    log_dir = sc_dir / "logs"

    logger.setup_logging(log_dir)
    ffmpeg_path = ffmpeg.download_ffmpeg(sc_dir / "3rd_party" / "ffmpeg")
    phantomjs_path = phantomjs.download_phantomjs(sc_dir / "3rd_party" / "phantomjs")
    os.environ["PHANTOM_JS"] = str(phantomjs_path)

    if str(ffmpeg_path).startswith(str(sc_dir)) and platform.system() == "Linux":
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "Final warning: ffmpeg would crash with a static build when used by this bot"
        )
        _logger.warning(
            "Final warning: just install it via your package manager or nscd"
        )

    bot = bot_config.CroiBot(config_file, ffmpeg_path)
    await bot.start_bot()


if __name__ == "__main__":
    asyncio.run(main())
