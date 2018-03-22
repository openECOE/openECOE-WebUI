# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/trusty64"

  config.vm.network "forwarded_port", guest: 5080, host: 5080

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
