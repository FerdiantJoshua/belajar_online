# Tutor Online

![GitHub repo size](https://img.shields.io/github/repo-size/FerdiantJoshua/belajar_online) ![GitHub issues](https://img.shields.io/github/issues/FerdiantJoshua/belajar_online) ![GitHub](https://img.shields.io/github/license/FerdiantJoshua/belajar_online) ![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/FerdiantJoshua/belajar_online?include_prereleases)

Online learning platform written in [Python](https://www.python.org/) using [Django](https://www.djangoproject.com/).

## Requirement

- [Python](https://www.python.org/) 3.6 or higher (tested in Python 3.7)

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

3. Create project environtment using `virtualenv`
    ```bash
    $ python -m virtualenv venv
    ```
    
4. Activate the virtual environment  
    Windows
    ```bash
    $ venv/Scripts/activate.bat
    ```    
    Linux or Mac
    ```bash
    $ source venv/bin/activate
    ```

5. Install dependency
    ```bash
    $ pip install -r requirements.txt
    ```

6. Create your .env file (check for [.env.example](.env.example))

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
7. Migrate the database
    ```bash
    $ python manage.py migrate
    ```

8. Run the server
    ```bash
    $ python manage.py runserver 0.0.0.0:8000
    ```

## Dependency

- All dependencies and requirements are mentioned in [requirements.txt](requirements.txt)

## Contribute
- Author: [@FerdiantJoshua](https://github.com/FerdiantJoshua)
- Contributor:
    - [@joshua060198](https://github.com/joshua060198)

## Change History
[CHANGELOG](CHANGELOG)

## License

[MIT](LICENSE)
