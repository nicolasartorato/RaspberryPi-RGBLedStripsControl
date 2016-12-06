#!/usr/bin/python
# -*- coding: utf-8 -*-

# The Pins. Use Broadcom numbers.
RED_PIN   = 4
GREEN_PIN = 17
BLUE_PIN  = 18

RED_II_PIN = 27
GREEN_II_PIN = 22
BLUE_II_PIN = 23

RED_IS_PIN = 24
#GREEN_IS_PIN = 25
#BLUE_IS_PIN = 5

# Number of color changes per step (more is faster, less is slower).
# You also can use 0.X floats.
STEPS     = 1

###### END ######

import os
import sys
import termios
import tty
import pigpio
import time
from thread import start_new_thread
from random import randint


bright = 255
r = 254.0
g = 239.0
b = 239.0

rii = 0
gii = 0
bii = 0

ris = 0
#gis = 0
#bis = 0

brightChanged = False
abort = False
state = True
giorno = True
stelle = False
# dg durata giorno - dn durata notte
dg = 15.00
dn = 20.00

# time speed per transizione giorno. Valore piccolo = transizione più veloce
ts = 0.03

pi = pigpio.pi()

def updateColor(color, step):
        color += step

        if color > 255:
                return 255
        if color < 0:
                return 0

        return color


def setLights(pin, brightness):
        realBrightness = int(int(brightness) * (float(bright) / 255.0))
        pi.set_PWM_dutycycle(pin, realBrightness)


def getCh():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
        finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return ch


def checkKey():
        global bright
        global brightChanged
        global state
        global abort

        while True:
                c = getCh()

                if c == '+' and bright < 255 and not brightChanged:
                        brightChanged = True
                        time.sleep(0.01)
                        brightChanged = False

                        bright = bright + 1
                        print ("Current brightness: %d" % bright)

                if c == '-' and bright > 0 and not brightChanged:
                        brightChanged = True
                        time.sleep(0.01)
                        brightChanged = False

                        bright = bright - 1
                        print ("Current brightness: %d" % bright)

                if c == 'p' and state:
                        state = False
                        print ("Pausing...")

                        time.sleep(0.1)

                        setLights(RED_PIN, 0)
                        setLights(GREEN_PIN, 0)
                        setLights(BLUE_PIN, 0)

                if c == 'r' and not state:
                        state = True
                        print ("Resuming...")

                if c == 'c' and not abort:
                        abort = True
                        break
def luceInterni():
        global giorno
        global rii
        global gii
        global RED_II_PIN
        global GREEN_II_PIN

        while True:
                while not giorno:
                        rii = 255
                        gii = (randint(200,255))
                        setLights(RED_II_PIN, rii)
                        setLights(GREEN_II_PIN, gii)
                        time.sleep(0.05)
                        #print ("luci interni accese rosso a %d e verde a %d" % (rii,gii))
                rii = 0
                gii = 0
                setLights(RED_II_PIN, rii)
                setLights(GREEN_II_PIN, gii)
                time.sleep(1.00)



def luceStelle():
        global stelle
        global ris
#       global gis
#       global bis
        global RED_IS_PIN
#       global GREEN_IS_PIN
#       global BLUE_IS_PIN

        while True:
                if stelle:
#                        gis = updateColor(gis, STEPS)
                        ris = updateColor(ris, STEPS)
#                       bis =  updateColor(bis, STEPS)
#                       setLights(BLUE_IS_PIN, bis)
#                        setLights(GREEN_IS_PIN, gis)
                        setLights(RED_IS_PIN, ris)
                elif not stelle:
#                        gis = updateColor(gis, -STEPS)
                        ris = updateColor(ris, -STEPS)
#                        bis =  updateColor(bis, -STEPS)
#                        setLights(BLUE_IS_PIN, bis)
#                        setLights(GREEN_IS_PIN, gis)
                        setLights(RED_IS_PIN, ris)
                #print ("Stelle: %d " % ris )
                time.sleep(0.05)




start_new_thread(checkKey, ())
start_new_thread(luceInterni, ())
start_new_thread(luceStelle, ())


print ("+ / - = Increase / Decrease brightness")
print ("p / r = Pause / Resume")
print ("c = Abort Program")


setLights(RED_PIN, r)
setLights(GREEN_PIN, g)
setLights(BLUE_PIN, b)


while abort == False:
        if state and not brightChanged:
                if r == 254 and g == 239 and b < 240 and b > 80:
                        b = updateColor(b, -STEPS)
                        setLights(BLUE_PIN, b)
                        #print ("Red: %d Green: %d Blu: %d" % (r,g,b) )
                        time.sleep( ts )

                elif r == 254 and g < 240 and b == 80 and g > 120:
                        g = updateColor(g, -STEPS)
                        setLights(GREEN_PIN, g)
                        #print ("Red: %d Green: %d Blu: %d" % (r,g,b) )
                        time.sleep( ts)

                elif r < 255 and g < 121 and b == 80 and r > 0:
                        stelle = True
                        g = updateColor(g, -STEPS)
                        r = updateColor(r, -STEPS)
                        setLights(GREEN_PIN, g)
                        setLights(RED_PIN, r)
                        #print ("Red: %d Green: %d Blu: %d" % (r,g,b) )
                        time.sleep( ts )
                elif r == 0 and g == 0 and b == 80:
                        giorno = False
                        time.sleep( dn )
                        while r < 45:
                                r = updateColor(r, STEPS)
                                setLights(RED_PIN, r)
                                #print ("Red: %d Green: %d Blu: %d" % (r,g,b) )
                                time.sleep( ts )
                        giorno = True
                        while g < 240:
                                stelle = False
                                r = updateColor(r, STEPS)
                                g = updateColor(g, STEPS)
                                setLights(RED_PIN, r)
                                setLights(GREEN_PIN, g)
                                #print ("Red: %d Green: %d Blu: %d" % (r,g,b) )
                                time.sleep( ts )
                        while b < 240:
                                b = updateColor(b, STEPS)
                                setLights(BLUE_PIN, b)
                                #print ("Red: %d Green: %d Blu: %d" % (r,g,b) )
                                time.sleep( ts )
                        time.sleep( dg )
                        r = updateColor(r, -STEPS)
                        g = updateColor(g, -STEPS)
                        b = updateColor(b, -STEPS)
                        setLights(BLUE_PIN, b)
                        setLights(GREEN_PIN, g)
                        setLights(RED_PIN, r)
                        #print ("Red: %d Green: %d Blu: %d" % (r,g,b) )
                        time.sleep( ts )

print ("Aborting...")

setLights(RED_PIN, 0)
setLights(GREEN_PIN, 0)
setLights(BLUE_PIN, 0)

time.sleep(0.5)

pi.stop()
