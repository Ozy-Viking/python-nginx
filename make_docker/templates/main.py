from glob import glob, iglob
from pathlib import Path
import re
import shutil
from icecream import ic
from loguru import logger
from string import Template

from make_docker.conf import BUILD_PATH
from make_docker.conf import NGINX_BUILD
from make_docker.conf import setting
from make_docker.templates.base import ENDING, FROM_TEMPLATE, LOCALE_FIX

OS_MAP: dict[str, str] = {
    "bookworm": "debian",
    "bullseye": "debian",
    "debian": "debian",
    "alpine": "alpine",
    "all": "all",
}


def validate_input(nginx, os, python):
    if python == "all":
        raise NotImplementedError(
            "All is not implemented yet, please specify a python version."
        )
    if os == "all":
        raise NotImplementedError("All is not implemented yet, please specify an OS.")
    if nginx == "all":
        raise NotImplementedError(
            "All is not implemented yet, please specify a nginx version."
        )


def main(*, nginx, os, python, **options) -> int:
    if nginx == "all":
        raise ValueError("nginx != all")
    try:
        validate_input(nginx, os, python)
        match OS_MAP[os]:
            case "debian":
                make_folders(nginx, os)
                py_tag = f"{python}-{setting.OS_VERSION_MAP[nginx]}"
                make_dockerfile(nginx, os, tag=py_tag)
                copy_entrypoints(nginx, os)
            case _:
                raise NotImplementedError(f"OS: {os} is not avaible yet.")
    except NotImplementedError as error:
        logger.exception(str(error), exception=error)
    return 0


def make_folders(nginx, os):
    folder_path: Path = (BUILD_PATH / nginx) / os
    folder_path.mkdir(exist_ok=True, parents=True)


def starts_with_list(
    line: str, matches: list[str] = setting.NGINX_BOTTOM_CUT_LINES
) -> bool:
    for comparison in matches:
        if line.startswith(comparison):
            return True
    return False


def make_dockerfile(nginx, os, tag, *, python="python", **kwargs):
    dockerfile: str = ""
    dockerfile = Template(FROM_TEMPLATE).substitute(
        {"image": python, "tag": tag, "name": "AS python-build"}
    )

    dockerfile_folder = f"{nginx}/{os}"
    nginx_build_path = NGINX_BUILD / dockerfile_folder
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

    dockerfile += "".join(nginx_dockerfile[cut_line_top + 1 : min(cut_line_bottom)])
    dockerfile += LOCALE_FIX
    dockerfile += ENDING

    with open((BUILD_PATH / dockerfile_folder) / "Dockerfile", "w") as f:
        f.write(dockerfile)

    logger.success(f"{dockerfile_folder} Dockerfile made.")


def copy_entrypoints(nginx, os):
    from_dir = (NGINX_BUILD / nginx) / os
    to_dir = (BUILD_PATH / nginx) / os
    entrypoints_re = re.compile(r"^((?!Dockerfile).*)$")
    ifiles = iglob("*", root_dir=str(from_dir))
    for file in [x for x in ifiles if entrypoints_re.match(x)]:
        shutil.copyfile(from_dir / file, to_dir / file)


if __name__ == "__main__":
    raise SystemExit(main(**{"nginx": "mainline", "os": "debian", "python": "3.11"}))
