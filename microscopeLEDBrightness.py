#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
class LEDBrightness():
    def __init__(self):
        self.brightness = 0
        port = "/dev/ttyACM0"
        self.ser = serial.Serial(port, 9600, timeout=3)
        #possibly change the above line to be relevant to the arduino serial port

    def __del__(self):
        self.ser.close();
        #destructing the class, closing down
        #the serial connection to avoid things getting bad

    def motion_control(self, direction="Down"):
        return direction

    def get_brightness(self):
        self.ser.write( "1\n" )#tells the arduino to the read the temperature
        self.temp=self.ser.readline()
        if self.temp == '': self.temp = 1
        return float(self.temp)

    def set_brightness(self, brightness):
        self.ser.write(brightness + "\n")
        return