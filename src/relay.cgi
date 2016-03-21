#!/usr/bin/python

import cgi
import sys
import traceback
#import RPi.GPIO as GPIO
import pigpio

#RELAY_MODE = GPIO.BOARD
RELAY_PIN_BCM = 25  # P1-22, GPIO 25

def initGPIO():
   gpio = pigpio.pi()
   gpio.set_mode(RELAY_PIN_BCM, pigpio.OUTPUT)
   return gpio
    
def getcmd():
    form = cgi.FieldStorage()

    if 'cmd' in form:
        if form.getvalue('cmd') == 'on':
            cmd = True;
        elif form.getvalue('cmd') == 'off':
            cmd = False;
        else:
            cmd = None  # do nothing for invalid input
    else:  # no request, so toggle
       cmd = True;
    return cmd
    
def setRelay(gpio, cmd):
    if cmd is None:
        return
    elif cmd:
        gpio.write(RELAY_PIN_BCM, 0)  # close relay contacts 
    else:
        gpio.write(RELAY_PIN_BCM, 1)  # open relay contacts 

print "Content-Type: text/html"
print
sys.stderr = sys.stdout
with open('relay_log.txt', 'a') as f:
    try:
        cmd = getcmd()
        if cmd is None:
            sys.exit(1)
        gpio = initGPIO()
        setRelay(gpio, cmd)
        f.write('Completed\n')
    except:
        print "\n\n<PRE>"
        traceback.print_exc()
        f.write('Failed\n')
