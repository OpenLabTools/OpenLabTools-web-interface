#!/usr/bin/env python
# -*- coding: utf-8 -*-
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import serial


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


if __name__ == "__main__":
    try:
        serial.Serial('/dev/ttyACM0').close()
        from microscope1 import Microscope
    except:
        from Microscope_dummy import Microscope

 #   from zaynUI.microscopeLEDBrightness import Microscope

    # Create server
    server = SimpleXMLRPCServer(("localhost", 8000), requestHandler=RequestHandler)
    server.register_introspection_functions()

    # Register an instance; all the methods of the instance are
    # published as XML-RPC methods
    server.register_instance( Microscope() )

    # Run the server's main loop
    server.serve_forever()
