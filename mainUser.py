import pandas as pd
from utils.Common import *
from bean.OrgTree import *
import utils.Constant as C

# globals files
resourcePath = buildPath(os.getcwd().replace("\\", "/"), "resource")
userPreHandledPath = buildPath(resourcePath, "out-intermediate", "users.csv")
organizationTreesPath = buildPath(resourcePath, "out-intermediate", "organizationTrees.plk")
userExportPath = buildPath(resourcePath, "out", "user_role_organization.sql")
userPicklePath = buildPath("resource", "out-intermediate", "users.plk")

# # global Uuid Generators
# UuidOfUser = Uuid(header=C.H_User)
# UuidOfUserRole = Uuid(header=C.H_UserRole)
# UuidUserOrganization = Uuid(header=C.H_UserOrganization)


def filterAvailable() -> str:
    # resourcePath = os.getcwd().replace("\\", "/") + "/resource"
    # preHandledPath = buildPath(resourcePath, "out", "users.csv")

    # load users-full.csv, filter those users who are valid
    df = read(buildPath(resourcePath, "src", "users.full.csv"))
    available = df[df.apply(axis=1, func=lambda s: s.ENABLED == 1 and (not isEmpty(s.USER_CODE)) and (not isEmpty(s.ORG_CODE)))]
    print("{} user(s) are counted as available, export it to {}".format(len(available), userPreHandledPath))

    # todo make it short
    '''
    USER_CODE 用来做用户名、登录名
    ORG_CODE 关联到机构表 -> 注意做存在性检查
    USER_NAME 实际上机构名，可以加上 “系统用户”后缀作为显示名
    '''
    available.loc[:, [C.U_user_code, C.U_org_code, C.U_user_name]].to_csv(path_or_buf=userPreHandledPath, index=False)
    return userPreHandledPath

'''
检查用户所关联的机构的存在性
'''
def preCheckUserOrgs(orgs : dict, users : pd.DataFrame):
    for i in users.index:
        line = users.loc[i, :]
        if not orgs.__contains__(str(line[C.U_org_code])):
            raise RuntimeError("user with id = {}, name = {}, cant find its org = {}".format(*line[[C.U_user_code, C.U_user_name, C.U_org_code]]))


# do this on a copy
def extractUser(line : pd.Series) -> User:
    return User(
        user_id = UuidOfUser.generate(),
        user_name = line[C.U_user_code],
        mobile = line[C.U_user_code],
        display_name =line[C.U_user_name] + "系统用户",   # 实际上是 {机构名} + 系统用户
        bind_enterprise = False # 不绑定企业
    )

def retrieveOrganization(line : pd.Series) -> Organization:
    orgCode = line[C.U_org_code]
    organization: Organization = (allOrgs[orgCode]).getTable()
    return organization

def extractUserOrganization(user: User, organization: Organization):
    userOrganization: UserOrganization = UserOrganization(
        id=UuidUserOrganization.generate(),
        user_id=user.user_id,
        user_org_id=organization.org_id,
        display_name=user.display_name  # not necessary
    )
    return userOrganization

def extractUserRole(user: User, role:Role):
    userRole: UserRole = UserRole(
        user_id=user.user_id,
        role_id=role.role_id
    )
    return userRole


# def exportAll(exportData : pd.DataFrame, exportPath : str):
#     logger = Logger(logPath=exportPath)
#     with logger:
#         for i in exportData.index:
#             line = exportData.loc[i, :]
#             # make user
#             user = extractUser(line)
#             # link it to organization, this orgId has been proved to be valid id, so no check is required
#             # retrieve orgId by orgCode, get roleId from dummy role
#             organization: Organization = retrieveOrganization(line)
#             role: Role = _preSetRole
#
#             # make user-organization, user-role
#             userOrganization : UserOrganization = extractUserOrganization(user, organization)
#             userRole : UserRole = extractUserRole(user, role)
#
#             # make sqls, be aware that sqls of organization are put to another file
#             # (for organizations have their hierarchy dependence)
#             logger.writeLine(user.insert())
#             logger.writeLine(userRole.insert())
#             logger.writeLine(userOrganization.insert())
#             logger.writeLine("")

def exportAll(exportData : pd.DataFrame, exportPath : str, picklePath : str = None):
    logger = Logger(logPath=exportPath)
    # 伴随一个dict准备存pickle
    p = {}
    with logger:
        for i in exportData.index:
            line = exportData.loc[i, :]
            # make user
            user = extractUser(line)
            # link it to organization, this orgId has been proved to be valid id, so no check is required
            # retrieve orgId by orgCode, get roleId from dummy role
            organization: Organization = retrieveOrganization(line)
            role: Role = _preSetRole

            # make user-organization, user-role
            userOrganization : UserOrganization = extractUserOrganization(user, organization)
            userRole : UserRole = extractUserRole(user, role)

            # make sqls, be aware that sqls of organization are put to another file
            # (for organizations have their hierarchy dependence)
            sqls = "\n".join([user.insert(), userRole.insert(), userOrganization.insert(), ""])
            logger.writeLine(sqls)
            p[user.user_name] = sqls

            # logger.writeLine(user.insert())
            # logger.writeLine(userRole.insert())
            # logger.writeLine(userOrganization.insert())
            # logger.writeLine("")
    if not isEmpty(picklePath):
        saveByPickle(p, picklePath)

if __name__ == '__main__':
    # global Uuid Generators
    UuidOfUser = Uuid(header=C.H_User)
    UuidOfUserRole = Uuid(header=C.H_UserRole)
    UuidUserOrganization = Uuid(header=C.H_UserOrganization)

    # 如果不存在预处理文件，先处理出来
    if not isExistedFile(userPreHandledPath):
        filterAvailable()
    # 确认有用户表数据后，读取用户表
    usersData = read(userPreHandledPath)

    # 读取pickle存储的organization tree
    organizationTrees : TreeBuilder = loadByPickle(organizationTreesPath)
    # load all orgs from orgTree
    allOrgs : dict = organizationTrees.pool
    # cross check if those orgs for user in users.csv is valid, do a loop
    preCheckUserOrgs(allOrgs, usersData)
    print("user - org validation done")

    # set a dummy role for all users, make it a fi? or op? doesn't matter, it's easy to change
    _preSetRole = C.ROLE_PRESET_OP

    '''
    基本情况是：
    organization 独占一个文件，处理好他的层级关系
    role 也已经初始化好了（flyway脚本设置了三个角色），此处代码挑选其中一个伪角色就可
    
    所以此段代码是以 user为中心，同时把中介表维护好，使user能够联系上organization和role 
    为了方便区分，其实可以把主键头区分一下（机构表也可以搞一搞）
    '''
    exportAll(usersData, userExportPath, userPicklePath)

    # logger = Logger(logPath=userExportPath)
    # with logger:
    #     for i in usersData.index:
    #         line = usersData.loc[i, :]
    #         # make user
    #         user = extractUser(line)
    #         # link it to organization, this orgId has been proved to be valid id, so no check is required
    #         # retrieve orgId by orgCode, get roleId from dummy role
    #         organization: Organization = retrieveOrganization(line)
    #         role: Role = _preSetRole
    #
    #         # make user-organization, user-role
    #         userOrganization : UserOrganization = extractUserOrganization(user, organization)
    #         userRole : UserRole = extractUserRole(user, role)
    #
    #         # make sqls, be aware that sqls of organization are put to another file
    #         # (for organizations have their hierarchy dependence)
    #         logger.writeLine(user.insert())
    #         logger.writeLine(userRole.insert())
    #         logger.writeLine(userOrganization.insert())
    #         logger.writeLine("")
