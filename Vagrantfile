# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
apt-get update -y
apt-get install python python-dev python-pip python-virtualenv -y
apt-get install libfreetype6-dev build-essential g++ libpng-dev libjpeg8-dev libfreetype6-dev python-matplotlib libffi-dev -y
pip install virtualenvwrapper
source /usr/local/bin/virtualenvwrapper.sh
echo 'source /usr/local/bin/virtualenvwrapper.sh' >> /home/vagrant/.bashrc

export WORKON_HOME=/home/vagrant/.virtualenvs
mkvirtualenv cb
easy_install -U distribute
cd /crawler-benchmark
pip install -r requirements.txt

chown -R vagrant: /home/vagrant

SCRIPT


VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
	config.vm.box = "precise64"
	config.vm.synced_folder "./", "/crawler-benchmark"
	config.vm.network "forwarded_port", guest: 8080, host: 8888

	config.vm.provision "shell", inline: $script
end