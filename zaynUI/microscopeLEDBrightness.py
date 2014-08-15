#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
class Microscope():
    def __init__(self):
        self.brightness = 0
        port = "/dev/ttyACM1"
        self.ser = serial.Serial(port, 9600, timeout=3)
        #possibly change the above line to be relevant to the arduino serial port

    def __del__(self):
        self.ser.close();
        #destructing the class, closing down
        #the serial connection to avoid things getting bad
   
    def set_brightness(self, brightness):
        print "set_brightness"
        self.brightness = brightness
        self.ser.write("1 " + str(int(float(self.brightness))) + "\n")

    def get_brightness(self):
        self.ser.write( "2\n" )#tells the arduino to the get the current brightness level
        self.brightness=self.ser.readline()
        return int(self.brightness)

	def test_LED(self):
		print "Testing LED"
		self.ser.write("3\n")