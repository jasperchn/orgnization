import os
from utils.Common import *

if __name__ == '__main__':
    srcCodePathRoot = os.getcwd().replace("\\", "/")
    # make organization first, (a pickle of organization tree(s) is needed later)
    os.system("python {}".format(buildPath(srcCodePathRoot, "mainOrganization.py")))
    # make users and other links later
    os.system("python {}".format(buildPath(srcCodePathRoot, "mainUser.py")))

    pass