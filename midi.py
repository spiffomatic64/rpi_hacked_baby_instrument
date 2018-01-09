#!/usr/bin/env python

'''
    File: midiExample

    Author: Jeff Kinne

    Contents:  basic example showing how to play midi sounds using pygame.

    Requires:  this example was run in Python 2.7 with pygame 1.9.2 installed.

    Sources:  I took the pygame.examples.midi file and extracted out only
    what is needed to play a few notes.
'''

import pygame
import pygame.midi
from time import sleep
import threading
import signal
import sys
import random

alive = True

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

    
def signal_handler(signal, frame):
    global alive
    
    print('You pressed Ctrl+C!')
    alive = False
    sleep(1)
    #sys.exit(0)
    
signal.signal(signal.SIGINT, signal_handler)
    
mode = GPIO.getmode()

GPIO.setmode(GPIO.BOARD)

chan_list = [7,11,12,13,15,16,18]
chan_data = {}
for chan in chan_list:
    chan_data[chan] = 1

GPIO.setup(chan_list, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 74 is middle C, 127 is "how loud" - max is 127
notes =[21,24,26,28,31,
        33,36,38,40,43,
        45,48,50,52,55,
        57,60,62,64,67,
        69,72,74,76,79,
        81,84,86,88,91,
        93,96,98,100,103,
        105,108,110,112,115]

TIMIDITYPORT = 2
TIMIDITYINSTRUMENT = 0

rand = False


GRAND_PIANO = 0
OD_GUITAR = 30
DS_GUITAR = 31
CHURCH_ORGAN = 19
SLAP_BASS = 37
TRUMPET = 57
TIMPANI = 48
BARRY_SAX = 68
PAN_FLUTE = 76

instrument = SLAP_BASS 
instrument = instrument - 1 

volume = 127

current_key = 0

pygame.init()
pygame.midi.init()

port = pygame.midi.get_default_output_id()
print ("default output_id :%s:" % port)
print ("using output_id :%s:" % TIMIDITYPORT)
midi_out = pygame.midi.Output(TIMIDITYPORT)

def worker():
    global midi_out
    global instrument
    global volume
    global current_key
    
    while alive == True:
        with open("/var/www/html/midi.txt", "r") as midifile:
            settings = []
            for line in midifile:
                line = line.rstrip('\n')
                settings.append(line)
                
            read_instrument = int(settings[0])-1
            if read_instrument>127:
                read_instrument = 127
            if read_instrument<0:
                read_instrument = 0
            if read_instrument!= instrument:
                print("Changing instrument from: %d to %d" %(instrument,read_instrument))
                
            read_volume = int(settings[1])
            if read_volume>127:
                read_volume = 127
            if read_volume<0:
                read_volume = 0
            if read_volume != volume:
                print("Changing volume from: %d to %d" %(volume,read_volume))
                volume = read_volume
            
            new_key = int(settings[2])
            if new_key>11:
                new_key = 11
            if new_key<0:
                new_key = 0
            if new_key != current_key:
                print("Changing Key from: %d to %d" %(current_key,new_key))
                current_key = new_key
                
            midi_out.set_instrument(read_instrument)
            instrument = read_instrument
        sleep(1)
    return    

midi_out.set_instrument(instrument)

t = threading.Thread(target=worker)
t.start()

last_note = 0
note = 21
held_on = False

key = ''
while alive==True:
    anyon = False
    for channel in chan_list:
        data = GPIO.input(channel)
        chan_data[channel] = data
        if data == 1:
            anyon = True
            print(channel,anyon,held_on,notes[note])
            if held_on == False:
                if channel == 7:
                    if rand:
                        note = note - random.randint(1,3)
                    else:
                        note = note - 2
                if channel == 11:
                    if rand:
                        note = note - random.randint(0,2)
                    else:
                        note = note -1
                if channel == 12:
                    if rand:
                        note = note + random.randint(0,2)
                    else:
                        note = note + 1
                if channel == 13:
                    if rand:
                        note = note + random.randint(1,3)
                    else:
                        note = note + 2
                if note>33:
                    note = 33
                if note<1:
                    note = 1
                
    if anyon == False:
        held_on = False
    else:
        held_on = True
    if anyon == True and last_note != note:
        # 127 is max volume
        midi_out.note_off(notes[last_note]+current_key,127)
        midi_out.note_on(notes[note]+current_key,127) 
        print("Note: %s" % note)
        last_note = note
    if anyon == False and last_note!=0:
        last_note = 0
        midi_out.note_off(notes[note]+current_key,127) 
        print("Stop note: %s" % note)
        
    sleep(.01)
    
del midi_out
pygame.midi.quit()

