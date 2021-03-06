from utils.Common import *
import utils.Constant as C


'''
用ascii码处理，处理出连续的数字
递归吧
'''

# def isNumber(c : str):
#     return ord(c) >= 48 and ord(c) <= 57
#
# # '.'
# def isDigitPoint(c : str):
#     return ord(c) == 46
#
# # '、'
# def isChineseSlash(c : str):
#     return ord(c) == 12289
#
# def isNumericalChar(c : str):
#     return isNumber(c) or isDigitPoint(c)

# # 数字不能以小数点打头
# def _extractFirstNumberLocation(src : str) -> tuple:
#     h, t, f = -1, -1, False
#     for i, c in enumerate(src):
#         # 找到head
#         if not f and h < 0 and isNumber(c):
#             h = i
#             f = True
#         # 开始找尾巴
#         if f and not isNumericalChar(c):
#         # if h >= 0 and h < i and t < 0 and isNumericalChar(c):
#             t = i
#             break
#     # 处理 sss777 末尾的问题
#     if f and t < 0:
#         t = i + 1
#     if h >= 0 and t >= 0 and h < t:
#         # return str[h : t + 1]
#         return h, t
#     else:
#         return None, None
#
# def extractAllNumbers(src : str):
#     def _recursiveSearch(d : str, container : list):
#         h, t = _extractFirstNumberLocation(d)
#         if h is None or t is None:
#             return
#         container.append(d[h: t])
#         _recursiveSearch(d[t:], container)
#
#     # start
#     re = []
#     if src is None or len(src) <= 0:
#         return re
#     else:
#         _recursiveSearch(src, re)
#         return re

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


# todo -1
'''

def filterChar(v: str):
    r = ""
    for c in v:
        if isNumber(c) or isChineseSlash(c):
            r += c
    return r

def handleMultipleParams(s : str):
    try:
        # s = s.replace(" ", "")
        # s = s.replace("、", ",")
        # return s.split(",").__repr__().replace("\'", "\"").replace(" ", "")

        s = s.replace(" ", "")
        s = filterChar(s)
        s = s.replace("、", ",")
        s = list(map(lambda x: str(int(x)-1), s.split(",")))
        return s.__repr__().replace("\'", "\"").replace(" ", "")

    except Exception as he:
        # print(he)
        raise he

def selectFirstParam(s : str):
    try:
        # s = s.replace(" ", "")
        # return s.split("、")[0]

        s = s.replace(" ", "")
        s = filterChar(s)
        return str(int(s.split("、")[0]) - 1)

    except Exception as he:
        # print(he)
        raise he


# productType不能为空，默认若为空，填一个10（其他）
def handleProductType(s: str):
    # start
    # 空值填一发默认值
    if isEmpty(s):
        return "10"
        # 过滤掉数字和顿号意外的所有字符
    else:
        s = filterChar(s)
        # 过滤之后可能得到"10、"之类的输出，不过只选第一个，所以无所谓
        return selectFirstParam(s)

# accept_mode好像没有中文
def handleAcceptMode(s: str):
    return selectFirstParam(s)

def handleCustomerType(s: str):
    return selectFirstParam(s)

def handleMaxLoanTerm(s: str):
    return parseMinMax(s)[1]

# guarantee_mode可以为空
def handleGuaranteeMode(s: str):
    if isEmpty(s):
        return s
    else:
        return handleMultipleParams(s)

def handleProcessingDuration(s: str):
    n = parseMinMax(s)[1]
    # 向上取整
    import math
    return int(math.ceil(float(n)))

# 1 yes 2 no
def handleIsPolicyProduct(s):
    if s == 1 or s == '1':
        return True
    elif s == 2 or s == '2':
        return False
    else:
        raise RuntimeError("bad policy")

def handlerMaxCreditAmount(s):
    #转数字 * 10000
    return str(float(s) * 10000)

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
            sub.loc[i, C.P_is_policy_product] = handleIsPolicyProduct(sub.loc[i, C.P_is_policy_product])
            sub.loc[i, C.P_max_loan_terms] = handleMaxLoanTerm(sub.loc[i, C.P_max_loan_terms])
            sub.loc[i, C.P_accept_mode] = handleAcceptMode(sub.loc[i, C.P_accept_mode])
            sub.loc[i, C.P_guarantee_mode] = handleGuaranteeMode(sub.loc[i, C.P_guarantee_mode])
            sub.loc[i, C.P_pay_mode] = handleMultipleParams(sub.loc[i, C.P_pay_mode])
            # sub.loc[i, C.P_customer_type] = handleMultipleParams(sub.loc[i, C.P_customer_type])
            sub.loc[i, C.P_customer_type] = handleCustomerType(sub.loc[i, C.P_customer_type])
            sub.loc[i, C.P_usage_inf] = handleMultipleParams(sub.loc[i, C.P_usage_inf])
            sub.loc[i, C.P_processing_duration] = handleProcessingDuration(sub.loc[i, C.P_processing_duration])
            # product type 有空置还有中文，麻痹！
            sub.loc[i, C.P_product_type] = handleProductType(sub.loc[i, C.P_product_type])
            # sub.loc[i, C.P_product_type] = selectFirstParam(str(sub.loc[i, C.P_product_type]))

            sub.loc[i, C.P_min_credit_amount] = '0'
            # sub.loc[i, C.P_max_credit_amount] = sub.loc[i, C.P_credit_amount]
            sub.loc[i, C.P_max_credit_amount] = handlerMaxCreditAmount(sub.loc[i, C.P_credit_amount])
            # 重头戏，处理利率
            minInterest, maxInterest = parseMinMax(sub.loc[i, C.P_interest_rates])
            # 检查并且抛出
            sub.loc[i, C.P_min_interest_rates] = minInterest
            sub.loc[i, C.P_max_interest_rates] = maxInterest
        except Exception as e:
            print("shit happens during process data, i = {}, name = {}".format(i, sub.loc[i, C.P_product_name]))

    # 有没有必要删掉无用数据？
    sub.to_csv(path_or_buf=outPath, index=False)
    print("export to = {}".format(outPath))

    pass