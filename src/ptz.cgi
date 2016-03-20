#!/usr/bin/python

from os import system
import cgi
from time import gmtime, strftime

# set up constants
PAN_CONST = 5
TILT_CONST = 2
PAN_ID = 'P1-12' 
TILT_ID = 'P1-16' 
VALID_DIRECTIONS = ('up', 'down', 'left', 'right', 'home')

def process_cgi():
    form = cgi.FieldStorage()  # Get querystring data
    direction = form.getvalue('move')
    debug = 'debug' in form and form.getvalue('debug') == '1' 
    return direction, debug


def main():
    direction, debug = process_cgi()
    if debug:
        servoBlasterf = open('debug.log', 'a')
        servoBlasterf.write('{}    {}\n'.format(strftime('%a, %d %b %Y %H:%M:%S', gmtime()), direction))
    errLogf = open('err.log', 'a')

    try:
        if direction == 'home':
            servocmd = 'echo {}=50% > /dev/servoblaster \necho {}=50% > /dev/servoblaster\n'.format(PAN_ID, TILT_ID)
        elif direction == 'up':
            #servocmd = 'echo {}=+{}% > /dev/servoblaster\n'.format(TILT_ID, TILT_CONST)
            id = TILT_ID
            const = TILT_CONST
            signstr = '+'
        elif direction == 'down':
            #servocmd = 'echo {}=-{}% > /dev/servoblaster\n'.format(TILT_ID, TILT_CONST)    
            id = TILT_ID
            const = TILT_CONST
            signstr = '-'
        elif direction == 'left':
            #servocmd = ('echo {}=-{}% > /dev/servoblaster\n'.format(PAN_ID, PAN_CONST)
            id = PAN_ID
            const = PAN_CONST
            signstr = '-'
        elif direction == 'right':
            #os.system('echo {}=+{}% > /dev/servoblaster\n'.format(PAN_ID, PAN_CONST)
            id = PAN_ID
            const = PAN_CONST
            signstr = '+'
        else:
            errLogf.write('{}  Unknown direction request received: {}\n'.format(strftime('%a, %d %b %Y %H:%M:%S', gmtime()), direction))

        if direction in VALID_DIRECTIONS:
            servocmd = 'echo {}={}{}% > /dev/servoblaster\n'.format(id, signstr, const)
            if debug:
                servoBlasterf.write(servocmd)
            os.system(servocmd)  # write to servoblaster
    finally:
        if debug:
            servoBlasterf.close()
        errLogf.close()

    print 'Content-type: text/html\n\n'


if __name__ == "__main__":
    main()