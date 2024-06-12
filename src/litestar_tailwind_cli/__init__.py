# SPDX-FileCopyrightText: 2024-present Tobi DEGNON <tobidegnon@proton.me>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import TYPE_CHECKING

from litestar.plugins import CLIPlugin
from litestar_tailwind_cli.utils import OS_TYPE

if TYPE_CHECKING:
    from pathlib import Path

    from click import Group

__all__ = ("TailwindCLIPlugin",)


@dataclass(frozen=True)
class TailwindCLIPlugin(CLIPlugin):
    project_dir: str | Path = "."
    src_css: str | Path = "css/input.css"
    dist_src: str | Path = ""
    config_file: str | Path = "tailwind.config.js"
    tailwind_version: str = "latest"
    cli_bin: str | None = None

    def on_cli_init(self, cli: Group) -> None:
        from litestar_tailwind_cli.cli import tailwind_group

        cli.add_command(tailwind_group)
        return super().on_cli_init(cli)

    @property
    def tailwind_cli_bin(self) -> str:
        if self.cli_bin:
            return self.cli_bin
        extension = ".exe" if OS_TYPE == "windows" else ""
        return f"tailwind-cli{extension}"

    @property
    def tailwind_cli_is_installed(self) -> bool:
        try:
            subprocess.run([self.tailwind_cli_bin], capture_output=True, check=True)
        except FileNotFoundError:
            return False
        return True

    # @contextmanager
    # def server_lifespan(self, app: Litestar) -> Iterator[None]:
    #     yield
