#!/usr/bin/env python
import os
import shutil
import subprocess
from pathlib import Path

import requests
from icecream import ic
from loguru import logger

from make_docker.conf import BUILD_PATH
from make_docker.conf import NGINX_BUILD
from make_docker.conf import setting


def remake_build_dir() -> None:
    """Remakes the build directory."""
    if BUILD_PATH.is_dir():
        logger.info(f"Removing the build directory.")
        shutil.rmtree(BUILD_PATH, ignore_errors=True)
    elif BUILD_PATH.is_file():
        logger.error(f"{BUILD_PATH} is a file and deleting it.")
        os.remove(BUILD_PATH)
    BUILD_PATH.mkdir()
    NGINX_BUILD.mkdir()
    logger.info(f"Making the build directory.")


def fetch_repot_structure() -> dict:
    file_structure = dict()
    url = f"{setting.API_GITHUB}/repos/{setting.NGINX_REPO}/git/trees/{setting.NGINX_BRANCH}?recursive=true"
    response: requests.Response = requests.get(url)
    for blob in response.json()["tree"]:
        file_structure[blob["path"]] = blob
    return file_structure


def fetch_raw_github(path: str, build_path=NGINX_BUILD):
    url = f"{setting.RAW_GITHUB}{setting.NGINX_REPO}/{setting.NGINX_BRANCH}/{path}"
    response: requests.Response = requests.get(url)
    with open(build_path / path, "w") as f:
        f.write(response.text)
    if endswith(path, ".sh"):
        os.chmod(build_path / path, 33277)
    if endswith(path, ".envsh"):
        os.chmod(build_path / path, 33277)


def fetch_nginx_executable() -> None:
    fetch_raw_github(setting.UPDATE_NGINX)
    os.chmod(NGINX_BUILD / setting.UPDATE_NGINX, 33277)


def endswith(string: str, test: str) -> bool:
    return string[-len(test) :] == test


def startswith(string: str, test: str) -> bool:
    return string[: len(test)] == test


def fetch_nginx_templates(repo_structure: dict) -> None:
    for path in repo_structure.keys():
        if endswith(path, ".template") and path[0] != ".":
            fetch_raw_github(path)


def fetch_entrypoints(repo_structure: dict):
    for path, blob in repo_structure.items():
        if startswith(path, "entrypoint") and blob["type"] == "blob":
            fetch_raw_github(path)


def create_tree(repo_structure: dict) -> None:
    for blob in repo_structure.values():
        if (
            blob["type"] == "tree"
            and blob["path"].split("/")[0] in setting.INCLUDE_PATH
        ):
            folder: Path = NGINX_BUILD / blob["path"]
            folder.mkdir(exist_ok=True)


def run_update():
    process = subprocess.run([NGINX_BUILD / setting.UPDATE_NGINX], capture_output=True)
    try:
        if process.returncode == 0:
            for line in process.stdout.splitlines():
                logger.debug(str(line).lstrip("b'").rstrip("'"))
        else:
            raise ChildProcessError
    except ChildProcessError as error:
        logger.exception("Failed to run nginx update.sh", exception=error)
        raise SystemExit(1)


def modify_templates(repo_structure: dict) -> None:
    for path in [
        x for x in repo_structure.keys() if endswith(x, ".template") and x[0] != "."
    ]:
        process = subprocess.run(
            [f"sed -i 's/ 101 / 102 /g' {NGINX_BUILD / path}"],
            shell=True,
            cwd=".",
            capture_output=True,
        )


def main(*args, **options) -> int:
    remake_build_dir()
    repo_structure = fetch_repot_structure()
    fetch_nginx_executable()
    fetch_nginx_templates(repo_structure)
    modify_templates(repo_structure)
    create_tree(repo_structure)
    fetch_entrypoints(repo_structure)
    run_update()
    logger.success("Nginx Dockerfiles Created")
    return 0


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("bye...")
        raise SystemExit(0)
