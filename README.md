# Tutor Online

![GitHub repo size](https://img.shields.io/github/repo-size/FerdiantJoshua/belajar_online) ![GitHub issues](https://img.shields.io/github/issues/FerdiantJoshua/belajar_online) ![GitHub](https://img.shields.io/github/license/FerdiantJoshua/belajar_online) ![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/FerdiantJoshua/belajar_online?include_prereleases)

Online learning platform write in [Python](https://www.python.org/) using [Django](https://www.djangoproject.com/).

## Requirement

- [Python](https://www.python.org/) 3.6 or higher (best to use version 3.7)

## Installation

1. Clone the project

    using SSH:
    ```bash
    $ git clone git@github.com:FerdiantJoshua/belajar_online.git
    ```
    or using HTTPS:
    ```bash
    $ git clone https://github.com/FerdiantJoshua/belajar_online.git
    ```
2. Change to the directory
    ```bash
    cd belajar_online
    ```

2. Create project environtment using `virtualenv`
    ```bash
    $ python -m virtualenv venv
    $ venv/Scripts/activate.bat
    ```

4. Install dependency
    ```bash
    $ pip install -r requirements.txt
    ```

5. Create your .env file

    for example:
    ```.env
    ALLOWED_HOSTS = localhost,127.0.0.1,192.168.0.1
    DEBUG = False
    DB_NAME = belajar_online
    DB_USER = root
    DB_PASSWORD = password
    DB_HOST = 127.0.0.1
    DB_PORT = 3306
    DEV_MODE = False
    ```
6. Migrate the database
    ```bash
    $ python manage.py migrate
    ```

7. Run the server
    ```bash
    $ python manage.py runserver 0.0.0.0:8000
    ```

## Dependency

- You can read all the library needed in [requirements.txt](requirements.txt)

## Contribute
- Author: [@FerdiantJoshua](https://github.com/FerdiantJoshua)
- Contributor:
    - [@joshua060198](https://github.com/joshua060198)

## Change History
[CHANGELOG](CHANGELOG)

## License

[MIT](LICENSE)