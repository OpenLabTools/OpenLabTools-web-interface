#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import random
import urllib
import xmlrpclib

class Microscope():
    def __init__(self, serial = '/dev/ttyARM0'):
        del serial
        self.temp = 1
        self.set_temp = self.temp
        self.control_temp = True

    def motion_control(self, direction="Down"):
        return direction

    def get_temp(self):
        if self.control_temp:
            self.temp = self.temp + (self.set_temp - self.temp)*random()*1.2
        return self.temp

    def set_set_temp(self, temp):
        self.set_temp = float(temp)
        return self.set_temp

    def get_set_temp(self):
        return self.set_temp

    def control_temp_toggle(self):
        self.control_temp = not self.control_temp
        return self.control_temp

    def get_image(self):
        url = "http://lorempixel.com/400/400/"
        #file = StringIO(urllib.urlopen(URL).read())
        #img = Image.open(file)
        return xmlrpclib.Binary(urllib.urlopen(url).read())


if __name__ == "__main__":
    r = Microscope()
