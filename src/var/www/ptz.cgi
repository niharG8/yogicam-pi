#!/usr/bin/python

import cgi
import sys
import traceback
import pigpio
import time

# set up constants
PAN_PCT = 20
TILT_PCT = 20
PAN_PIN_BCM = 18 
TILT_PIN_BCM = 23 
PINS = (PAN_PIN_BCM, TILT_PIN_BCM)
DIRECTIONS = ('up', 'down', 'left', 'right')

def init_gpio():
    return pigpio.pi()

def process_cgi():
    form = cgi.FieldStorage()  # Get querystring data
    direction = form.getvalue('move')
    debug = 'debug' in form and form.getvalue('debug') == '1' 
    return direction, debug

def pct2pulsewidth(pct):
    """ Convert % servo travel to pulse width for use with pigpio
    pct is 0% (full CCW) to 100% (full CW)"""
    if pct < 0 or pct > 100:
        raise ValueError('pct not in range [0,100]')
    scaled = pct / 100.0 * 2000.0
    shifted = scaled + 500.0
    pulsewidth = int(shifted)
    return pulsewidth

def pulsewidth2pct(pw):
    """ Convert pulse width from pigpio (500-2500) to % servo travel
    from 0% (full CCW) to 100% (full CW)""" 
    shifted = pw - 500.0
    scaled = shifted / 2000.0 * 100.0
    pct = scaled
    return pct

def rotate_servo_rel(pi, pin, pct):
    """ rotate the servo on a given BCM pin by the relative % travel
    given by pct (e.g. to rotate 10% of total travel in the ccw
    direction, pct = -10)"""
    try:
        pw_old = pi.get_servo_pulsewidth(pin)
    except:
        pw_old = 0  # no PWM has been set yet, so assume 0 
    pct_old = pulsewidth2pct(pw_old)
    if pct_old == -25:  # no PWM output commanded, go to center first to get a reference point
       pi.set_servo_pulsewidth(pin, pct2pulsewidth(50))
       pct_old = pulsewidth2pct(pi.get_servo_pulsewidth(pin))
    pct_cmd = pct_old + pct
    # saturate input to protect servo 
    if pct_cmd < 10:
        pct_cmd = 10
    elif pct_cmd > 90:
        pct_cmd = 90
    pi.set_servo_pulsewidth(pin, pct2pulsewidth(pct_cmd)) 


def get_servo_pct(pi, pin):
    """ get percent travel of a given BCM pin """
    return pulsewidth2pct(pi.get_servo_pulsewidth(pin))

def center_servos(pi, pins):
    for pin in pins:
        pi.set_servo_pulsewidth(pin, pct2pulsewidth(50))
        time.sleep(1)  # delay between commands
        pi.set_servo_pulsewidth(pin, 0)  # burn-out protection

def set_output_pins(gpio_pi, pins):
    """ configure each element of pins (BCM numbered) for output on 
    gpio_pi (instance of pigpio.pi)  """
    for pin in pins:
        gpio_pi.set_mode(pin, pigpio.OUTPUT)

def main():
    direction, debug = process_cgi()
    if debug:
        debugf = open('debug.log', 'a')
        debugf.write('{}    {}\n'.format(time.strftime('%a, %d %b %Y %H:%M:%S', time.gmtime()), direction))
    errLogf = open('err.log', 'a')

    try:
        #  Initialize pan/tilt GPIO pins for PWM output
        pi = init_gpio()
        set_output_pins(pi, PINS) 
        if direction == 'home':
            center_servos(pi, PINS)
        elif direction == 'up':
            rotate_servo_rel(pi, TILT_PIN_BCM, -1 * TILT_PCT)
        elif direction == 'down':
            rotate_servo_rel(pi, TILT_PIN_BCM, TILT_PCT)
        elif direction == 'left':
            rotate_servo_rel(pi, PAN_PIN_BCM, -1 * PAN_PCT)
        elif direction == 'right':
            rotate_servo_rel(pi, PAN_PIN_BCM, PAN_PCT)
        else:
            errLogf.write('{}  Unknown direction request received: {}\n'.format(time.strftime('%a, %d %b %Y %H:%M:%S', time.gmtime()), direction))

        if debug:
            try:
                debugf.write('Tilt: {}% \t Pan: {}%\n\n'.format(get_servo_pct(pi, TILT_PIN_BCM), get_servo_pct(pi, PAN_PIN_BCM)))
            except:
                pass
    finally:
        if debug:
            debugf.close()
        errLogf.close()


if __name__ == "__main__":
    print 'Content-type: text/html\n\n'
    print
    sys.stderr = sys.stdout
    try:
        main()
    except:
        print "\n\n<PRE>"
        traceback.print_exc()
