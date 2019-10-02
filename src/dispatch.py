#!/usr/local/bin/python3
# coding: utf-8

import datetime
import os
import sys
import functools

from flask import Flask,request,make_response,jsonify
from module import github_trend

app = Flask(__name__)

@app.route('/__test')
def endpoint_for_testing():
    return "Hello world"

@app.route("/github/trend")
def trend_github():
    module.run()
    return ""

if __name__ == "__main__":
    FLASK_IPADDR = os.getenv("FLASK_IPADDR", "0.0.0.0")
    FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
    FLASK_DEBUG_MODE = bool(os.getenv("FLASK_DEBUG_MODE", False))

    app.run(FLASK_IPADDR, FLASK_PORT, debug=FLASK_DEBUG_MODE)
