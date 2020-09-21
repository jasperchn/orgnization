import datetime
import pickle
import os
import pandas as pd
import numpy as np


def buildPath(*args):
    return '/'.join(args)

def read(path) -> pd.DataFrame:
    data = pd.read_csv(path)
    return data

def readableTimestamp(formatter="%Y-%m-%d_%H:%M:%S"):
    return datetime.datetime.now().strftime(formatter)

# path以linux方式命名
def saveByPickle(obj, path):
    dir, fileName = os.path.split(path)
    if (not os.path.exists(dir)):
        os.makedirs(dir)
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def loadByPickle(path):
    with open(path, "rb") as f:
        obj = pickle.load(f)
    return obj


def isEmpty(obj) -> bool:
    if obj is None:
        return False
    elif (isinstance(obj, str)):
        return obj == ""
    else:
        return obj is np.NaN


# def writeLine(src):
#     return src + "\n"
