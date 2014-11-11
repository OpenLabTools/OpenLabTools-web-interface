#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial, sys, threading

class Device():
    def __init__(self, serial_port = "COM5"):
        self.ser = serial.Serial(serial_port, 9600, timeout=3)
        self.lock = threading.Lock()
        self.ser_lock = threading.Lock()
        self.temperature = -1;
        self.humidity = -1;
        self.orientation = -1;
        def update_thread():
            while(self.ser.isOpen()):
                with self.ser_lock:
                    self.ser.flushInput()
                    self.ser.readline()
                    new_line = self.ser.readline()
                with self.lock:
                    self.orientation = ord(new_line[0])
                    self.temperature = ord(new_line[1])
                    self.humidity = ord(new_line[2])
        thread = threading.Thread( target = update_thread )
        thread.daemon = True
        thread.start()

    def __del__(self):
        self.ser.close();

    def set_angle(self, angle):
        cmd = "1 %i\n"%( int(float(angle)) );
        print "writing command: " + cmd
        sys.stdout.flush()
        with self.ser_lock:
            self.ser.write( cmd )
            self.ser.flushOutput()
        return angle

    def get_temperature(self):
        with self.lock:
            return self.temperature

    def get_humidity(self):
        with self.lock:
            return self.humidity

    def get_orientation(self):
        with self.lock:
            return self.orientation

if __name__ == "__main__":
    r = Device()
    print r.get_temperature()
    print r.get_humidity()
    print r.set_angle(20)
