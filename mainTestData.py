from mainUser import *

_userBias = 23
_userCount = 6



# 利用Node的recentAdd来标记路径，本来这个rencentAdd存的是个node，充分利用python动态特性
def setRecentAdd(trees : TreeBuilder , v : bool = False):
    for i, (_, node) in enumerate(trees.pool.items()):
        node.recentAdded = v

def markMinimunRoute(trees : TreeBuilder, orgs : list):
    for org in orgs:
        leaf : Node = trees.pool[org]
        # 对叶子节点向上寻根
        leaf.recentAdded = True
        while leaf.getParent() is not None:
            leaf.recentAdded = True
            leaf = leaf.getParent()

def deleteUnmarkNode(trees : TreeBuilder):
    def _run(head: Node):
        # copy keys
        childrenKeys = list(head.getChildren().keys())
        for key in childrenKeys:
            child = head.getChildren()[key]
            if not child.recentAdded:
                head.getChildren().pop(key)
            else:
                _run(child)
    # run
    # trees.root.recentAdded = True
    _run(trees.root)

def peekLayer(users : pd.DataFrame, trees : TreeBuilder):
    # 可以用取巧的办法，数interOrgNo的横杠数
    def getLayer(node : Node):
        return node.getTable().inter_org_no.count("-") + 1

    for i in users.index:
        orgCode = users.loc[i, C.U_org_code]
        layer = getLayer(trees.pool[orgCode])
        print("orgCode = {}, layer = {}".format(orgCode, layer))

'''
这个文件的意义是选取部分用户，并且生成最小的机构树，做一批测试数据
'''
if __name__ == '__main__':
    UuidOfUser = Uuid(header=C.H_User)
    UuidOfUserRole = Uuid(header=C.H_UserRole)
    UuidUserOrganization = Uuid(header=C.H_UserOrganization)

    # 读取机构树
    organizationTrees : TreeBuilder = loadByPickle(organizationTreesPath)

    # 如果不存在预处理文件，先处理出来
    if not isExistedFile(userPreHandledPath):
        filterAvailable()
    # 确认有用户表数据后，读取用户表
    _usersDataAll = read(userPreHandledPath)
    # 观察一下数据，可以发现能初始化的用户其实都是一级用户
    peekLayer(_usersDataAll, organizationTrees)

    # 只取部分用户
    usersData = read(userPreHandledPath).loc[_userBias : _userBias + _userCount, :]
    # usersData = read(userPreHandledPath).loc[[5, 12, 23, 34, 46], :]

    setRecentAdd(organizationTrees, False)
    markMinimunRoute(organizationTrees, usersData[C.U_org_code].values.tolist())
    deleteUnmarkNode(organizationTrees)

    # print(usersData)
    # print(organizationTrees.root.getChildren())

    # 删掉无用节点之后可以导出数据了，先出organization，再用同样的逻辑出user相关
    organizationTrees.export(buildPath(resourcePath, "out-test", "organization-test.sql"))
    # exportAll(usersData, buildPath(resourcePath, "out-test", "users-test.sql"))

    userPickle = loadByPickle(userPicklePath)
    uLogger = Logger(buildPath(resourcePath, "out-test", "users-test.sql"))
    with uLogger:
        for code in usersData.loc[:, C.U_user_code].values.tolist():
            uLogger.writeLine(userPickle[code])



    pass