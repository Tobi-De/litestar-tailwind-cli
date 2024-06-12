from __future__ import annotations

import subprocess
from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING

from click import group
from litestar.cli._utils import LitestarGroup
from litestar_tailwind_cli.utils import download_asset
from litestar_tailwind_cli.utils import get_asset_url
from litestar_tailwind_cli.utils import simple_progress
from rich import print as rprint

if TYPE_CHECKING:
    from litestar import Litestar


@group(cls=LitestarGroup, name="tailwind")
def tailwind_group():
    """Manage tailwind tasks."""


@tailwind_group.command(name="init", help="Initialize tailwind configuration.")
def tailwind_init(app: Litestar):
    from litestar_tailwind_cli import TailwindCLIPlugin

    plugin = app.plugins.get(TailwindCLIPlugin)
    if not plugin.tailwind_cli_is_installed:
        asset_url = get_asset_url(version=plugin.cli_version)
        with simple_progress(description=f"[blue]Downloading tailwind from {asset_url}"):
            tailwind_cli = download_asset(
                asset_url=asset_url,
                tailwind_cli_bin=plugin.cli_path,
            )
        rprint(f"[green]Installed to {tailwind_cli}")

    subprocess.run([plugin.cli_path, "init"], check=False)


class TailwindCLINotInstalledError(Exception):
    def __init__(self, message="Tailwind CLI is not installed, run `litestar tailwind init` to install it."):
        super().__init__(message)


def run_tailwind_watch(cli_path: Path | str, src_css: Path | str, dist_css: Path | str):
    with suppress(KeyboardInterrupt):
        subprocess.run(
            [
                cli_path,
                "--input",
                src_css,
                "--output",
                dist_css,
                "--watch",
            ],
            check=False,
        )


@tailwind_group.command(name="watch", help="Run tailwind watch.")
def tailwind_watch(app: Litestar):
    from litestar_tailwind_cli import TailwindCLIPlugin

    plugin = app.plugins.get(TailwindCLIPlugin)
    if not plugin.tailwind_cli_is_installed:
        raise TailwindCLINotInstalledError

    src_css = Path(plugin.src_css)
    if not src_css.exists():
        src_css.parent.mkdir(parents=True, exist_ok=True)
        src_css.touch()
        src_css.write_text("@tailwind base;\n@tailwind components;\n@tailwind utilities;")
    run_tailwind_watch(cli_path=plugin.cli_path, src_css=plugin.src_css, dist_css=plugin.dist_css)


@tailwind_group.command(name="build", help="")
def tailwind_build(app: Litestar):
    from litestar_tailwind_cli import TailwindCLIPlugin

    plugin = app.plugins.get(TailwindCLIPlugin)
    if not plugin.tailwind_cli_is_installed:
        raise TailwindCLINotInstalledError
