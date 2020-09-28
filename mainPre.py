from bean.OrgTree import *
import pandas as pd


def makeCoder(source : pd.DataFrame) -> dict:
    ret = {}
    for i in source.index:
        raw, code = source.loc[i, ["raw", "code"]]
        ret[raw] = code
    return ret


'''
codes是最早的数据改了表头得到的
首先用codes + patch + type 把新增加的字典和修补的机构信息恢复出来，得到codes-patched
然后再到makeOrg中用codes-patched生成sql
'''
if __name__ == '__main__':
    resourcePath = os.getcwd().replace("\\", "/") + "/resource"
    patchPath = buildPath(resourcePath, "src", "patch.csv")
    srcPath = buildPath(resourcePath, "src", "codes.csv")
    typePath = buildPath(resourcePath, "src", "types.csv")
    outPath = buildPath(resourcePath, "src", "codes-patched.csv")

    patch : pd.DataFrame = read(patchPath)
    src : pd.DataFrame = read(srcPath)
    coder = makeCoder(read(typePath))

    # 先轮循patch，修复level_1_code
    for i in patch.index:
        id, code = patch.loc[i, ["id", "level_1_code"]]
        # 首先获得src中对应的行号，注意检验数量
        linkIndex = src[src.id == id].index
        if len(linkIndex) != 1:
            raise RuntimeError("patch -> src is not 1 to 1, check id = {}".format(id))
        # 就地改值需要用loc
        print("try to change id = {}, code: {} -> {}".format(id, src.loc[linkIndex[0], "level_1_code"], code))
        src.loc[linkIndex[0], "level_1_code"] = code


    # 根据patch中的fi_org_type替换成新的编码
    # 用apply效率应该会好一点，不过不讲究了
    for i in src.index:
        raw = src.loc[i, "level_1_code"]
        # 注意处理KeyError
        try:
            src.loc[i, "level_1_code"] = coder[raw]
        except KeyError:
            raise RuntimeError("error occurs when transferring code with raw code = {}".format(raw))

    # 输出src
    src.to_csv(path_or_buf=outPath, index=False)
