import json

import numpy as np
import pickle


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
