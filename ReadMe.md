# Crawler Benchmark

[![Build Status](https://travis-ci.org/WebMole/crawler-benchmark.svg?branch=master)](https://travis-ci.org/WebMole/crawler-benchmark)
[![codecov](https://codecov.io/gh/WebMole/crawler-benchmark/branch/master/graph/badge.svg)](https://codecov.io/gh/WebMole/crawler-benchmark)
[![Docker Stars](https://img.shields.io/docker/stars/webmole/crawler-benchmark.svg)](https://hub.docker.com/r/webmole/crawler-benchmark/)
[![Docker Pulls](https://img.shields.io/docker/pulls/webmole/crawler-benchmark.svg)](https://hub.docker.com/r/webmole/crawler-benchmark/)
[![Docker layers](https://images.microbadger.com/badges/image/webmole/crawler-benchmark.svg)](https://microbadger.com/images/webmole/crawler-benchmark)

![Crawler-Benchmark](http://i.imgur.com/vHUkr9t.jpg)

A Reference Framework for the Automated Exploration of Web Applications. Provides some general web features to let you test crawlers in a well defined environment.

## Usage

First, clone the repository and `cd` into the repository.

### Using [Docker][docker]

1. Clone repository
2. Install [Docker][docker-install]
2. Install [docker-compose][docker-compose-install]
3. Build and use the docker image with [docker-compose][docker-compose]

    ```bash
    cd crawler-benchmark
    cp .env.example .env # then edit with desired credentials
    docker-compose up -d
    ```

When it's done, you can visit the app running at [localhost:8080](http://localhost:8080)

## Development

### Run tests locally

```bash
docker-compose run --rm website bash -c 'pytest --cov --cov-report term:skip-covered'
```

### css editing

We are using [grunt](http://gruntjs.com/) to auto compile [scss](http://sass-lang.com/) files into `css` files and we may add tasks in the future. [npm](https://www.npmjs.org/) dependencies are specified in `package.json`.

[Install sass from the command line](http://sass-lang.com/install) (you may need `sudo` privileges)

```bash
gem install sass
npm install
npm run grunt
```

## Todos

* build frontend using webpack and load `pure.scss` from `node_modules`
* Publish docker image so the world can spin this
* Add nodejs docker support
* Add link to home page (from title)
* Add new features!
  * Robots.txt validation
  * Visited urls
  * Provide an api 
* Website navigation generation from model
* Improve settings
  * Import
  * Export
  * json? yaml?
* Spread the word, make the application known by crawler authors
* Put online
  * Get crawled by general crawlers like google bot
  * Share results to the public

[docker]: https://docker.com/
[docker-install]: https://docs.docker.com/install/
[docker-compose]: https://docs.docker.com/compose/
[docker-compose-install]: https://docs.docker.com/compose/install/
