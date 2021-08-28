
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, abort, jsonify, make_response
import json
import requests
import ast
import cv2
from os import path
import os
import numpy as np
import base64
import yolov5


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


# @app.route('/fullcycle', methods=['GET'])
# def fullcycle():


# @app.route('/halfcycle')
# def halfcycle(): 



if __name__ == '__main__':
       app.run()
