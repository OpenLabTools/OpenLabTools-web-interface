#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import random
import urllib
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
import xmlrpclib
from picamera import PiCamera
from time import time as tic

class Microscope():
    def __init__(self, serial = '/dev/ttyARM0'):
        self.temp = 1
        self.set_temp = self.temp
        self.control_temp = True
        self.camera = PiCamera()
        self.camera.resolution = (320, 200)

    def get_image(self):
        #file = StringIO(urllib.urlopen(URL).read())
        #img = Image.open(file)
        start = tic()
        print "capturing_image"
        fd = StringIO()
        print tic()-start
        self.camera.capture(fd,'jpeg', use_video_port=True )
        print tic()-start
        # return xmlrpclib.Binary(urllib.urlopen(URL).read())
        retval = xmlrpclib.Binary(fd.getvalue())
        print tic()-start
        return retval


if __name__ == "__main__":
    r = Microscope()
