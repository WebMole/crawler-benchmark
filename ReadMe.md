# Crawler Benchmark
CB is a crawler utility that implement a couple of site categories to be crawled. It also includes scenarios and configurations to handle ajax and some other goodies. Work in progress.

## Usage

First, clone the repository, cd to the directory and install dependencies using pip (provided with python)

    pip install -r requirements.txt

Then launch the server using `cb.py` (cb for Crawler Benchmark)

    python cb.py

Or you can use `gunicorn` used in the requirements by running

    foreman start

Once the server is running, visit `/admin` and login with credentials.

Default login:

    username: admin
    password: default

## Changelog
See [changelog.md](./Changelog.md) file.