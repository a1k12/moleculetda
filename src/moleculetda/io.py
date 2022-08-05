import json
import pickle

import numpy as np


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def dump_json(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f, cls=NumpyEncoder)


def dump_pickle(obj, path):
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def read_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)
