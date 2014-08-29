
# OpenLabTools Web interface

## Introduction
The web interface is a set of software to enable simple controls of hardware using a browser. Having a web interface means that hardware can be monitored and controlled from anywhere using anydevice with a modern broswer.

The OpenLabTools Web interface features:

* __Control widgets__: buttons, sliders, toggles and more
* __Monitor widgets__: Time series plots, dynamic texts, video streams and more
* __Data explorer__ (in development)

The code is done entirely using python, html and javascript hence it is compatable with virtually any platform, be it Windows, mac or linux.


## The basics

### Software structure
<img src="images/software_structure.png" width=600px>

#### Microscope class
This is a user defined class to impliment methods to communicate with the hardware. Users will be able to call these functions in order to control and monitor the target hardware.

#### XMLRPC server
A simple XMLRPC server is implimented using python's xmlrpclib module. The server will expose methods from a user defined class named Microscope as functions. The application server can call these functions and get the returned data.

#### Application server
This server is implimented using python's flask library. It serves a dynamically generated webpage to clients web browser. And I will serve requests from the UI elements and translate them into xmlrpc calls.

