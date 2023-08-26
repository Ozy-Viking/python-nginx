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
NGINX_BOTTOM_CUT_LINES = [
    "ENTRYPOINT",
    "EXPOSE",
    "STOPSIGNAL",
    "CMD"
]

UPDATE_NGINX = "update.sh"
INCLUDE_PATH = ["mainline", "stable", "entrypoint"]

API_GITHUB = "https://api.github.com"
RAW_GITHUB = "https://raw.githubusercontent.com/"
OS_VERSION_MAP = {
    'mainline': 'bookworm',
    'stable': 'bullseye'
}