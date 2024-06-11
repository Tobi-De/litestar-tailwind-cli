# SPDX-FileCopyrightText: 2024-present Tobi DEGNON <tobidegnon@proton.me>
#
# SPDX-License-Identifier: MIT
from contextlib import contextmanager
from typing import Iterator

from litestar import Litestar
from litestar.plugins import CLIPlugin
from click import Group


class TailwindCLIPlugin(CLIPlugin):
    def on_cli_init(self, cli: Group) -> None:
        from litestar_tailwind_cli.cli import tailwind_group

        cli.add_command(tailwind_group)
        return super().on_cli_init(cli)

    @contextmanager
    def server_lifespan(self, app: Litestar) -> Iterator[None]:
        yield
