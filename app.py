from flask import Flask, request, abort
from flask_cors import *

from math import *
from scipy import optimize
import numpy as np
import json
import base64
from arma import arma
from rungekutta import rungekutta
import io

def wrapper_solve_input(s):
    def ret(x):
        return eval(s)
    return ret

app = Flask(__name__)


CORS(app, supports_credentials=True)

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

@app.route('/usersolve', methods=['POST'])
def usersolve():
    try:
        paras = request.json
        x, info, status, message = optimize.fsolve(wrapper_solve_input(paras['function']), paras['solution'], full_output=True)
        return json.dumps({'x': x, 'info': info, 'status': status, 'msg': message}, cls=NumpyEncoder)
    except Exception as e:
        abort(403, description=str(e))

@app.route('/arma', methods=['POST'])
def arma_handler():
    try:
        paras = request.json
        ret = arma( {'length': paras['length'], 'data': io.BytesIO(base64.standard_b64decode(paras['data'])) })
        return json.dumps(ret)
    except Exception as e:
        abort(403, description=str(e))

@app.route('/rungekutta', methods=['POST'])
def runge_handler():
    try:
        paras = request.json
        ret = rungekutta(paras)
        return json.dumps(ret, cls=NumpyEncoder)
    except Exception as e:
        abort(403, description=str(e))

if __name__ == "__main__":
    app.run(port='9998')