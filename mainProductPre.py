from utils.Common import *
import utils.Constant as C


'''
用ascii码处理，处理出连续的数字
递归吧
'''

def isNumber(c : str):
    return ord(c) >= 48 and ord(c) <= 57

def isDigitPoint(c : str):
    return ord(c) == 46

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
分开左右两边，用'-'的
'''
def parseMinMax(src : str) -> tuple:
    def getOne(part : str) -> str:
        r = extractAllNumbers(part)
        if len(r) == 1:
            return r[0]
        else:
            raise RuntimeError("failed to get 'one' from source string = {}".format(part))

    delimiter = "-"
    # 应该要分出左右两个数
    if src.__contains__(delimiter):
        loc = src.index(delimiter)
        left = src[: loc]
        right = src[loc + 1:]

        l, r = None, None
        if not isEmpty(left):
            l = getOne(left)
        if not isEmpty(right):
            r = getOne(right)
        return l, r
    # 只应该解出来一个数，放在左边，但不一定表示是最小值
    else:
        single = getOne(src)
        return single, single




# 首先造中间输出，

'''
处理形如 1、2 => ["1", "2"]
'''
def handleMultipleParams(s : str):
    s = s.replace(" ", "")
    s = s.replace("、", ",")
    return s.split(",").__repr__().replace("\'", "\"").replace(" ", "")

def selectFirstParam(s : str):
    s = s.replace(" ", "")
    return s.split("、")[0]

def handleProductType(s : str):
    pass


if __name__ == '__main__':
    resourcePath = os.getcwd().replace("\\", "/") + "/resource"
    srcPath = buildPath(resourcePath, "src", "product-1-input.csv")
    outPath = buildPath(resourcePath, "out-intermediate", "product-2-clear.csv")
    # 选出可以执行的
    data = read(srcPath)
    sub = data[data[C.P_valid] == 1].copy()

    # 逐行遍历，试图处理数据，就地修改sub，最后输出
    # 首先造新列，避免奇怪的自动填充
    sub[C.P_min_credit_amount] = None
    sub[C.P_max_credit_amount] = None
    sub[C.P_min_interest_rates] = None
    sub[C.P_max_interest_rates] = None

    for i in sub.index:
        try:
            sub.loc[i, C.P_guarantee_mode] = handleMultipleParams(sub.loc[i, C.P_guarantee_mode])
            # sub.loc[i, C.P_guarantee_mode] = handleMultipleParams(str(sub.loc[i, C.P_guarantee_mode]))
            sub.loc[i, C.P_pay_mode] = handleMultipleParams(sub.loc[i, C.P_pay_mode])
            sub.loc[i, C.P_customer_type] = handleMultipleParams(sub.loc[i, C.P_customer_type])
            sub.loc[i, C.P_usage_inf] = handleMultipleParams(sub.loc[i, C.P_usage_inf])
            # product type 有空置还有中文，麻痹！
            sub.loc[i, C.P_product_type] = selectFirstParam(sub.loc[i, C.P_product_type])
            # sub.loc[i, C.P_product_type] = selectFirstParam(str(sub.loc[i, C.P_product_type]))

            sub.loc[i, C.P_min_credit_amount] = '0'
            sub.loc[i, C.P_max_credit_amount] = sub.loc[i, C.P_credit_amount]
            # 重头戏，处理利率
            minInterest, maxInterest = parseMinMax(sub.loc[i, C.P_interest_rates])
            # 检查并且抛出
            sub.loc[i, C.P_min_interest_rates] = minInterest
            sub.loc[i, C.P_max_interest_rates] = maxInterest
        except Exception as e:
            print(e)
            print("shit happens during process data, i = {}, name = {}".format(i, sub.loc[i, C.P_product_name]))
    sub.to_csv(path_or_buf=outPath, index=False)

    print("")

    # s1 = "这恩8.5512%hh0.223jjj77"
    # s2 = "8.5512sssdd2%hh0.2aa1"
    # s3 = "sssdd2558ggbb2210.2aa"
    #
    # r1 = extractAllNumbers(s1)
    # print(r1)
    # print(extractAllNumbers(s2))
    # print(extractAllNumbers(s3))


    pass    