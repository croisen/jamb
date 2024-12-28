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

    final = ""
    ffmpeg_dir.mkdir(parents=True, exist_ok=True)
    if p_plat == "Windows":
        final = "ffmpeg.exe"
    elif p_plat == "Linux":
        final = "ffmpeg"
    elif p_plat == "Darwin":
        final = "ffmpeg"
    elif p_plat == "Android":
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
    if p_plat == "Windows":
        p = download_win(ffmpeg_dir, p_arch)
    elif p_plat == "Linux":
        p = download_lin(ffmpeg_dir, p_arch)
    elif p_plat == "Darwin":
        p = download_mac(ffmpeg_dir, p_arch)
    elif p_plat == "Android":
        p = download_lin(ffmpeg_dir, p_arch)
    else:
        _logger.error(f"Unknown platform type: {p_plat}")
        raise Exception(f"Unsupported platform: {p_plat} for ffmpeg autodownload")

    return p


def download_win(f: Path, arch: str) -> Path:
    url = ""
    if arch == "i386" or arch == "i686":
        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z"
    elif arch == "x86_64":
        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z"
    else:
        _logger.error(f"Unknown archiecture type: {arch}")
        raise Exception(f"Unsupported architecture: {arch} for ffmpeg autodownload")

    _logger.info(f"Downloading ffmpeg from {url}")
    urlretrieve(url, str(f / "ffmpeg.7z"))
    extract_archive(archive=str(f / "ffmpeg.7z"), outdir=str(f), verbosity=-1)
    ex = f.glob("*/bin/*")
    for extracted in f.glob("*/bin/*"):
        shutil.copy2(extracted, str(f))

    return f / "ffmpeg.exe"


def download_lin(f: Path, arch: str) -> Path:
    _logger.warning(
        "DNS resolutions for a static build of ffmpeg fails (due to static linking of glibc)"
    )
    _logger.warning(
        "Either install ffmpeg through your package manager or install nscd with your package manager"
    )
    url = ""
    if arch == "i386" or arch == "i686":
        url = "https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-i686-static.tar.xz"
    elif arch == "x86_64":
        url = "https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz"
    elif arch == "arm":
        url = "https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-armel-static.tar.xz"
    elif (
        arch == "aarch64"
        or arch == "aarch64_be"
        or arch == "armv8b"
        or arch == "armv81"
    ):
        url = "https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-armhf-static.tar.xz"
    else:
        _logger.error(f"Unknown archiecture type: {arch}")
        raise Exception(f"Unsupported architecture: {arch} for ffmpeg autodownload")

    _logger.info(f"Downloading ffmpeg from {url}")
    urlretrieve(url, str(f / "ffmpeg.tar.xz"))
    extract_archive(archive=str(f / "ffmpeg.tar.xz"), outdir=str(f), verbosity=-1)
    ex = f.glob("*/bin/*")
    for extracted in f.glob("*/ffmpeg"):
        shutil.copy2(extracted, str(f))

    return f / "ffmpeg"


def download_mac(f: Path, arch: str) -> Path:
    url = ""
    if arch == "i386" or arch == "i686":
        _logger.error(
            "Unsupported autodownload of ffmpeg in macos in 32 bit intel or amd cpus"
        )
    elif arch == "x86_64":
        url = "https://evermeet.cx/ffmpeg/ffmpeg-7.1.7z"
    else:
        _logger.error(f"Unknown archiecture type: {arch}")
        raise Exception(f"Unsupported architecture: {arch} for ffmpeg autodownload")

    _logger.info(f"Downloading ffmpeg from {url}")
    urlretrieve(url, str(f / "ffmpeg.7z"))
    extract_archive(archive=str(f / "ffmpeg.7z"), outdir=str(f), verbosity=-1)
    return f / "ffmpeg"
