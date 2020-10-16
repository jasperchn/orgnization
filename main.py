import os
# from utils.Common import *

import re

if __name__ == '__main__':
    # srcCodePathRoot = os.getcwd().replace("\\", "/")
    # # make organization first, (a pickle of organization tree(s) is needed later)
    # os.system("python {}".format(buildPath(srcCodePathRoot, "mainOrganization.py")))
    # # make users and other links later
    # os.system("python {}".format(buildPath(srcCodePathRoot, "mainUser.py")))

    line = "Cats are smarter than dogs";
    searchObj = re.search(r'(.*) are (.*?) .*', line, re.M | re.I)
    if searchObj:
        print("searchObj.group() : ", searchObj.group())
        print("searchObj.group(1) : ", searchObj.group(1))
        print("searchObj.group(2) : ", searchObj.group(2))
    else:
        print("Nothing found!!")



    s = "1、我的;2.他的;11.大家的10.0元"

    s = "d1、我的;2.他的;11.大家的10元;22."
    s = "d1、"
    # s = "1.我的;2.他的;11.大家的10元"
    # s = "2.他的;11.大家的10元"

    # pattern = re.compile(r"[0-9]+[\.、]{1}[^\d]{1}")
    # m = pattern.match(s)

    regx = r"([\s\S]*?)([0-9]+[、\.]{1})([^\d]{1})"
    pattern = re.compile(regx)
    m = pattern.match(s)

    pass