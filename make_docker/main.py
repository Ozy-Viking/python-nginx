#!/usr/bin/env python
import importlib
from pathlib import Path

import click
from icecream import ic
from loguru import logger

import make_docker.settings as setting

from .nginx import fetch_nginx_dockerfiles
from .templates import build_dockerfiles

# from make_docker.conf import setting


BASE_PATH: Path = Path(__file__).parent.parent
BUILD_PATH: Path = BASE_PATH / "build"


@click.command("make-docker")
@click.option(
    "-p",
    "--python",
    default=setting.PYTHON_VERSIONS[0],
    help=f"Python version/s. Default: {setting.PYTHON_VERSIONS[0]}",
    type=click.Choice(setting.PYTHON_VERSIONS),
)
@click.option(
    "-n",
    "--nginx",
    default=setting.NGINX_VERSIONS[0],
    help=f"Nginx version/s. Default: {setting.NGINX_VERSIONS[0]}",
    type=click.Choice(setting.NGINX_VERSIONS),
)
@click.option(
    "-o",
    "--os",
    default=setting.OS_CHOICES[0],
    help=f"Base OS for container. Default: {setting.OS_CHOICES[0]}",
    type=click.Choice(setting.OS_CHOICES),
)
@click.option('-a', '--all', help='All combinations',  is_flag=True)
def main(all: bool, *args, **options) -> int:
    if all:
        options = setting.ALL
    fetch_nginx_dockerfiles(**options)
    build_dockerfiles(**options)
    return 0



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("bye...")
        raise SystemExit(0)
