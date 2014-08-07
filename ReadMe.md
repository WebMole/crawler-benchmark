# Crawler Benchmark

![Crawler-Benchmark](http://i.imgur.com/vHUkr9t.jpg)

A Reference Framework for the Automated Exploration of Web Applications. Provides some general web features to let you test crawlers in a well defined environement.

## Usage

First, clone the repository and `cd` into the repository.

### Using [Vagrant](http://www.vagrantup.com/)

First [install vagrant](https://docs.vagrantup.com/v2/installation/). Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) if you don't have it already.

Also make sure you have [precise64 box installed](https://docs.vagrantup.com/v2/providers/basic_usage.html)

Now simply run this in the current repository directory

    vagrant up

> Now sit and relaxe or go take a coffee, may take a while ;)

Note: Not fully tested yet, you now need to manually `vagrant ssh`, `cd /crawler-benchmark`, then `python runserver.py`. Will automate this in the future.

When it's done, you can visit the app running at [localhost:8888](http://localhost:8888)


### Using osx

#### [Install python](http://docs.python-guide.org/en/latest/starting/install/osx/)

#### I suggest you use [VirtualEnvWrapper](http://virtualenvwrapper.readthedocs.org/en/latest/)

    pip install virtualenvwrapper
    echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc
	source ~/.bashrc

#### Python dependencies

Install dependencies using pip (usually provided with python)

    pip install -r requirements.txt

You may have troubles installing matplotlib so you can do this:

    pip install matplotlib --allow-external matplotlib

Then launch the server using `runserver.py`

    python runserver.py


### Using Ubuntu or similar os

#### Update apt-get, install python and pip

	sudo apt-get update -y
	sudo apt-get install python python-dev python-pip -y

#### Install matplotlib dependencies and build tools requirements
	
	sudo apt-get install libfreetype6-dev build-essential g++ build-dep python-matplotlib -y

#### To install [MatPlotLib](http://matplotlib.org/) correctly, you also need to upgrade `distribute`

    sudo easy_install -U distribute

#### install virtualenvwrapper (optionnal)

	pip install virtualenvwrapper
	echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc
	source ~/.bashrc

##### Create a virtualenv with virtualenvwrapper (optionnal)

	mkvirtualenv cb

#### Install requirements

	sudo pip install -r requirements

When it's done, you can visit the app running at [localhost:8888](http://localhost:8888)


## CrawlerBenchmark Administration

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


##  Todos

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

## Changelog
See [changelog.md](./Changelog.md) file.