import utils.Constant as C
from utils.Common import *
from bean.OrgTree import *
from table.PmsDb import *
from table.UsrDb import *


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



## common ↑

def makeLines(*args):
    return "\n".join(args)


# '''
# 输入：
#
# -->
#     1、非抵押担保企业，借款企业在本行月均有效结算量占其月均销售收入的比率≥本行在各金融同业对企业融资的占比；
#     2、如本行为其唯一或主要授信银行，借款企业在本行月均有效结算量应不低于其月均销售收入的30%。
#
# -->
#     信用贷款，随借随还
#
# 输出：
#     按序号拆分，保序地输出为字符串列表
#     如果没有序号，输出本身
# '''
# def _extractPart(src: str) -> tuple:
#     h, t, f = -1, -1, False
#
#     i = 0
#     while i < len(src):
#         if not f and isNumber(src[i]) and i + 1 < len(src) and isChineseSlash(src[i + 1]):
#             h = i
#             f = True
#             # 立刻移动i
#             i += 1
#         if f and isNumber(src[i]) and i + 1 < len(src) and isChineseSlash(src[i + 1]):
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
#
# def extractMultipleLines(src: str):
#     def _recursiveSearch(d: str, container: list):
#         h, t = _extractPart(d)
#         if h is None or t is None:
#             return
#         if h == 0 and t == len(d):
#             if t > h:
#                 container.append(d)
#             return
#         container.append(d[h: t])
#         _recursiveSearch(d[t:], container)
#
#     # 清除空格什么的
#     src = src.replace(" ", "")
#
#     re = []
#     if src is None or len(src) <= 0:
#         return re
#     else:
#         _recursiveSearch(src, re)
#         return re

if __name__ == '__main__':
    s1 = makeLines('1、符合《关于印发中小企业划型标准规定的通知》（工信部联企业〔2011〕300号）文件中划型标准的小型、微型企业，且纳入我行小微企业授信业务管理范畴；',
               '2、经工商行政管理部门核准登记并及时进行了年度申报；',
               '3、企业无不良信用记录； ',
               '4、我行需要认定的其他条件。'
                )
    s2 = "房产抵押，最高1000万；最长能贷20年；还款方式多样，最长5年不还本；可配套一笔最高100万的自助循环贷款"

    s3 = makeLines("A、业务条线权限业务：1、客户经理调查；2、条线有权审批人审批；3、放款；",
        "B、超业务条线权限业务：1、客户经理调查；2、风险审查员审查；3、风险条线有权审批人审批；4、放款")
    s4 = "d1、我的;2.他的;11.大家的10元;22."
    s5 = "1.好房快贷业务申请表；2.业务尽职调查及审批表；3.身份证明材料；4.婚姻状况声明书；5.房产证明材料；6.同意抵押申明；7.未出租声明；8.流水；9.借款人及其配偶个人征信报告；10.抵质押人有效身份证明材料、关系证明材料；11.抵质押物清单及权属证明材料；12.抵押物评估报告；13.借款人及配偶的执行查询。"

    # k = expose(s4)


    r1 = extractMultipleLines(s1)
    r2 = extractMultipleLines(s2)
    r3 = extractMultipleLines(s3)
    r4 = extractMultipleLines(s4)
    r5 = extractMultipleLines(s5)

    print(r1)
    print()
    print(r2)
    print()
    print(r3)
    print()
    print(r4)
    print()
    print(r5)



    pass
