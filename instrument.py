#!/usr/bin/env python

class Instrument:

    # 74 is middle C, 127 is "how loud" - max is 127
    notes =[21,24,26,28,31,
        33,36,38,40,43,
        45,48,50,52,55,
        57,60,62,64,67,
        69,72,74,76,79,
        81,84,86,88,91,
        93,96,98,100,103,
        105,108,110,112,115]

    def __init__(self, midi_out, instrument = 0, volume = 127, key = 0):
        self.instrument = 0
        self.volume = 127
        self.key = 0
    
        self.midi_out = midi_out
        self.set_instrument(instrument)
        self.set_volume(volume)
        self.set_key(key)
        self.note_index = 21
        
    def set_instrument(self,instrument):
        if instrument > 127:
            instrument = 127
            
        if instrument < 0:
            instrument = 0
            
        if self.instrument != instrument:    
            print("Changing instrument from: %d to %d" %(self.instrument,instrument))
            self.instrument = instrument
            self.midi_out.set_instrument(self.instrument)
        
    def set_volume(self,volume):
        if volume > 127:
            volume = 127
            
        if volume < 0:
            volume = 0
            
        if self.volume != volume:
            print("Changing volume from: %d to %d" %(self.volume,volume))
            self.volume = volume
        
    def set_key(self,key):
        if key > 11:
            key = 11
            
        if key < 0:
            key = 0
            
        if self.key != key:
            print("Changing key from: %d to %d" %(self.key,key))
            self.key = key
        
    def get_note(self):
        return self.notes[self.note_index] + self.key
        
    def change_note_index(self,amount):
        self.midi_out.note_off(self.get_note(), self.volume)
        self.note_index += amount
        
        if self.note_index > 33:
            self.note_index = 33
        if self.note_index < 1:
            self.note_index = 1
            
        self.midi_out.note_on(self.get_note(), self.volume)
        
    def increase_note_index(self, amount = 1):
        self.change_note_index(amount)
            
    def decrease_note_index(self, amount = 1):
        amount = 0 - amount
        self.change_note_index(amount)
        
    def turn_off(self):
        self.midi_out.note_off(self.get_note(), self.volume)
        
