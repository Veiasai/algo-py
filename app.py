from flask import Flask, request, abort
from flask_cors import *

from math import *
from scipy import optimize
import numpy as np
import json

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

if __name__ == "__main__":
    app.run(port='9998')