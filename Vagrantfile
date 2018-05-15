# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.network "private_network", ip: "192.168.11.21"
  config.vm.box = "ubuntu/trusty64"
  config.vm.network "public_network"
  config.vm.network "private_network", ip: "192.168.11.21:5080"

  config.vm.provision "ansible_local" do |ansible|
    #ansible.verbose = "v"
    ansible.galaxy_role_file= "vagrant_requeriments.yml"
    ansible.playbook = "vagrant_setup.yml"
  end

  config.vm.provider "virtualbox" do |v|
  #  v.name = "openECOE-WebUI"
    v.memory = 2048
    v.cpus = 2
  end
end
