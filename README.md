# rpi_hacked_baby_instrument
Python based midi instrument toy hacked into a baby toy using raspberrypi gpios

Video example: https://www.youtube.com/watch?v=knuSGUGNOsc

I'll make this better in the future, I swear


Requires a raspberrypi, python (pygame,, and timidity

Set volume in rc.local (or any other startup way you want) via amixer set 'PCM' 75%

To use crummy web interface use a llmp server:
sudo apt-get install lighttpd php-common php-cgi php


Hardware: 
  Fisher-Price Kick & Play Piano Gym
  raspberrypi
  wire
  
(Ill add pictures if people care)
# Hardware Instructions:
* Open piano
* unsolder/cut wires from buttons
* You have to cut the trace on the IC for the button thats on the IC board
* Use a female jumper from a 3.3v pin, solder 4 wires to that wire, and to each of the button pads (pick one side to stay consitent) 
* (I know the above line is confusing, you should end up with a female header on one end, and 4 male ends on the other, the male ends are soldered to the button's
* Use a female->male jumper, and solder the male side to the other side of each button
* Connect these jumpers to the following pins: 7, 11, 12 and 13 (you can use different pins, just update the code)

