#! /usr/bin/env python
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/toggle_led', methods=['GET'])
def toggle_led():
    requested_state = request.args.get("state")
    if requested_state == "On": state = "On"
    elif requested_state == "Off": state = "Off"
    return jsonify( **{ 'state': state } )

import calendar, time, random
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
    state = 0
    app.debug = True
    app.run(host='0.0.0.0')
