# Python Photobooth project
Just a small fun project for me for hustling with flask, python applications and more.
## :rocket:

# Contents
1. [Installation](#installation)
   1. [Install Raspi Dependencies](#install-raspi-dependencies)
   2. [Install Project](#install-project)
   3. [Configure Raspi](#configure-raspi)
2. [Run Service](#run-service)

# Installation
You need to do some configurations to successfully run the project
You will need the most actual raspi os installed. 
At the Moment it's bookworm or bullseye. I used bullseye for this.

## Install Raspi Dependencies
If not already done install libcamera in your raspi.
````commandline
# get latest updates
sudo apt update 
sudo apt upgrade

# install libcamera
sudo apt libcamera-apps
````

After this you will need the gstreamer plugin installed. 
-> libcamera is not directly supported by chromium. For running the webcam in the browser we need to stream the video from the actual device to a virtual device

https://forums.raspberrypi.com/viewtopic.php?t=351986


## Install Project
For installing the Project on your raspberry you will need to install all requirements
you can use a virtual environment for isolating the packages. But you will probably not use the Raspi  for other stuff. So you can directly install it.
````commandline
pip install -r requirements.txt
````

now you can manually run the service for tests.

## Configure Raspi

# Run Service
