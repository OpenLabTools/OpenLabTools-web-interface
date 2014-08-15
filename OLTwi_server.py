#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, g
import calendar, time, random, xmlrpclib
from OLT_config_parser import get_config, get_config_by_id
from flask.ext.cache import Cache
from os import path

app = Flask(__name__)
cache = Cache(app,config={'CACHE_TYPE': 'memcached'})


def get_xmlrpc_server():
    if not hasattr(g, 'xmlrpc_server'):
        address = "http://localhost:8000/RPC2"
        g.xmlrpc_server = xmlrpclib.ServerProxy( address )
    return g.xmlrpc_server


def get_UI_config_obj():
    device_id = request.args['device_id']
    print device_id
    device_config = get_config_by_id( get_cluster_config_obj(), device_id )
    UI_config = get_config_by_fn( device_config['config_file'] )
    return UI_config


def get_cluster_config_obj():
    if not hasattr(g, 'cluster_config'):
        g.cluster_config = get_config(app.config['cluster_config_fn'])
    return g.cluster_config


@cache.memoize(1)
def get_config_by_fn(fn):
    return get_config(fn)


def xmlrpc_call( elem_args, extra_args=[] ):
    xmlrpc_server = get_xmlrpc_server()

    if 'args' in elem_args.keys():
        args = elem_args['args']
        if type( args ) is not list:
            args = [args]
    else: args = []

    if type( extra_args ) is not list:
        extra_args = [extra_args]

    args = tuple(args + extra_args)

    func = elem_args['func']

    @cache.memoize(1)
    def cachable( func, args ):
        """This function construct allow caching by matching func, args"""
        f = getattr(xmlrpc_server, func)
        retval = f( *args )
        return retval

    return cachable( func, args )


@app.route( '/button_click' )
def button_click():
    button_id = request.args.get("id")
    extra_args = request.args.get( "extra_args", [] )
    elem_args = get_config_by_id( get_UI_config_obj(), button_id )
    retval = xmlrpc_call( elem_args, extra_args )
    return jsonify( **{ 'state': retval } )


@app.route('/get_point')
def tsp_get_point():
    tsp_id = request.args.get("id")
    elem_args = get_config_by_id( get_UI_config_obj(), tsp_id )
    retval = xmlrpc_call( elem_args )
    return jsonify(
        time = calendar.timegm(time.localtime()),
        data = retval )


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
    if 'device_id' in request.args.keys():
        device_id = request.args['device_id']
        device_config = get_config_by_id( get_cluster_config_obj(), device_id )
        UI_config = get_config_by_fn( device_config['config_file'] )
        template_name = ['OpenLabTools_template.html']
        return render_template( template_name,
            UI_config = UI_config,
            cluster_config = get_cluster_config_obj(),
            device_id = device_id )
    else:
        return render_template( "device_picker.html",
            cluster_config = get_cluster_config_obj())


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2: cluster_config_fn = sys.argv[1]
    else: cluster_config_fn = './OLT_cluster_config.ini'
    app.config.update( dict( cluster_config_fn=cluster_config_fn ))
    app.debug = True
    app.run(host='0.0.0.0')