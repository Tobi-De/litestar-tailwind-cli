# original code by https://github.com/cofin
from __future__ import annotations

import platform
import shutil
import stat
import tempfile
import urllib.request
from contextlib import contextmanager
from pathlib import Path

from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TextColumn

URL_BASE = "https://github.com/tailwindlabs/tailwindcss"
OS_TYPE = platform.system().lower().replace("win32", "windows").replace("darwin", "macos")
ARCHITECTURE = platform.machine()


def get_asset_url(version: str) -> str:
    asset_name_ = asset_name()
    if version.lower() == "latest":
        return f"{URL_BASE}/releases/latest/download/{asset_name_}"
    return f"{URL_BASE}/releases/download/{version}/{asset_name_}"


class UnknownArchitectureError(Exception):
    pass


def asset_name() -> str:
    """Formats target name for provided OS name and CPU ARCHITECTURE."""
    extension = ".exe" if OS_TYPE == "windows" else ""
    if ARCHITECTURE in ("amd64", "x86_64"):
        return f"tailwindcss-{OS_TYPE}-x64{extension}"
    if ARCHITECTURE in ("arm64", "aarch64"):
        return f"tailwindcss-{OS_TYPE}-arm64{extension}"
    msg = f"{OS_TYPE}, {ARCHITECTURE}"
    raise UnknownArchitectureError(msg)


def download_asset(asset_url: str, tailwind_cli_bin: str | Path) -> Path:
    file_name = Path(asset_url).name
    with tempfile.TemporaryDirectory() as app_temp_dir:
        output_file = f"{app_temp_dir}/{file_name}"
        with urllib.request.urlopen(asset_url) as response, open(output_file, "wb") as out_file:
            data = response.read()
            out_file.write(data)

        tailwind_cli = Path(shutil.copy(output_file, tailwind_cli_bin))
        tailwind_cli.chmod(tailwind_cli.stat().st_mode | stat.S_IEXEC)
    return tailwind_cli


@contextmanager
def simple_progress(description: str, display_text="[progress.description]{task.description}"):
    progress = Progress(SpinnerColumn(), TextColumn(display_text), transient=True)
    progress.add_task(description=description, total=None)
    try:
        progress.start()
        yield
    finally:
        progress.stop()
