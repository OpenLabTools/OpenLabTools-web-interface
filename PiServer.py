#!/usr/bin/env python
# -*- coding: utf-8 -*-
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import serial


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


if __name__ == "__main__":

    import os
    import sys
    if len(sys.argv) == 4:
        microscope_def_fn = sys.argv[1]
        port = sys.argv[2]
        serial_port = sys.argv[3]
    else:
        microscope_def_fn = 'defaultUI/Microscope_dummy.py'
        port = 8000
        serial_port = '/dev/ttyARM0'

    microscope_def_fn = os.path.abspath(microscope_def_fn)
    sys.path.append(os.path.dirname(microscope_def_fn))

    m = __import__(os.path.basename(microscope_def_fn).split('.')[0])
    Microscope = m.Microscope

    # Create server
    server = SimpleXMLRPCServer(("localhost", port), requestHandler=RequestHandler)
    server.register_introspection_functions()

    # Register an instance; all the methods of the instance are
    # published as XML-RPC methods
    server.register_instance( Microscope(serial_port) )

    # Run the server's main loop
    server.serve_forever()
