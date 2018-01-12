#!/usr/bin/env python

import pygame
import pygame.midi
from time import sleep
import threading
import signal
import sys
import random
import instrument
import os

alive = True
chan_data = {}
chan_list = [7,11,12,13,15,16,18]

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
    
def setup_gpio():
    global chan_data
    mode = GPIO.getmode()

    GPIO.setmode(GPIO.BOARD)

    for chan in chan_list:
        chan_data[chan] = 0

    GPIO.setup(chan_list, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
def get_settings(file):
    with open(file, "r") as midifile:
        settings = []
        for line in midifile:
            line = line.rstrip('\n')
            settings.append(line)
            
        read_instrument = int(settings[0])-1
        read_volume = int(settings[1])
        new_key = int(settings[2])
        
        settings = (read_instrument, read_volume, new_key)
        
        return settings
        
def settings_thread():
    global instrument
    file = "/var/www/html/midi.txt"
    modified = 0
    while alive == True:
        current = os.path.getmtime(file)
        if modified != current:
            print(modified)
            settings = get_settings(file)
            instrument.set_instrument(settings[0])
            instrument.set_volume(settings[1])
            instrument.set_key(settings[2])
            modified = current
        sleep(0.2)
    return

def setup_midi():
    TIMIDITYPORT = 2

    pygame.init()
    pygame.midi.init()

    port = pygame.midi.get_default_output_id()
    print ("default output_id :%s:" % port)
    print ("using output_id :%s:" % TIMIDITYPORT)
    return pygame.midi.Output(TIMIDITYPORT)


    
def poll_gpio():
    global instrument
    
    any_on = False
    
    for channel in chan_list:
        data = GPIO.input(channel)
        
        if data == 1:
            any_on = True
            
            if chan_data[channel] == 0:
                print("Pressed %d" % channel)
                chan_data[channel] = 1
                
                if channel == 7:
                    instrument.decrease_note_index(2)
                if channel == 11:
                    instrument.decrease_note_index(1)
                if channel == 12:
                    instrument.increase_note_index(1)
                if channel == 13:
                    instrument.increase_note_index(2)
            else:
                chan_data[channel] = 2
        else:
            if chan_data[channel]!=0:
                print("Released %d" % channel)
            chan_data[channel] = 0
            
    if any_on == False:
        instrument.turn_off()  

signal.signal(signal.SIGINT, signal_handler)    
setup_gpio()
midi_out = setup_midi()
instrument = instrument.Instrument(midi_out)    

t = threading.Thread(target=settings_thread)
t.start()

while alive==True:
    poll_gpio()
    sleep(.01)
    
pygame.midi.quit()

