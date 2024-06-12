# SPDX-FileCopyrightText: 2024-present Tobi DEGNON <tobidegnon@proton.me>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import subprocess
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Iterator
from typing import TYPE_CHECKING

from litestar.plugins import CLIPlugin
from litestar_tailwind_cli.utils import OS_TYPE
from rich import print as rprint

if TYPE_CHECKING:
    from litestar import Litestar
    from click import Group

__all__ = ("TailwindCLIPlugin",)


def _default_cli_path() -> Path:
    bin_path = Path(sys.prefix) / "bin"
    extension = ".exe" if OS_TYPE == "windows" else ""
    return bin_path / f"tailwind-cli{extension}"


@dataclass(frozen=True)
class TailwindCLIPlugin(CLIPlugin):
    src_css: str | Path = "css/input.css"
    dist_css: str | Path = "css/tailwind.css"
    use_server_lifespan: bool = False
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

    @contextmanager
    def server_lifespan(self, app: Litestar) -> Iterator[None]:
        import multiprocessing
        import platform
        from litestar_tailwind_cli.cli import run_tailwind_watch_process

        run_using_server_lifespan = self.use_server_lifespan and app.debug
        if not run_using_server_lifespan:
            yield

        if platform.system() == "Darwin":
            multiprocessing.set_start_method("fork", force=True)

        rprint("[yellow]Starting tailwind watch process[/]")
        process = multiprocessing.Process(
            target=run_tailwind_watch_process,
            args=(self.cli_path, self.src_css, self.dist_css),
        )

        try:
            process.start()
            yield
        finally:
            if process.is_alive():
                process.terminate()
                process.join()
            rprint("[yellow]Tailwind watch process stopped[/]")
