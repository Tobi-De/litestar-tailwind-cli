# original code by https://github.com/cofin


from __future__ import annotations

import argparse
import logging
import platform
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

TAILWIND_CLI_VERSION = "latest"
URL_BASE = "https://github.com/tailwindlabs/tailwindcss"

logger = logging.getLogger("tailwind-cli")


def get_asset_url(version: str, asset_name: str) -> str:
    if version.lower() == "latest":
        return f"{URL_BASE}/releases/latest/download/{asset_name}"
    return f"{URL_BASE}/releases/download/{version}/{asset_name}"


def asset_name(os_type: str, architecture: str) -> str:
    """Formats target name for provided OS name and CPU architecture."""
    extension = ".exe" if os_type == "windows" else ""
    if architecture == "amd64":
        return f"tailwindcss-{os_type}-x64{extension}"
    if architecture == "x86_64":
        return f"tailwindcss-{os_type}-x64{extension}"
    if architecture == "arm64":
        return f"tailwindcss-{os_type}-arm64{extension}"
    if architecture == "aarch64":
        return f"tailwindcss-{os_type}-arm64{extension}"
    raise Exception("Unknown architecture.")


def download_asset(options: argparse.Namespace) -> None:
    version_to_install = options.version_to_install if options.version_to_install is not None else TAILWIND_CLI_VERSION
    os_type = platform.system().lower().replace("win32", "windows").replace("darwin", "macos")
    asset_url = get_asset_url(
        version=version_to_install,
        asset_name=asset_name(os_type=os_type, architecture=platform.machine()),
    )
    file_name = Path(asset_url).name
    bin_path = Path(sys.prefix) / "bin"
    with tempfile.TemporaryDirectory() as app_temp_dir:
        logger.info("Downloading tailwind from %s", asset_url)
        extension = ".exe" if os_type == "windows" else ""
        subprocess.run(["/usr/bin/env", "wget", asset_url, "-O", f"{app_temp_dir}/{file_name}"], check=False)
        tailwind_cli = Path(shutil.copy(f"{app_temp_dir}/{file_name}", bin_path / f"tailwind-cli{extension}"))
        tailwind_cli.chmod(tailwind_cli.stat().st_mode | stat.S_IEXEC)
        logger.info("Installed to %s", tailwind_cli)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Install Tailwind CLI")
    parser.add_argument("--version-to-install", required=False)
    args = parser.parse_args()
    download_asset(args)
