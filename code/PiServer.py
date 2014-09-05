#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from SimpleXMLRPCServer import SimpleXMLRPCServer
    import os
    import sys
    if len(sys.argv) == 3:
        device_def_fn = sys.argv[1]
        port = sys.argv[2]
    elif len(sys.argv) == 2 and sys.argv[1] == "test":
        device_def_fn = 'examples/WidgetOverview/Microscope_dummy.py'
        port = 8000
    else:
        print "Usage:"
        print "    python PiServer.py [Device file path] [XML-RPC server port no.]"
        print "    python PiServer.py test"
        sys.exit(0)

    device_def_fn = os.path.abspath(device_def_fn)
    sys.path.append(os.path.dirname(device_def_fn))

    m = __import__(os.path.basename(device_def_fn).split('.')[0])
    Device = m.Device

    # Create server
    server = SimpleXMLRPCServer( ("0.0.0.0", int(port)) )
    server.register_introspection_functions()

    # Register an instance; all the methods of the instance are
    # published as XML-RPC methods
    server.register_instance( Device() )

    # Run the server's main loop
    server.serve_forever()
