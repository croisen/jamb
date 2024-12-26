from pathlib import Path
from urllib.request import urlretrieve
import logging
import platform
import shutil

from patoolib import extract_archive


_logger = logging.getLogger(__name__)


def download_ffmpeg(ffmpeg_dir: Path) -> Path:
    p_plat = platform.system()
    p_arch = platform.machine()

    url = ""
    name = "ffmpeg-master-latest-gpl"
    final = ""
    ffmpeg_dir.mkdir(parents=True, exist_ok=True)

    if p_plat == "Windows":
        url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win"
        final = "ffmpeg.exe"
    elif p_plat == "Linux":
        url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux"
        final = "ffmpeg"
    else:
        _logger.error(f"Unknown platform type: {p_plat}")
        raise Exception(f"Unsupported platform: {p_plat} for ffmpeg autodownload")

    pf = shutil.which(final)
    if pf:
        _logger.info(f"Found ffmpeg in {pf}")
        return Path(pf)

    p = ffmpeg_dir / final
    if p.exists():
        _logger.info(f"Found ffmpeg in {p}")
        return p

    _logger.info("FFmpeg not found and attempting auto download")
    if p_arch == "i386" or p_arch == "i686":
        _logger.error("32 bit Intel or AMD cpu builds are not supported")
        raise Exception(f"Unsupported architecture: {p_arch} for ffmpeg autodownload")
    elif p_arch == "x86_64":
        url += "64-gpl"
    else:
        _logger.error(f"Unknown archiecture type: {p_arch}")
        raise Exception(f"Unsupported architecture: {p_arch} for ffmpeg autodownload")

    if p_plat == "Windows":
        url += ".zip"
        name += ".zip"
    elif p_plat == "Linux":
        url += ".tar.xz"
        name += ".tar.xz"
    else:
        _logger.error(f"Unknown platform type: {p_plat}")
        raise Exception(f"Unsupported platform: {p_arch} for ffmpeg autodownload")

    _logger.info(f"Downloading ffmpeg from {url}")
    urlretrieve(url, str(ffmpeg_dir / name))
    extract_archive(archive=str(ffmpeg_dir / name), outdir=str(ffmpeg_dir))

    for extracted in ffmpeg_dir.glob("*/bin/*"):
        shutil.copy2(extracted, str(ffmpeg_dir))

    return p
