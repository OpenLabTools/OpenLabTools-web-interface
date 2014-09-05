#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, Response, abort
import calendar, time, xmlrpclib
from OLT_config_parser import get_config, get_config_by_id
from flask.ext.cache import Cache

app = Flask(__name__)
cache = Cache(app,config={'CACHE_TYPE': 'memcached'})


def get_xmlrpc_server():
    device_id = request.args['device_id']
    device_config = get_config_by_id( get_cluster_config_obj(), device_id )
    address = device_config['ip']
    return xmlrpclib.ServerProxy( 'http://' + address )


def get_UI_config_obj():
    device_id = request.args['device_id']
    device_config = get_config_by_id( get_cluster_config_obj(), device_id )
    UI_config = get_config_by_fn( device_config['config_file'] )
    return UI_config


def get_cluster_config_obj():
    return get_config_by_fn(app.config['cluster_config_fn'])


@cache.memoize(60, unless=(lambda: app.debug))
def get_config_by_fn(fn):
    return get_config(fn)


def xmlrpc_call( elem_args, extra_args, fast_update=False ):
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

    @cache.memoize(1, unless = (lambda: fast_update) )
    def cachable( func, args ):
        """This function construct allow caching by matching func, args"""
        f = getattr(xmlrpc_server, func)
        retval = None
        try:
            retval = f( *args )
        except:
            print "Unexpected error:", sys.exc_info()[0]
            abort(500)
        return retval

    return cachable( func, args )


@app.route( '/get_point'    )
@app.route( '/get_image'    )
@app.route( '/button_click' )
def button_click():
    button_id  = request.args.get("id")
    extra_args = request.args.get( "extra_args", [] )
    elem_args  = get_config_by_id( get_UI_config_obj(), button_id )

    if   request.path == '/button_click':
        retval = xmlrpc_call( elem_args, extra_args )
        return jsonify( state = retval )

    elif request.path == '/get_image':
        retval = xmlrpc_call( elem_args, extra_args, fast_update = True )
        cache_key = 'last_image' + button_id
        print cache_key
        cache.set(cache_key, retval)
        return Response( retval.data, mimetype='image/jpeg' )

    elif request.path == '/get_point':
        retval = xmlrpc_call( elem_args, extra_args )
        return jsonify(
            time = calendar.timegm(time.localtime()),
            data = retval )

    else: abort(404)

@app.route( '/save_image' )
def save_image():
    elem_id  = request.args.get("id")
    cache_key = 'last_image' + elem_id
    print cache_key
    img_data = cache.get('last_image' + elem_id).data
    return Response(img_data, mimetype='image/jpeg')


@app.template_filter('debug')
def debug(x):
    """print content to console from jinja2 templates."""
    print x
    return ""


@app.route('/')
@app.route('/html_gen')
def html_gen():
    if 'device_id' in request.args.keys():
        device_id = request.args['device_id']
        device_config = get_config_by_id( get_cluster_config_obj(), device_id )
        UI_config = get_config_by_fn( device_config['config_file'] )
        template_name = ['web_interface.html']
        return render_template( template_name,
            UI_config = UI_config,
            cluster_config = get_cluster_config_obj(),
            device_id = device_id,
            current_device_name = device_config['name'] )
    else:
        return render_template( "device_picker.html",
            cluster_config = get_cluster_config_obj())


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2: cluster_config_fn = sys.argv[1]
    else: cluster_config_fn = './examples/OLT_cluster_config.ini'
    app.config.update( dict( cluster_config_fn=cluster_config_fn ))
    app.debug = True
    app.run(host='0.0.0.0', port=80)
