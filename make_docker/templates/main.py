"""
Todo: Fix up the mapping to be inline with the update.sh.
"""
import re
import shutil
from glob import glob
from glob import iglob
from pathlib import Path
from string import Template
from typing import Generator, Iterable

from icecream import ic
from loguru import logger

from make_docker.conf import BUILD_PATH, DEFAULT_HTML
from make_docker.conf import NGINX_BUILD
from make_docker.conf import setting
from make_docker.templates.base import ENDING
from make_docker.templates.base import FROM_TEMPLATE
from make_docker.templates.base import LOCALE_FIX


def valid_input(*options: str):
    if options in setting.INVALID_OPTIONS:  # type: ignore
        return False
    return True


def generate_enumations(
    nginx: str, os: str, python: str
) -> Generator[tuple[str, str, str], None, None]:
    nginx_options = setting.NGINX_ALL if nginx == "all" else [nginx]  # type: ignore
    os_options = setting.OS_ALL if os == "all" else [os]  # type: ignore
    python_options = setting.PYTHON_ALL if python == "all" else [python]  # type: ignore
    for nginx in nginx_options:
        for os in os_options:
            for python in python_options:
                if valid_input(nginx, os, python):
                    yield nginx, os, python


def main(*, nginx: str, os: str, python: str, **options) -> int:
    try:
        # validate_input(nginx, os, python)
        generate_enumations(nginx, os, python)
        for nginx, os, python in generate_enumations(nginx, os, python):
            builder(nginx, os, python)
    except NotImplementedError as error:
        logger.exception(str(error), exception=error)
    return 0


def builder(nginx: str, os: str, python: str):
    path = "/".join((nginx, os, python))
    make_folders(nginx, os, python)
    if setting.OS_MAP[os] == "debian":  # type: ignore
        py_tag = f"{python}-{os}"  # type: ignore
    elif setting.OS_MAP[os] == "alpine":  # type: ignore
        py_tag = f"{python}-alpine{setting.ALPINE_VERSION_MAP[nginx]}"  # type: ignore
    else:
        raise NotImplementedError(
            f"This combination has not been impletmented: {(nginx, os, python)}"
        )

    make_dockerfile(nginx, os, python, py_tag)
    copy_entrypoints(nginx, os, path)
    copy_default_html(path)


def make_folders(nginx: str, os: str, python: str):
    folder_path: Path = ((BUILD_PATH / nginx) / os) / python
    folder_path.mkdir(exist_ok=True, parents=True)


def starts_with_list(
    line: str, matches: list[str] = setting.NGINX_BOTTOM_CUT_LINES  # type: ignore
) -> bool:
    for comparison in matches:
        if line.startswith(comparison):
            return True
    return False


def make_dockerfile(nginx: str, os: str, python: str, tag: str):
    dockerfile: str = ""
    dockerfile = Template(FROM_TEMPLATE).substitute(
        {"image": "python", "tag": tag, "name": "AS python-build"}
    )

    dockerfile_folder = f"{nginx}/{os}/{python}"
    nginx_build_path = NGINX_BUILD / f"{nginx}/{setting.OS_MAP[os]}{'-slim' if os == 'alpine' else ''}"  # type: ignore
    nginx_dockerfile_path = nginx_build_path / "Dockerfile"
    
    with open(nginx_dockerfile_path, "r") as f:
        nginx_dockerfile = f.readlines()
    cut_line_top = 0
    cut_line_bottom = []

    for idx, line in enumerate(nginx_dockerfile):
        if starts_with_list(line, ["LABEL maintainer=", "FROM"]):
            cut_line_top = idx
        elif starts_with_list(line):
            cut_line_bottom.append(idx)


    
    cut_line_bottom_idx = min(cut_line_bottom) if len(cut_line_bottom) else None

    dockerfile += "".join(nginx_dockerfile[cut_line_top + 1 : cut_line_bottom_idx])
    
    if os == 'alpine':
        nginx_build_path = NGINX_BUILD / f"{nginx}/{setting.OS_MAP[os]}" # type: ignore
        nginx_dockerfile_path = nginx_build_path / "Dockerfile"
        with open(nginx_dockerfile_path, "r") as f:
            nginx_dockerfile = f.readlines()   
            
        for idx, line in enumerate(nginx_dockerfile):
            if starts_with_list(line, ["LABEL maintainer=", "FROM"]):
                cut_line_top = idx
                
        dockerfile += "".join(nginx_dockerfile[cut_line_top + 1 : cut_line_bottom_idx])
    else:
        dockerfile += LOCALE_FIX
    dockerfile += ENDING

    with open((BUILD_PATH / dockerfile_folder) / "Dockerfile", "w") as f:
        f.write(dockerfile)

    logger.success(f"{dockerfile_folder} Dockerfile made.")


def copy_entrypoints(nginx: str, os: str, path: str | Path):
    from_dir = NGINX_BUILD / "entrypoint"  # type: ignore
    to_dir = BUILD_PATH / path
    entrypoints_re = re.compile(r"^((?!Dockerfile).*)$")
    ifiles = iglob("*", root_dir=str(from_dir))
    for file in [x for x in ifiles if entrypoints_re.match(x)]:
        shutil.copyfile(from_dir / file, to_dir / file)



def copy_default_html(path: str | Path):
    from_dir = DEFAULT_HTML
    to_dir = BUILD_PATH / path
    ifiles = iglob("*", root_dir=str(from_dir))
    for file in ifiles:
        shutil.copyfile(from_dir / file, to_dir / file)


if __name__ == "__main__":
    raise SystemExit(main(**{"nginx": "all", "os": "all", "python": "all"}))
