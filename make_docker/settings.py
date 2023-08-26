PYTHON_VERSIONS = [
    "3.11",
    "3.10",
    "3.9",
    "all",
]
NGINX_VERSIONS = [
    "mainline",
    "stable",
    "all",
]
OS_CHOICES = ["debian", "bookworm", "bullseye", "alpine", "all"]

NGINX_REPO = "nginxinc/docker-nginx"
NGINX_BRANCH = "master"
NGINX_BOTTOM_CUT_LINES = ["ENTRYPOINT", "EXPOSE", "STOPSIGNAL", "CMD"]

UPDATE_NGINX = "update.sh"
INCLUDE_PATH = ["mainline", "stable", "entrypoint"]

API_GITHUB = "https://api.github.com"
RAW_GITHUB = "https://raw.githubusercontent.com/"
DEBIAN_VERSION_MAP = {"mainline": "bookworm", "stable": "bullseye"}
ALPINE_VERSION_MAP = {"mainline": "3.18", "stable": "3.18"}
OS_MAP: dict[str, str] = {
    "bookworm": "debian",
    "bullseye": "debian",
    "debian": "debian",
    "alpine": "alpine",
}
OS_ALL = [os for os in OS_CHOICES if os not in ['all', 'debian']]
NGINX_ALL = [nginx for nginx in NGINX_VERSIONS if nginx not in ['all']]
PYTHON_ALL = [python for python in PYTHON_VERSIONS if python not in ['all']]
ALL = {'os':"all", 'nginx':'all', 'python':'all'}
