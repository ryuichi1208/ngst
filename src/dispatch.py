#!/usr/local/bin/python3
# coding: utf-8

import collections
import datetime
import os
import sys
import functools

from flask import Flask, request, make_response, jsonify
from multiprocessing import Pool, Process, cpu_count
from module import github_trend
from module import qiita_trend

app = Flask(__name__)


def j_threads_create(n_cores: int) -> dict:
    return {
        "code" : "001",
        "cpu_count": n_cores,
        "pid" : os.getpid(),
        "ppid" : os.getppid(),
        "uid" : os.getuid(),
        "gid" : os.getgid(),
    }

@app.route("/__test")
def endpoint_for_testing():
    n_cores = cpu_count()
    p = Process(target=j_threads_create, args=(n_cores,))
    return jsonify(ResultSet=collections.OrderedDict(j_threads_create(n_cores)))


@app.route("/github/trend")
def trend_github():
    module.run()
    return ""


if __name__ == "__main__":
    FLASK_IPADDR = os.getenv("FLASK_IPADDR", "0.0.0.0")
    FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
    FLASK_DEBUG_MODE = bool(os.getenv("FLASK_DEBUG_MODE", True))

    app.run(FLASK_IPADDR, FLASK_PORT, debug=FLASK_DEBUG_MODE)
