from bean.OrgTree import *
import utils.Constant as C

if __name__ == '__main__':
    resourcePath = os.getcwd().replace("\\", "/") + "/resource"
    # srcPath = buildPath(resourcePath, "codes.csv")
    srcPath = buildPath(resourcePath, "src", "codes-patched.csv")


    df = read(srcPath)
    pool = buildNodesPool(df)
    treeBuilder = TreeBuilder(pool, uuid=Uuid(header=C.H_Organization))
    treeBuilder.build(logger = Logger(buildPath(resourcePath, "out", "buildLog.txt")))

    '''
    树恢复之后重走一遍森林，完成以下任务
    1 遍历，检查节点数量，检查有无遗漏
    2 恢复层级关系，补全node中table的interOrgNo和level，重新设置topOrgId特别地，为了避免冲撞数据库已有interOrgNo，需要设置起始值
    3 替换orgId为数字型，数据库的orgId是big int，不是字符串，可以用以前的uuid模块来生成，减一位避免冲撞数据库
    '''

    treeBuilder.fixTreesLevel(interOrgNoHead=30)
    # treeBuilder.export(filePath= buildPath(resourcePath, "out", "org.sql"))

    # organizationSql = Logger(buildPath(resourcePath, "out", "organization.sql"))
    # treeBuilder._toLogger(organizationSql, True)

    treeBuilder.export(buildPath(resourcePath, "out", "organization.sql"))
    saveByPickle(treeBuilder, buildPath(resourcePath, "out-intermediate", "organizationTrees.plk"))







    pass