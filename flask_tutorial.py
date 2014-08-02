#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, g
import calendar, time, random, xmlrpclib

app = Flask(__name__)

def get_xmlrpc_server():
    if not hasattr(g, 'xmlrpc_server'):
        address = "http://localhost:8000/"
        g.xmlrpc_server = xmlrpclib.ServerProxy( address )
    return g.xmlrpc_server


@app.route( '/button_click' )
def button_click():
    button_id = request.args.get("id")
    return jsonify( **{ 'state': random.random() } )


@app.route('/get_new_point', methods=['GET'])
def get_new_point():
    return jsonify(**{
        "time" : calendar.timegm(time.localtime()),
        "data" : (random.random() - 0.5) * 60
    })


from OLT_html_generator import unit_test
@app.route('/html_gen', methods=['GET'])
def html_gen():
    return unit_test()


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')