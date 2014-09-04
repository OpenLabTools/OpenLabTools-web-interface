#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
class Microscope():
    def __init__(self, serial_port = "/dev/ttyACM0"):
        self.temp = 1
        self.set_temp = self.temp
        self.control_temp = True
        self.ser = serial.Serial(serial_port, 9600, timeout=3)
        #possibly change the above line to be relevant to the arduino serial port

    def __del__(self):
        self.ser.close();
        #destructing the class, closing down
        #the serial connection to avoid things getting bad

    def motion_control(self, direction="Down"):
        return direction

    def get_temp(self):
        self.ser.write( "1\n" )#tells the arduino to the read the temperature
        self.temp=self.ser.readline()
        if self.temp == '': self.temp = 1
        return float(self.temp)

    def set_set_temp(self, temp):
        self.ser.write("2\n")
        self.ser.write(str(temp))
        retval = self.ser.readline()
        return retval

    def get_set_temp(self):
        return self.set_temp

    def control_temp_toggle(self):
        self.control_temp = not self.control_temp
        return self.control_temp


if __name__ == "__main__":
    r = Microscope()
    import time
    time.sleep(1)
    print r.get_temp()
