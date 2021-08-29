
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, abort, jsonify, make_response
# import json
# import requests
# import ast
# import cv2
from os import path
# import numpy as np
# import base64
# import yolov5
from test import *
from time import sleep


app = Flask(__name__)


class flaskApp:
    def __init__(self):
        @app.route('/')
        def index():
            return render_template("index.html")


        @app.route('/wash_syringes')
        def wash_syringes():
            return render_template('washSyringe.html')


        @app.route('/dry_syringes')
        def dry_syringes():
            return render_template('drySyringe.html')


        @app.route('/sterilise_syringes')
        def sterilise_syringes():
            return render_template('steriliseSyringe.html')


        @app.route('/check_stains')
        def check_stains():
            # Run model to detect for stains and return value gotStains
            # gotStains 1 or 0
            gotStains = testFunction1()
            return jsonify(result=gotStains)


        @app.route('/check_wetness')
        def check_wetness():
            # Run model to detect for dry or wet and return value isWet
            # isWet 1 or 0
            isWet = testFunction2()
            return jsonify(result=isWet)


        @app.route('/wash_syringes_process')
        def wash_syringes_process():
            for x in range(10):
                print(x)
                sleep(1)
            return jsonify(result=True)


        @app.route('/dry_syringes_process')
        def dry_syringes_process():
            for x in range(10):
                print(x)
                sleep(1)
            return jsonify(result=True)


        @app.route('/sterilise_syringes_process')
        def sterilise_syringes_process():
            for x in range(10):
                print(x)
                sleep(1)
            return jsonify(result=True)

        app.run(host='0.0.0.0')

if __name__ == '__main__':
    flaskApp()
