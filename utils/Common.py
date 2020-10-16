import datetime
import pickle
import os
import pandas as pd
import numpy as np
import re

def pathExists(obj : str) -> bool:
    return os.path.exists(obj)

def isExistedFile(obj : str) -> bool:
    return pathExists(obj) and os.path.isfile(obj)

def isExistedDir(obj : str) -> bool:
    return pathExists(obj) and os.path.isdir(obj)

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
        # return obj is np.NaN
        # 上面那样写可能有bug
        return obj is np.NaN or np.isnan(obj)

# string processing
def isNumber(c : str):
    return ord(c) >= 48 and ord(c) <= 57

# '.'
def isDigitPoint(c : str):
    return ord(c) == 46

# '、'
def isChineseSlash(c : str):
    return ord(c) == 12289


def isNumericalChar(c : str):
    return isNumber(c) or isDigitPoint(c)

# 数字不能以小数点打头
def _extractFirstNumberLocation(src : str) -> tuple:
    h, t, f = -1, -1, False
    for i, c in enumerate(src):
        # 找到head
        if not f and h < 0 and isNumber(c):
            h = i
            f = True
        # 开始找尾巴
        if f and not isNumericalChar(c):
        # if h >= 0 and h < i and t < 0 and isNumericalChar(c):
            t = i
            break
    # 处理 sss777 末尾的问题
    if f and t < 0:
        t = i + 1
    if h >= 0 and t >= 0 and h < t:
        # return str[h : t + 1]
        return h, t
    else:
        return None, None

def extractAllNumbers(src : str):
    def _recursiveSearch(d : str, container : list):
        h, t = _extractFirstNumberLocation(d)
        if h is None or t is None:
            return
        container.append(d[h: t])
        _recursiveSearch(d[t:], container)

    # start
    re = []
    if src is None or len(src) <= 0:
        return re
    else:
        _recursiveSearch(src, re)
        return re



'''
输入：

-->
    1、非抵押担保企业，借款企业在本行月均有效结算量占其月均销售收入的比率≥本行在各金融同业对企业融资的占比；
    2、如本行为其唯一或主要授信银行，借款企业在本行月均有效结算量应不低于其月均销售收入的30%。

-->
    信用贷款，随借随还

输出：
    按序号拆分，保序地输出为字符串列表
    如果没有序号，输出本身
'''
# def _extractPart(src: str) -> tuple:
#     h, t, f = -1, -1, False
#
#     i = 0
#     while i < len(src):
#         # if not f and isNumber(src[i]) and i + 1 < len(src) and isChineseSlash(src[i + 1]):
#         if not f and isNumber(src[i]) and i + 1 < len(src) and (isChineseSlash(src[i + 1]) or isDigitPoint(src[i + 1])):
#             h = i
#             f = True
#             # 立刻移动i
#             i += 1
#         # if f and isNumber(src[i]) and i + 1 < len(src) and isChineseSlash(src[i + 1]):
#         if f and isNumber(src[i]) and i + 1 < len(src) and (isChineseSlash(src[i + 1]) or isDigitPoint(src[i + 1])):
#             # 不含
#             t = i
#             break
#         i += 1
#     # 从头开始，最后
#     if f and t < 0:
#         t = i + 1
#     # 从头开始，直到最后，其中一个数字标示都没有
#     if not f and h == -1 and t == -1:
#         return 0, len(src)
#     # 最后的验证
#     if h >= 0 and t >= 0 and h < t:
#         return h, t
#     else:
#         return None, None

def expose(src):
    return _extractPart(src)

def _extractPart(src: str) -> tuple:
    regx = r"([\s\S]*?)([0-9]+[、\.]{1})([^\d]{1})"
    pattern = re.compile(regx)
    matched = pattern.match(src)
    h, t = None, None
    if matched is not None:
        h = len(matched.group(1))
        bias = len(matched.group(1)) + len(matched.group(2))
        tailMatched = pattern.match(src[bias:])
        if tailMatched is not None:
            t = len(tailMatched.group(1)) + bias
        else:
            t = len(src)
    else:
        h, t = 0, len(src)
    return h, t


def extractMultipleLines(src: str):
    def _recursiveSearch(d: str, container: list):
        h, t = _extractPart(d)
        if h is None or t is None:
            return
        if h == 0 and t == len(d):
            if t > h:
                container.append(d)
            return
        container.append(d[h: t])
        _recursiveSearch(d[t:], container)

    # 清除空格什么的
    src = src.replace(" ", "")
    # 清除换行符
    src = src.replace("\n", "")

    re = []
    if src is None or len(src) <= 0:
        return re
    else:
        _recursiveSearch(src, re)
        return re