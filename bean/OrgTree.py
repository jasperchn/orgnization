from bean.Node import *
from utils.Common import *
import pandas as pd
import utils.Constant as const
from utils.Logger import *
from utils.InterOrgNoFactory import *
from utils.Uuid import *
from table.UsrDb import *

def buildNodesPool(data : pd.DataFrame) -> dict:
    pool = {}
    for i in data.index:
        line = data.loc[i]
        # tobe make: interOrgNo, orglevel， topId层次相关的值要等到树建完了才知道

        table = Organization(
            org_id=line[const.R_id],
            parent_org_id=line[const.R_parent_org_id],
            area=line[const.R_district_code],
            fi_org_type=line[const.R_level_1_code],
            org_name=line[const.R_org_name]
        )

        # 每个node初始化时都没有父节点
        pool[table.org_id] = Node(table.org_id, table, None)
    return pool

class TreeBuilder():

    def __init__(self, pool : dict, uuid = Uuid()) -> None:
        super().__init__()
        # 所有节点，节点池
        self.pool = pool
        # 最终的森林，真树根
        self.trees = []
        # 伪头结点，把森林关联到头结点上，遍历代码更紧凑
        self.root = None
        self.interOrgNoFactory = InterOrgNoFactory()
        # self.uuid = Uuid()
        self.uuid = uuid

        # 统计值
        self.treesCount = 0
        self.nodesCount = 0

    def build(self, logger : Logger = None):
        self._generate(logger)

    # 重建关联关系，列表需要倒序删除
    def _generate(self, logger : Logger):
        with logger:
            for _, node in self.pool.items():
                # 头结点，加入森林
                table : Organization = node.getTable()
                if isEmpty(table.parent_org_id):
                    self.trees.append(node)
                # 非头结点，在pool中找父节点，建立关联
                else:
                    try:
                        parentKey = table.parent_org_id
                        parentNode: Node = self.pool[parentKey]
                        # 执行树的构造
                        parentNode.addChild(node)
                        node.setParent(parentNode)
                    except KeyError:
                        # # 写log，并且跳过这个节点
                        # logger.writeLine("key error, can not find org with id = {} as parent org of {}".format(parentKey, node.key))

                        # 写log，并且将这个节点上浮为顶层节点，
                        # 特别注意！table的topOrgId会出现混乱，后续重整层级时应特别注意
                        logger.writeLine("key error, can not find org with id = {} as parent org of {}, uplift it to topOrg".format(parentKey, node.key))
                        self.trees.append(node)
            # make root
            self._generateRoot()

    # invoke this after self.trees has been set properly
    def _generateRoot(self):
        self.root = Node(key="root", value=Organization(), parent=None)
        for node in self.trees:
            self.root.addChild(node)

    # 重建层级信息，同时报告节点数量
    # 第一层需要对inter-org-no的起始值做特殊处理
    # 最合适的应该是bfs而不是dfs（bfs中插入一截对层数的判断处理interOrgNo），不过因为原本是用self.trees遍历第一层的，所以可以绕开这点
    def fixTreesLevel(self, interOrgNoHead = 30):
        self.nodesCount = 0
        self.treesCount = 0

        for i, head in enumerate(self.trees):
            # 设置初值
            table : Organization = head.getTable()
            table.org_id = self.uuid.generate()
            table.parent_org_id = None
            table.inter_org_no = self.interOrgNoFactory.getOne(str(i + interOrgNoHead))
            table.org_level = 1
            table.top_org_id = table.org_id

            self.treesCount += 1
            self.nodesCount += 1
            # 递归
            self._fixSingleTree(head, head)

        # make a brief report
        print("brief report: treeCounts = {}, nodeCounts = {}".format(self.treesCount, self.nodesCount))

    # 尾递归？
    def _fixSingleTree(self, head : Node, top: Node):
        for i, (key, node) in enumerate(head.getChildren().items()):
            currentTable : Organization = node.getTable()
            parentTable : Organization = head.getTable()
            topTable : Organization = top.getTable()

            interOrgNo = self.interOrgNoFactory.getDown(parentTable.inter_org_no)

            currentTable.org_id = self.uuid.generate()
            currentTable.parent_org_id = parentTable.org_id
            currentTable.inter_org_no = self.interOrgNoFactory.getRight(interOrgNo, i)
            currentTable.org_level = parentTable.org_level + 1
            currentTable.top_org_id = topTable.top_org_id

            self.nodesCount += 1
            self._fixSingleTree(node, top)

    # 输出要用规范的树结构出

    def export(self, path :str):
        self._toLogger(self.root, Logger(path))

    def _toLogger(self, head: Node, logger: Logger):
        for i, (key, node) in enumerate(head.getChildren().items()):
            logger.writeLine(node.getTable().insert())
            self._toLogger(node, logger)

    # def _toLogger(self, logger : Logger, close=True):
    #     for tree in self.trees:
    #         logger.writeLine(tree.getTable().insert())
    #         self._exportToLogger(tree, logger)
    #     if close:
    #         logger.close()
    #
    # def _exportToLogger(self, head, logger : Logger):
    #     for i, (key, node) in enumerate(head.getChildren().items()):
    #         logger.writeLine(node.getTable().insert())
    #         self._exportToLogger(node, logger)



    # def export(self, path :str):
    #     self._toLogger(Logger(path), True)
    #
    # def _toLogger(self, logger : Logger, close=True):
    #     for tree in self.trees:
    #         logger.writeLine(tree.getTable().insert())
    #         self._exportToLogger(tree, logger)
    #     if close:
    #         logger.close()
    #
    # def _exportToLogger(self, head, logger : Logger):
    #     for i, (key, node) in enumerate(head.getChildren().items()):
    #         logger.writeLine(node.getTable().insert())
    #         self._exportToLogger(node, logger)