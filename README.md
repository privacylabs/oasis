# Overview

Oasis automates the setup of a raspberrypi email server meant to run from
inside your home.  In this environment ISPs and user equipment can make it
difficult to externally reach home based email servers due to port blocking.
Also, in most cases it's expensive to obtain a static IP address which is
necessary to successfully run a mail server.

To work around these issues oasis provisions a cloud based component that
acts as a gateway to your home based raspberrypi server.  This cloud component
is stateless and all data received is immediately forwarded to your pi for
safe storage of your data.



# Prerequisites

1. A registered domain
1. An account with AWS or Digital Ocean
1. For AWS your AWS_ACCESS_KEY and AWS_SECRET_ACCESS_KEY
1. For Digital Ocean your APIKEY
1. Raspberry Pi 3
1. Micro sdcard, recommend 32GB class 10



# Quickstart

1. [PC] Download the latest version of raspbian
1. [PC] Flash raspbian image to sdcard (https://www.raspberrypi.org/documentation/installation/installing-images/README.md)
1. [PI] Insert sdcard in to sdcard socket on raspberry pi
1. [PI] Power and connect pi to your local network
1. [PC] Install ansible
1. [PC] Clone this repository
1. [PC] `$ ssh pi@raspberrypi.local` - ssh to your pi, default password 'raspberry':
1. [PI] `$ passwd` - change the default password to your own
1. [PI] `$ raspi-config` - expand filesystem and reboot
1. [PC] `$ ansible-playbook -i inventory bootstrap_pi.yml -k` - when prompted enter the password you created previously
1. [PC] Modify ansible variables found in group_vars/all/vars.yml file to match your desired options and settings
1. [PC] Generate random passwords for services to copy into your vault (see below)
1. [PC] `ansible-playbook -i inventory bootstrap_pw.yml`
1. [PC] Create an ansible vault in group_vars/all named vault.yml to hold sensitive variables
1. [PC] `ansible-vault create group_vars/all/vault.yml`
1. [PC] Add vault_ variables referred to in group_vars/all/vars.yml to vault.yml
1. [PC] `$ ansible-playbook -i inventory site.yml --ask-vault-pass`



# Choosing a Cloud Provider

Oasis works with both AWS and Digital Ocean, however, AWS is more
fully supported.  The ansible scripts will automatically setup required DNS
settings with AWS.  DNS settings on Digital Ocean require more manual steps.



# Variables

```yaml
- vars:
  cloud: [aws|digitalocean] # use aws or digitalocean
  aws_region: [us-west-2, etc] # aws region where to deploy
  aws_access_key: # access key for your aws account, should go in your vault
  aws_secret_key: # secret key for your aws account, should go in your vault
  digital_ocean_api_token: YOUR_DIGITAL_OCEAN_API_TOKEN, should go in your vault
  domain: domain.com # your registered domain that will be used for email
  admin_email: # should be username @ your domain
  preserve_keys: # if defined will preserve generated diffie hellman key on your ansible host
  ldap_org_name: # whatever you want to call your organization
  ldapadminpassword: # root password for openldap, should be stored in your vault
  caldavduserpassword: # password for calendserver to work with ldap
  postfixuserpassword: # password for postfix to work with ldap
  terminate_gateway: # if defined will always terminate and restart the gateway instance when running playbook
  public_ip: # the first time you run the playbook a public ip will be auto generated and so this should be undefined
  letsencrypt_staging: # if defined will use the staging host for obtaining certificates
```

# Development

For testing and development purposes a Vagrant configuration is supplied that allows you
to run the components that would normally execute in your Raspberry Pi, inside a virtual
machine.  The cloud based gateway component still executes in AWS of Digital Ocean.

To run in development mode:

1. Install the latest version of Vagrant on your development machine
1. Navigate to this source directory from the command line
1. Modify configuration values in development/inventory
1. $ vagrant up

In Vagrant 1.8.1 there is a known bug which prevents ansible from being found in the
virtual machine instance.  This will result in an error shown until Vagrant 1.8.2 is
release.  To work around this problem, complete the installation by ssh'ing into the
virutal machine and manually executing ansible

1. $ vagrant ssh
1. $ cd /vagrant
1. $ ansible-playbook -i development/inventory site.yml
