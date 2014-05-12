# Crawler Benchmark
CB is a crawler utility that implement a couple of site categories to be crawled. It also includes scenarios and configurations to handle ajax and some other goodies. Work in progress.

## Usage

### Python dependencies

First, clone the repository, `cd` into the directory and install dependencies using pip (usually provided with python)

    pip install -r requirements.txt

You may have troubles installing matplotlib so you can do this:

    pip install matplotlib --allow-external matplotlib

Then launch the server using `runserver.py`

    python runserver.py

Once the server is running, visit `/admin` and login with credentials.

Default login:

    username: admin
    password: default

## Development

### css editing

We are using [grunt](http://gruntjs.com/) to auto compile [scss](http://sass-lang.com/) files into `css` files and we may add tasks in the future. [npm](https://www.npmjs.org/) dependencies are specified in `package.json`.

[Install sass from the command line](http://sass-lang.com/install) (you may need `sudo` powers)

    gem install sass

Install grunt dependencies

    npm install

Install grunt globally

    npm install -g grunt grunt-cli

Run grunt and enjoy

    grunt

## Changelog
See [changelog.md](./Changelog.md) file.