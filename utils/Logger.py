

class Logger():

    def __init__(self, logPath=None, mode="w+") -> None:
        super().__init__()
        self.logFile = open(logPath, mode, encoding="utf-8")

    def __enter__(self):
        if self.logFile is None:
            raise RuntimeError("file object does not exist")
        # self.logFile = open(self.logPath, "w+", encoding="utf-8")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def write(self, line : str):
        if self.logFile is not None:
            self.logFile.write(line)
        # to make chain operation available
        return self

    def writeLine(self, line : str):
        self.write(line + "\n")
        return self

    def close(self):
        print("logger shutdown, check exported file = {}".format(self.logFile.name))
        self.logFile.close()