from utils.TableOrganization import *
# import utils

class Node():
    # 可选父节点
    def __init__(self, key, value : Table, parent: 'Node' = None):
        self.key = key
        self.parent = parent
        self.value = value
        self.zptr = {}

        # 特殊
        self.recentAdded = None

    def getKey(self):
        return self.key

    def getTable(self) -> Table:
        return self.value

    def getRecentAdded(self):
        return self.recentAdded

    def setParent(self, parent : 'Node'):
        self.parent = parent

    def getParent(self) -> 'Node':
        return self.parent

    def addChild(self, node):
        if(isinstance(node, Node)):
            self.zptr[node.key] = node
            self.recentAdded = node

    # def getChild(self, key):
    #     return self.zptr[key]

    def getChild(self, key):
        if(self.zptr.__contains__(key)):
            return self.zptr[key]
        else:
            return None

    def getChildren(self):
        return self.zptr