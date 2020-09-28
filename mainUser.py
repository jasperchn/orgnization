import pandas as pd
from utils.Common import *

# def getValidIndex(s : pd.Series):
#     return s.ENABLED == 1 and (not isEmpty(s.USER_CODE)) and (not isEmpty(s.ORG_CODE))

if __name__ == '__main__':
    resourcePath = os.getcwd().replace("\\", "/") + "/resource"
    preHandledPath = buildPath(resourcePath, "out", "users.csv")

    # load users-full.csv, filter those users who are valid
    df = read(buildPath(resourcePath, "src", "users.full.csv"))
    available = df[df.apply(axis=1, func=lambda s: s.ENABLED == 1 and (not isEmpty(s.USER_CODE)) and (not isEmpty(s.ORG_CODE)))]
    print("{} user(s) are counted as available, export it to {}".format(len(available), preHandledPath))

    # todo make it short
    available.to_csv(path_or_buf=preHandledPath, index=False)


    pass