# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
apt-get update -y
apt-get install python python-dev python-pip -y
apt-get install libfreetype6-dev build-essential g++ build-dep python-matplotlib libffi-dev -y
pip install virtualenvwrapper
echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc
source ~/.bashrc

easy_install -U distribute

mkvirtualenv cb
cd /crawler-benchmark
pip install -r requirements

SCRIPT


VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
	config.vm.box = "precise64"
	config.vm.synced_folder "./", "/crawler-benchmark"
	config.vm.network "forwarded_port", guest: 8888, host: 8080

	config.vm.provision "shell", inline: $script
end