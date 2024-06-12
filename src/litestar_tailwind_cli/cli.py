from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING

from click import group
from litestar.cli._utils import LitestarGroup
from litestar_tailwind_cli.utils import asset_name
from litestar_tailwind_cli.utils import download_asset
from litestar_tailwind_cli.utils import get_asset_url
from litestar_tailwind_cli.utils import simple_progress
from rich import print as rprint

if TYPE_CHECKING:
    from litestar import Litestar


@group(cls=LitestarGroup, name="tailwind")
def tailwind_group():
    """Manage tailwind tasks."""


@tailwind_group.command(name="init", help="")
def tailwind_init(app: Litestar):
    from litestar_tailwind_cli import TailwindCLIPlugin

    plugin = app.plugins.get(TailwindCLIPlugin)
    if not plugin.tailwind_cli_is_installed:
        asset_url = get_asset_url(
            version=plugin.tailwind_version,
            asset_name=asset_name(),
        )
        with simple_progress(description=f"[blue]Downloading tailwind from {asset_url}"):
            tailwind_cli = download_asset(
                asset_url=asset_url,
                tailwind_cli_bin=plugin.tailwind_cli_bin,
            )
        rprint(f"[green]Installed to {tailwind_cli}")

    subprocess.run([plugin.tailwind_cli_bin, "init"], check=False)


def run_tailwind_watch_process():
    pass


@tailwind_group.command(name="watch", help="")
def tailwind_watch():
    pass


@tailwind_group.command(name="build", help="")
def tailwind_build():
    pass
