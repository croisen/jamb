from pathlib import Path
from urllib.request import urlretrieve
import logging
import platform
import shutil

from patoolib import extract_archive

WINDOWS_BUILD = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z"

LINUX_BUILD_AMD32 = (
    "https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-i686-static.tar.xz"
)
LINUX_BUILD_AMD64 = (
    "https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz"
)
LINUX_BUILD_ARM64 = (
    "https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-arm64-static.tar.xz"
)

MACOS_BUILD_AMD64 = [
    "https://evermeet.cx/ffmpeg/ffmpeg-118086-g8272d34377.7z",
    "https://evermeet.cx/ffmpeg/ffprobe-118086-g8272d34377.7z",
    "https://evermeet.cx/ffmpeg/ffplay-117286-g262e6f8430.7z",
]

logger = logging.getLogger(__name__)


def download_ffmpeg(ffmpeg_dir: Path) -> Path:
    plat = platform.system()
    arch = platform.machine()

    match plat:
        case "Windows":
            return download_win(ffmpeg_dir)
        case "Linux":
            return download_lin(ffmpeg_dir, arch)
        case "Mac":
            pass
        case _:
            logger.error(f"Unsupported platform: {plat}")
            raise Exception("Unknown platform to download ffmpeg for")


def download_win(dir: Path) -> Path:
    d = dir / "windows"
    d.mkdir(parents=True, exist_ok=True)
    f = d / "ffmpeg.7z"
    fe = d / "ffmpeg.exe"
    if fe.exists():
        return fe

    logger.info(f"Now retrieving ffmpeg from: {WINDOWS_BUILD}")
    urlretrieve(WINDOWS_BUILD, f)
    extract_archive(str(f), outdir=str(d))
    extracted = d.glob("*/ffmpeg.exe").__next__()
    shutil.copy2(extracted, d)
    return fe


def download_lin(dir: Path, arch: str) -> Path:
    d = dir / "linux"
    d.mkdir(parents=True, exist_ok=True)
    f = d / "ffmpeg.tar.xz"

    fe = d / "ffmpeg"
    if fe.exists():
        return fe

    match arch:
        case "i386":
            logger.info(f"Now retrieving ffmpeg from: {LINUX_BUILD_AMD32}")
            urlretrieve(LINUX_BUILD_AMD32, f)
        case "x86_64":
            logger.info(f"Now retrieving ffmpeg from: {LINUX_BUILD_AMD64}")
            urlretrieve(LINUX_BUILD_AMD64, f)
        case "arm64":
            logger.info(f"Now retrieving ffmpeg from: {LINUX_BUILD_ARM64}")
            urlretrieve(LINUX_BUILD_ARM64, f)
        case _:
            logger.error(f"Unsupported architecture: {arch}")
            raise Exception("Unknown architecture to download ffmpeg for")

    extract_archive(str(f), outdir=str(d))
    extracted = d.glob("*/ffmpeg").__next__()
    shutil.copy2(extracted, d)

    return fe
