from bean.OrgTree import *
import utils.Constant as C


def find(src: str, all: list):
    c = []
    for h in all:
        if src in h:
            c.append(h)
    return c

    # for h in all:
    #     if src in h:
    #         return h



    # raise RuntimeError("cannot find {} in index".format(src))
    # print("cannot find {} in index".format(src))

if __name__ == '__main__':
    resourcePath = os.getcwd().replace("\\", "/") + "/resource"
    srcPath = buildPath(resourcePath, "src", "org-order.csv")


    data = read(srcPath)
    tree : TreeBuilder = loadByPickle(buildPath(resourcePath, "out-intermediate", "organizationTrees.plk"))


    search = {}
    names = []
    # first layer
    for k, v in tree.root.getChildren().items():
        orgName = v.getTable().org_name
        search[orgName] = k
        names.append(orgName)
        pass

    logger : Logger = Logger(buildPath(resourcePath, "out-intermediate", "orgs.csv"))

    #
    with logger:
        logger.writeLine("{},{},{}".format("id", "name", "cnt"))
        bias = 0
        gap = 1000
        cnt = 1
        already = []
        for i in data.index:
            name = data.loc[i, 'name']
            indexName = find(name, names)

            # if len(indexName) == 1:
            #     indexOrgNo = search[indexName[0]]
            #     data.loc[i, 'id'] = indexOrgNo
            #     # print("{} ===> {}, no = {}".format(name, indexName, indexOrgNo))
            if len(indexName) == 0:
                print("{} matched failed".format(name))
            elif len(indexName) >= 1:
                for x in indexName:
                    indexOrgNo = search[x]
                    already.append(indexOrgNo)
                    logger.writeLine("{},{},{}".format(indexOrgNo, x, gap * cnt + bias))
                    cnt += 1
        print("last overrider = {},{}".format(indexOrgNo, x))
        # 收尾
        for n in tree.trees:
            ogn = n.getTable().org_no
            if ogn not in already:
                logger.writeLine("{},{},{}".format(ogn, n.getTable().org_name, gap * cnt + bias))
                cnt += 1

    # data.to_csv(path_or_buf= buildPath(resourcePath, "out-intermediate", "orgs.csv"), index=False)
    pass
