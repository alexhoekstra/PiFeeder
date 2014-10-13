##Description
Pifeeder is an Automated Feeder (human or animal) that will feed
the desired species twice a day, at specified times. Uses a 
RaspberryPi and its GPIO output
##Purpose
Developed to feed my cat, Yo-Sing on the long weekends that I am
away at the cottage during the summer
##Installation
Clone this repo into your RaspberryPI

	git clone https://github.com/alexhoekstra/PiFeeder.git

change directories into cloned location

	cd PiFeeder

Run the program 

	sudo python PiFeeder.py 
  
##Dependencies

RPIO

### Installation of RPIO ###

	$ sudo apt-get install python-setuptools
	$ sudo easy_install -U RPIO