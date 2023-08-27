# Python Nginx Container

[![Build and Publish Containers](https://github.com/Ozy-Viking/python-nginx/actions/workflows/build_container.yaml/badge.svg?branch=main)](https://github.com/Ozy-Viking/python-nginx/actions/workflows/build_container.yaml) ![GitHub](https://img.shields.io/github/license/Ozy-Viking/python-nginx) ![Static Badge](https://img.shields.io/badge/python%20-%203.9%20%7C%203.10%20%7C%203.11-blue) ![Static Badge](https://img.shields.io/badge/OS-bookworm%20%7C%20bullseye-darkred) ![Static Badge](https://img.shields.io/badge/nginx-mainline%20%7C%20stable-brightgreen)

Pulls the docker files from nginx and then build it on a python image. Using up-to-date images for both python and nginx.

Docker Hub: [ozyviking/python-nginx](https://hub.docker.com/r/ozyviking/python-nginx)
GitHub Repo: [ozy-viking/python-nginix](https://github.com/Ozy-Viking/python-nginx)

## Container

Contianers can be pulled from either docker hub or github container registry:

- Docker: ozy-viking/python-nginx:latest
- Github: ghcr.io/ozy-viking/python-nginx:latest

### Tags

Tags are broken into 3 parts for their respective versions `<python>-<nginx>-<os>`.
For example the tag `3.11-mainline-bookworm` means that it is built bookworm (debian os), with a python version of 3.11 and the nginx branch of mainline

- 3.11-mainline-bookworm, mainline, bookworm, 3.11, latest
- 3.10-mainline-bookworm, 3.10
- 3.9-mainline-bookworm, 3.9
- 3.11-stable-bullseye
- 3.10-stable-bullseye
- 3.9-stable-bullseye

## Install

1. Install poetry.

    ```bash
    python -m pip install poetry
    ```

2. Install the package.

    ```bash
    git clone https://github.com/Ozy-Viking/python-nginx.git
    cd poetry-nginx
    poetry install
    ```

3. Activate the virtual environment.

    ```bash
    poetry shell
    ```

4. Use the script.

    ```bash
    makedocker --help
    ```

## Known bugs

Please raise an issue or a pull request if you want to solve this. Thank you in advance.

- [ ] No alpine support.
- [ ] No mainline bullseye or stable bookworm.
- [ ] No testing.
