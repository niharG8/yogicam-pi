#!/usr/bin/python

import os, cgi, cgitb
from time import gmtime, strftime

DEBUG = 1
# set up constants
panConst = 5
tiltConst = 2
panID = 'P1-12' 
tiltID = 'P1-16' 

# Get querystring data
form = cgi.FieldStorage()
direction = form.getvalue('move')

# Open files
# ### DEBUG ###
if DEBUG:
    servoBlasterf = open('debug.log', 'a')
    servoBlasterf.write('{}    {}\n'.format(strftime('%a, %d %b %Y %H:%M:%S', gmtime()), direction))
# using os.system() instead
#servoBlasterf = open('/dev/servoblaster', 'w')
errLogf = open('err.log', 'a')

if direction == 'up':
    os.system('echo {}=+{}% > /dev/servoblaster\n'.format(tiltID, tiltConst))			
#    if DEBUG:
#        servoBlasterf.write('echo {}=+{}% > /dev/servoblaster\n'.format(tiltID, tiltConst))
elif direction == 'down':
    os.system('echo {}=-{}% > /dev/servoblaster\n'.format(tiltID, tiltConst))			
elif direction == 'left':
    os.system('echo {}=-{}% > /dev/servoblaster\n'.format(panID, panConst))
elif direction == 'right':
    os.system('echo {}=+{}% > /dev/servoblaster\n'.format(panID, panConst))
elif direction == 'home':
    os.system('echo {}=50% > /dev/servoblaster\n'.format(panID))
    os.system('echo {}=50% > /dev/servoblaster\n'.format(tiltID))
else:
    errLogf.write('{}  Unknown direction request received: {}\n'.format(strftime('%a, %d %b %Y %H:%M:%S', gmtime()), direction))

# Close files 
servoBlasterf.close()
errLogf.close()

print 'Content-type: text/html\n\n'
