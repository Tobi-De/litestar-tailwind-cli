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
    from litestar_tailwind_cli import TailwindCLIPlugin


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

    config_file = Path(plugin.config_file)
    if config_file.exists():
        rprint(f"[yellow]Configuration file already exists at {config_file}")
        return
    config_file.write_text(DEFAULT_TAILWIND_CONFIG)
    rprint(f"[green]Configuration file created at {config_file}")

    src_css = Path(plugin.src_css)
    if not src_css.exists():
        src_css.parent.mkdir(parents=True, exist_ok=True)
        src_css.write_text("@tailwind base;\n@tailwind components;\n@tailwind utilities;")
        rprint(f"[green]Created input css file at {src_css}")


class TailwindCLINotInstalledError(Exception):
    def __init__(
        self,
        message="Tailwind CLI is not installed, run `litestar tailwind init` to install it.",
    ):
        super().__init__(message)


def run_tailwind_watch(plugin: TailwindCLIPlugin):
    with suppress(KeyboardInterrupt):
        subprocess.run(
            [
                plugin.cli_path,
                "--input",
                plugin.src_css,
                "--output",
                plugin.dist_css,
                "--watch",
                "--config",
                plugin.config_file,
            ],
            check=False,
        )


@tailwind_group.command(name="watch", help="Start Tailwind CLI in watch mode during development.")
def tailwind_watch(app: Litestar):
    from litestar_tailwind_cli import TailwindCLIPlugin

    plugin = app.plugins.get(TailwindCLIPlugin)
    if not plugin.tailwind_cli_is_installed:
        raise TailwindCLINotInstalledError

    run_tailwind_watch(plugin=plugin)


# shamelessy copied from https://django-tailwind-cli.andrich.me/settings/#tailwindconfigjs
DEFAULT_TAILWIND_CONFIG = """/** @type {import('tailwindcss').Config} */
const plugin = require("tailwindcss/plugin");

module.exports = {
  content: [],
  theme: {
    extend: {},
  },
  plugins: [
    require("@tailwindcss/typography"),
    require("@tailwindcss/forms"),
    require("@tailwindcss/aspect-ratio"),
    require("@tailwindcss/container-queries"),
    plugin(function ({ addVariant }) {
      addVariant("htmx-settling", ["&.htmx-settling", ".htmx-settling &"]);
      addVariant("htmx-request", ["&.htmx-request", ".htmx-request &"]);
      addVariant("htmx-swapping", ["&.htmx-swapping", ".htmx-swapping &"]);
      addVariant("htmx-added", ["&.htmx-added", ".htmx-added &"]);
    }),
  ],
};
"""


@tailwind_group.command(name="build", help="Build a minified production ready CSS file.")
def tailwind_build(app: Litestar):
    from litestar_tailwind_cli import TailwindCLIPlugin

    plugin = app.plugins.get(TailwindCLIPlugin)
    if not plugin.tailwind_cli_is_installed:
        raise TailwindCLINotInstalledError

    subprocess.run(
        [
            plugin.cli_path,
            "--input",
            plugin.src_css,
            "--output",
            plugin.dist_css,
            "--config",
            plugin.config_file,
            "--minify",
        ],
        check=False,
    )
