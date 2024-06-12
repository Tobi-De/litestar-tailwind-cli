# SPDX-FileCopyrightText: 2024-present Tobi DEGNON <tobidegnon@proton.me>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import TYPE_CHECKING

from litestar.plugins import CLIPlugin
from litestar_tailwind_cli.utils import OS_TYPE

if TYPE_CHECKING:
    from click import Group

__all__ = ("TailwindCLIPlugin",)


def _default_cli_path() -> Path:
    bin_path = Path(sys.prefix) / "bin"
    extension = ".exe" if OS_TYPE == "windows" else ""
    return bin_path / f"tailwind-cli{extension}"


@dataclass(frozen=True)
class TailwindCLIPlugin(CLIPlugin):
    src_css: str | Path = "css/input.css"
    dist_src: str | Path = ""
    config_file: str | Path = "tailwind.config.js"
    cli_version: str = "latest"
    cli_path: str | Path = field(default_factory=_default_cli_path, init=False)

    def on_cli_init(self, cli: Group) -> None:
        from litestar_tailwind_cli.cli import tailwind_group

        cli.add_command(tailwind_group)
        return super().on_cli_init(cli)

    @property
    def tailwind_cli_is_installed(self) -> bool:
        try:
            subprocess.run([self.cli_path], capture_output=True, check=True)
        except FileNotFoundError:
            return False
        return True

    # @contextmanager
    # def server_lifespan(self, app: Litestar) -> Iterator[None]:
    #     yield
