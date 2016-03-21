# yogicam-pi
## Webcam and home automation, running on Raspberry Pi

### What does this do?
yogicam-pi started out as a project to keep an eye on my puppy, Yogi, while I was at work. It began with a Raspberry Pi and a USB webcam I had laying around. As I quickly realized that dogs move around, I found the need to add pan and tilt capabilities.  The next evolution is controlling power to a standard 110 VAC lamp, in case it gets dark before I get home. This repo includes the scripts and config files I used to tie it all together. 

### Hardware Components
* Raspberry Pi
* UVC compatible USB webcam 
	* I used the [Logitech C270](http://www.amazon.com/Logitech-Widescreen-Webcam-Calling-Recording/dp/B004FHO5Y6)
* Pan/tilt bracket 
	* I used [this one](https://www.sparkfun.com/products/10335) from Sparkfun
* 2 RC "sub-micro" size servos
* Wifi adapter for the Raspberry Pi 
	* Optional, can use ethernet instead
* Logic-level compatible relay module
	* Switches 110 VAC
	* I used this [4-channel](http://www.amazon.com/gp/product/B00KTEN3TM?psc=1&redirect=true&ref_=oh_aui_detailpage_o01_s00) model from Amazon

### Software Components
* [pigpio](http://abyz.co.uk/rpi/pigpio/)
	* userspace digital and PWM control of GPIO pins
* [MJPG-streamer](https://sourceforge.net/projects/mjpg-streamer/)
	* stream webcam video over the internet
* apache 
	* a simple web server with CGI scripts to interact with GPIO pins
* [noip2](http://www.noip.com/) 
	* free dynamic DNS with a Linux updater client
* [tinyCam Monitor for Android](https://play.google.com/store/apps/details?id=com.alexvas.dvr.pro&hl=en)
	* Allows viewing and pan/tilt, using a custom config file


