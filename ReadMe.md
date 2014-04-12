# Crawler Benchmark
CB is a crawler utility that implement a couple of site categories to be crawled. It also includes scenarios and configurations to handle ajax and some other goodies. Work in progress.

## Usage

First, clone the repository, `cd` into the directory and install dependencies using pip (provided with python)

    pip install -r requirements.txt

You may have troubles installing matplotlib so you can do this:

    pip install matplotlib --allow-external matplotlib

Then launch the server using `runserver.py`

    python runserver.py

Once the server is running, visit `/admin` and login with credentials.

Default login:

    username: admin
    password: default

## Changelog
See [changelog.md](./Changelog.md) file.