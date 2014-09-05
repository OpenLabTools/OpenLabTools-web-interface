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
import threading

class Device():
    def __init__(self, serial = '/dev/ttyARM0'):
        self.camera = PiCamera()
        self.camera.resolution = (320, 200)
        self.camera.framerate = 30
        self.double_buf = [StringIO(), StringIO()]
        self.buf_ptr = 0
        self.front_buf_lock = threading.Lock()

        def capture_thread():
            temp_buf = StringIO()
            for img in self.camera.capture_continuous(temp_buf, 'jpeg'):
                temp_buf.truncate()
                # write to back buffer
                self.double_buf[ 1-self.buf_ptr ] = temp_buf
                temp_buf.seek(0)
                with self.front_buf_lock:
                    # flip the front buffer to the back buffer
                    self.buf_ptr = 1 - self.buf_ptr

        thread = threading.Thread( target = capture_thread )
        thread.daemon = True
        thread.start()


    def get_image(self):
        start = tic()
        print "capturing_image"
        with self.front_buf_lock:
            retval = xmlrpclib.Binary(self.double_buf[self.buf_ptr].getvalue())
        print tic()-start
        return retval


if __name__ == "__main__":
    from time import sleep
    r = Device()
    sleep(1)
    print r.get_image()
