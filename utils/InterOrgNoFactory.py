

class InterOrgNoFactory():
    def __init__(self, delimiter : str = "-", width = 4) -> None:
        super().__init__()
        self.width = width
        self.delimiter = delimiter

    def getOne(self, orgNo : str):
        return orgNo.zfill(self.width)

    # 向右加n个
    def getRight(self, orgNo : str, bias : int) -> str:
        r = orgNo.rindex(self.delimiter)
        num = str(int(orgNo[r + 1 :]) + bias)
        return orgNo[: r + 1] + num.zfill(self.width)

    # 向下加一层
    # 支持从空开始，可设置初始值
    def getDown(self, orgNo : str = "", initial : int = 0) -> str:
        n = (str(initial)).zfill(self.width)
        if orgNo == "" or orgNo is None:
            return n
        else:
            return orgNo + self.delimiter + n
