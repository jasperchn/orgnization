

class Table():

    '''
    处理必填字段，用getattr
    '''
    def __init__(self,
                 org_id = None,
                 inter_org_no = None,
                 parent_org_id = None,
                 area = None,
                 fi_org_type = None,
                 org_name = None,
                 org_level = None,
                 top_org_id = None,
                 enabled = "1",
                 org_type = "fi",
                 set_fi_store = "false",
                 set_top = "false"):
        super().__init__()
        self.org_id = org_id
        self.inter_org_no = inter_org_no
        self.parent_org_id = parent_org_id
        self.area = area
        self.fi_org_type = fi_org_type
        self.org_name = org_name
        self.org_level = org_level
        self.top_org_id = top_org_id
        self.enabled = enabled
        self.org_type = org_type
        self.set_fi_store = set_fi_store
        self.set_top = set_top

    def allAttrs(self) -> dict:
        return vars(self)

class TableInjection():
    def __init__(self):
        super().__init__()
        self.attrs = list(vars(Table()).keys())

    def buildSrcValue(self, data : Table) -> tuple:
        s, v = list.copy(self.attrs), []
        for attr in s:
            v.append("'{}'".format(getattr(data, attr)))
        # special
        s.append("create_time")
        v.append("now()")
        s.append("update_time")
        v.append("now()")
        return ', '.join(s), ', '.join(v)

    def insertSql(self, tableName : str, srcFieldString : str, valueFieldString : str):
        return "insert into {} ({}) \nvalues({});\n".format(tableName, srcFieldString, valueFieldString)

    def run(self, filePath, trees : list):
        f = open(filePath, "w+", encoding="utf-8")
        for tree in trees:
            self.export(tree, f)
        f.close()

    # 遍历
    def export(self, head , file):
        for i, (key, node) in enumerate(head.getChildren().items()):
            t = self.buildSrcValue(node.getTable())
            file.write(self.insertSql("organization", *t))

            self.export(node, file)




    # # sql语句的注入写在这里好了
    # def exportSingle(self, head : Node):
    #
    #
    #
    #     pass
    #
    # def exportAll(self, heads : list):
    #     pass