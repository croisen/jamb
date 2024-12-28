from pathlib import Path
from urllib.request import urlretrieve
import logging
import platform
import shutil

from patoolib import extract_archive


_logger = logging.getLogger(__name__)


def download_phantomjs(phantomjs_dir: Path) -> Path:
    p_plat = platform.system()
    p_arch = platform.machine()

    final = ""
    phantomjs_dir.mkdir(parents=True, exist_ok=True)
    if p_plat == "Windows":
        final = "phantomjs.exe"
    elif p_plat == "Linux":
        final = "phantomjs"
    elif p_plat == "Darwin":
        final = "phantomjs"
    else:
        final = "phantomjs"
        _logger.error(f"Unknown platform type: {p_plat}")
        raise Exception(f"Unsupported platform: {p_plat} for phantomjs autodownload")

    pf = shutil.which(final)
    if pf:
        _logger.info(f"Found phantomjs in {pf}")
        return Path(pf)

    p = phantomjs_dir / final
    if p.exists():
        _logger.info(f"Found phantomjs in {p}")
        return p

    _logger.info("phantomjs not found and attempting auto download")
    if p_plat == "Windows":
        p = download_win(phantomjs_dir, p_arch)
    elif p_plat == "Linux":
        p = download_lin(phantomjs_dir, p_arch)
    elif p_plat == "Darwin":
        p = download_mac(phantomjs_dir, p_arch)
    else:
        _logger.error(f"Unknown platform type: {p_plat}")
        raise Exception(f"Unsupported platform: {p_plat} for phantomjs autodownload")

    return p


def download_win(f: Path, arch: str) -> Path:
    url = ""
    if arch == "i386" or arch == "i686":
        url = "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-windows.zip"
    elif arch == "x86_64":
        url = "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-windows.zip"
    else:
        _logger.error(f"Unknown archiecture type: {arch}")
        raise Exception(f"Unsupported architecture: {arch} for phantomjs autodownload")

    _logger.info(f"Downloading phantomjs from {url}")
    urlretrieve(url, str(f / "phantomjs.zip"))
    extract_archive(archive=str(f / "phantomjs.zip"), outdir=str(f), verbosity=-1)
    ex = f.glob("*/bin/*")
    for extracted in f.glob("*/bin/*"):
        shutil.copy2(extracted, str(f))

    return f / "phantomjs.exe"


def download_lin(f: Path, arch: str) -> Path:
    if arch == "i386" or arch == "i686":
        url = "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-i686.tar.bz2"
    elif arch == "x86_64":
        url = "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2"
    else:
        _logger.error(f"Unknown archiecture type: {arch}")
        raise Exception(f"Unsupported architecture: {arch} for phantomjs autodownload")

    _logger.info(f"Downloading phantomjs from {url}")
    urlretrieve(url, str(f / "phantomjs.tar.bz2"))
    extract_archive(archive=str(f / "phantomjs.tar.bz2"), outdir=str(f), verbosity=-1)
    ex = f.glob("*/bin/*")
    for extracted in f.glob("*/bin/*"):
        shutil.copy2(extracted, str(f))

    return f / "phantomjs"


def download_mac(f: Path, arch: str) -> Path:
    if arch == "i386" or arch == "i686":
        url = (
            "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-macosx.zip"
        )
    elif arch == "x86_64":
        url = (
            "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-macosx.zip"
        )
    else:
        _logger.error(f"Unknown archiecture type: {arch}")
        raise Exception(f"Unsupported architecture: {arch} for phantomjs autodownload")

    _logger.info(f"Downloading phantomjs from {url}")
    urlretrieve(url, str(f / "phantomjs.zip"))
    extract_archive(archive=str(f / "phantomjs.zip"), outdir=str(f), verbosity=-1)
    ex = f.glob("*/bin/*")
    for extracted in f.glob("*/bin/*"):
        shutil.copy2(extracted, str(f))

    return f / "phantomjs"
