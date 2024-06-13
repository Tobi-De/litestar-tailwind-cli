# litestar-tailwind-cli

[![PyPI - Version](https://img.shields.io/pypi/v/litestar-tailwind-cli.svg)](https://pypi.org/project/litestar-tailwind-cli)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/litestar-tailwind-cli.svg)](https://pypi.org/project/litestar-tailwind-cli)

-----

> [!IMPORTANT]
> This plugin currently contains minimal features and is a work-in-progress

Provides a CLI plugin for [Litestar](https://litestar.dev) to use [Tailwind CSS](https://tailwindcss.com) via the Tailwind CLI.

## Table of Contents

- [litestar-tailwind-cli](#litestar-tailwind-cli)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)

## Installation

```console
pip install litestar-tailwind-cli
```

## Usage

Configure and include the `TailwindCLIPlugin` in your Litestar app:

```python
from pathlib import Path

from litestar import Litestar
from litestar.static_files import create_static_files_router
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig
from litestar_tailwind_cli import TailwindCLIPlugin

ASSETS_DIR = Path("assets")

tailwind_cli = TailwindCLIPlugin(
  use_server_lifespan=True,
  src_css=ASSETS_DIR / "css" / "input.css",
  dist_css=ASSETS_DIR / "css" / "tailwind.css",
)

app = Litestar(
    route_handlers=[create_static_files_router(path="/static", directories=["assets"])],
    debug=True,
    plugins=[tailwind_cli],
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine,
    ),
)
```

```jinja
<head>
...
  <link rel="stylesheet" href="{{ url_for('static', path='css/tailwind.css') }}">
</head>
```

After setting up, you can use the following commands:

- `litestar tailwind init`: This command initializes the tailwind configuration and downloads the CLI if it's not already installed.
- `litestar tailwind watch`: This command starts the Tailwind CLI in watch mode during development. You won't have to use this if you set `use_server_lifespan` to `True`.
- `litestar tailwind build`: This command builds a minified production-ready CSS file.

> [!NOTE]
> Don't forget to update the `content` key in `tailwind.config.js` to specify your templates directories.

The `TailwindCLIPlugin` has the following configuration options:

- `src_css`: The path to the source CSS file. Defaults to "css/input.css".
- `dist_css`: The path to the distribution CSS file. Defaults to "css/tailwind.css".
- `config_file`: The path to the Tailwind configuration file. Defaults to "tailwind.config.js".
- `use_server_lifespan`: Whether to use server lifespan. Defaults to `False`. It will start the Tailwind CLI in watch mode when you use the `litestar run` command.
- `cli_version`: The version of the Tailwind CLI to download. Defaults to "latest".

## License

`litestar-tailwind-cli` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
