from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from click import Context, group, option
from click import Path as ClickPath
from litestar.cli._utils import (
    LitestarEnv,
    LitestarGroup,
)

if TYPE_CHECKING:
    from litestar import Litestar


@group(cls=LitestarGroup, name="tailwind")
def tailwind_group():
    """Manage tailwind tasks."""


@tailwind_group.command(name="init", help="")
def tailwind_init(app: Litestar):
    pass


@tailwind_group.command(name="watch", help="")
def tailwind_watch():
    pass


@tailwind_group.command(name="build", help="")
def tailwind_build():
    pass
