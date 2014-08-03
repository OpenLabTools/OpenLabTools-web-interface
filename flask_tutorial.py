#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, g
import calendar, time, random, xmlrpclib
from OLT_config_parser import get_config, get_config_by_id

app = Flask(__name__)

def get_xmlrpc_server():
    if not hasattr(g, 'xmlrpc_server'):
        address = "http://localhost:8000/RPC2"
        g.xmlrpc_server = xmlrpclib.ServerProxy( address )
    return g.xmlrpc_server

def get_config_obj():
    if not hasattr(g, 'UI_config'):
        config_name = 'OLT_config_test.ini'
        g.UI_config = get_config(config_name)
    return g.UI_config


@app.route( '/button_click' )
def button_click():
    button_id = request.args.get("id")
    elem_args = get_config_by_id(get_config_obj(), button_id)
    xmlrpc_server = get_xmlrpc_server()
    print elem_args['func']
    f = getattr(xmlrpc_server, elem_args['func'])
    retval = f()
    return jsonify( **{ 'state': retval } )


@app.route('/get_new_point', methods=['GET'])
def get_new_point():
    return jsonify(**{
        "time" : calendar.timegm(time.localtime()),
        "data" : (random.random() - 0.5) * 60
    })


@app.template_filter('debug')
def debug(x):
    """print content to console from jinja2 templates."""
    print x
    return ""


@app.route('/html_gen', methods=['GET'])
def html_gen():
    template_name = 'OpenLabTools_template.html'
    return render_template( template_name, 
        UI_config = get_config_obj() )


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')