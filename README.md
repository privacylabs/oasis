# Overview

Oasis automates the setup of a Raspberry Pi email server meant to run from
inside your home.  In the home environment, ISPs and user equipment can make it
difficult to externally reach home-based email servers due to port blocking.
Also, in most cases it's expensive to obtain a static IP address which is
necessary to successfully run a mail server.

To work around these issues Oasis provisions a cloud-based component that
acts as a gateway to your home-based Raspberry Pi server.  This cloud component
is stateless and all data received is immediately forwarded to your pi for
safe storage.


# Prerequisites

## Materials

1. Raspberry Pi 3 + microUSB Cable + Ethernet cable
1. MicroSD card, 32GB Class 10 minimum recommended, with SD card reader/adapter

## Windows Users

We recommend that you install putty so you have a good ssh client to access your Pi. Putty is available here: http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html (choose putty.exe, putty.zip or the MSI installer). Launch putty.exe to have an open terminal for all the commands specified below.

## Linux Users

We have tested Ubuntu 14.04 and 16.04. Please install avahi-daemon for discovering the Pi on the network - `$ sudo apt-get install avahi-daemon`

## Preparing the Pi

1. Download Raspbian Jessie Lite (https://www.raspberrypi.org/downloads/raspbian/)
1. Flash your microSD card with Raspbian Jessie Lite (https://www.raspberrypi.org/documentation/installation/installing-images/README.md)
1. Insert the microSD card into the microSD card socket on the bottom of the Pi
1. Connect your Pi to your router using an Ethernet Cable
1. Connect your Pi to your laptop using a microUSB cable or to a power plug
1. Log into your Pi - `$ ssh pi@raspberrypi.local` - the default password is 'raspberry'
1. Change your password to a secure password - `$ passwd`
  * We recommend using a password manager for generating and storing strong passwords
1. Configure wifi on your Pi (https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md)
1. Install prerequisites:
  * `$ sudo apt-get update`
  * `$ sudo apt-get upgrade (reboot if necessary)`
  * `$ sudo apt-get install python-pip python-crypto libffi-dev libssl-dev python-dev python-yaml git`
  * `$ sudo pip install markupsafe`
  * `$ sudo pip install cryptography --upgrade`
  * `$ sudo pip install boto`
  * `$ sudo pip install ansible --upgrade` (You may see an error about libyaml, but if you can run `$ ansible --version` successfully, you're all set)

## Preparing your cloud configuration

1. Create an account with AWS - sign up for 1 year of free tier services (https://aws.amazon.com/free/)
  * Verify your account: https://portal.aws.amazon.com/billing/signup?redirect_url=https://aws.amazon.com/registration-confirmation#/identityverification
  * Check your email for any additional verification steps and complete them as needed
  * If you want to use the free tier service, you will need to edit group_vars/all/vars.yml and set instance_size to 't2.micro'. After your free service is over, this instance size will cost ~$10/month. You can automatically switch to a smaller instance that costs ~$5/month by changing the value back to 't2.nano' and re-running the playbook.
  * If you already have an AWS account and have exhausted your free services, the services required to support Oasis are a t2.nano instance and a hosted zone. We estimate charges to be ~$5-6/month for a t2.nano with DNS services.
1. Register a domain that will be used for email (e.g.: cooldomain.net)
  * We suggest using Amazon Web Services (AWS) to skip manually configuring DNS. You will receive an email asking to verify your registration - click the link in the email.
  * If you are using a domain registered with another service it is likely not using AWS for DNS and you will need to configure your domain to use AWS DNS services  (http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/MigratingDNS.html)
1. In the AWS web console, go to Identity Access and Management (IAM) and create a user account and save the credentials for the account (AWS_ACCESS_KEY and AWS_SECRET_ACCESS_KEY). (http://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console) You will need to assign the following permissions to the user under Managed Policies (http://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-using.html#attach-managed-policy-console)
  * AmazonEC2FullAccess
  * AmazonRoute53FullAccess
1. Submit a request to Amazon to get reverse DNS support after you have completed the Quickstart section below. This will help ensure mail deliverability. Your elastic IP address will be available in group_vars/all/vars.yml after you have completed the Quickstart. The reverse DNS record is mail.cooldomain.net where you replace cooldomain.net with your custom domain. For the Use Case Description section the form, you can enter "personal email gateway". (https://aws-portal.amazon.com/gp/aws/html-forms-controller/contactus/ec2-email-limit-rdns-request)


# Quickstart

1. Log into your Pi - `$ ssh pi@raspberrypi.local`
1. Clone this repository - `$ git clone https://github.com/privacylabs/oasis --recursive`
1. `$ cd oasis`
1. Run the playbooks - `$ ansible-playbook -i inventory site.yml`
1. When prompted, carefully enter responses for the following values (There is a bug in Ansible 2.x which prevents responses from showing in the terminal as you type. Unfortunately, this way of taking input is very unforgiving, so any typos will require you to start over)
  * Domain - (e.g.: cooldomain.net)
  * First Name (e.g.: Louis)
  * Last Name (e.g.: Brandeis)
  * Username - (e.g. louis, creates the email address louis@cooldomain.net)
  * Password - We recommend using a password manager for generating and storing strong passwords
  * Confirm Password
  * AWS Access Key
  * AWS Secret Access Key
1. You will be prompted to confirm that the values you entered are correct. Press Enter to continue or Ctrl+C and then 'a' to abort. If you abort, delete the the vault.decrypted file in files/ `$ rm files/vault.decrypted`
1. You will be prompted to specify a vault password. The vault password is used to encrypt the information you provided in the prompts above, along with some randomly generated passwords.
  * We recommend using a password manager for generating and storing strong passwords
1. After the vault password prompt, you will soon be prompted to accept the SSH key for the gateway. Type 'yes' and press 'Enter'. If execution fails after this point, you will need to edit your .ssh/known_hosts file and remove this host before running the playbooks again.
1. Configure your mail (IMAP), calendar (CalDAV) and contacts (CardDAV) clients as follows from values you input when prompted during the install:
  * username: louis
  * password: strong_password_here
  * server name: mail.cooldomain.net
  * IMAP port: 993
  * SMTP port: 587
  * CalDAV and CardDAV port: 8443


# Development

For testing and development purposes a Vagrant configuration is supplied that allows you
to run the components that would normally execute in your Raspberry Pi, inside a virtual
machine.  The cloud based gateway component still executes in AWS of Digital Ocean.

To run in development mode:

1. Install the latest version of Vagrant on your development machine
1. Navigate to this source directory from the command line
1. $ vagrant up
1. $ vagrant ssh
1. $ cd oasis
1. $ ansible-playbook -i inventory site.yml
