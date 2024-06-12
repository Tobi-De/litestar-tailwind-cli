from pathlib import Path

from litestar import get
from litestar import Litestar
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.response import Template
from litestar.template.config import TemplateConfig
from litestar_tailwind_cli import TailwindCLIPlugin


@get("/")
async def index() -> Template:
    return Template(template_name="index.html.j2", context={})


@get("/favicon.ico", media_type="image/svg+xml")
async def favicon() -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        '<text y=".9em" font-size="90">🚀</text>'
        "</svg>"
    )


tailwind_cli = TailwindCLIPlugin(use_server_lifespan=True)

app = Litestar(
    route_handlers=[index, favicon],
    debug=True,
    plugins=[tailwind_cli],
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine,
    ),
)
