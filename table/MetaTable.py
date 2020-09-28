
class MetaTable(object):

    # 使用slot避免vars()找出tableName
    __slots__ = ["table_name"]

    def __init__(self, table_name):
        super().__init__()
        self.table_name = table_name


    def _buildSrcValue(self) -> tuple:
        s, v = [], []
        for attr, value in vars(self).items():
            if value is None:
                value = "null"
            elif isinstance(value, bool):
                value = "1" if value else "0"
            # 处理类似于 now() 的内置函数
            elif isinstance(value, str) and value.endswith("()"):
                value = value
            else:
                value = "'{}'".format(value)
            # raise RuntimeError("invalid value type to make sql")
            v.append(value)
            s.append(attr)
        return ', '.join(s), ', '.join(v)

    def _insertSql(self, srcFieldString : str, valueFieldString : str):
        return "insert into {} ({}) \nvalues({});\n".format(self.table_name, srcFieldString, valueFieldString)

    def insert(self):
        return self._insertSql(*self._buildSrcValue())
