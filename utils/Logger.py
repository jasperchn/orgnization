

class Logger():

    def __init__(self, logPath = None) -> None:
        super().__init__()
        self.logPath = logPath

    def __enter__(self):
        self.logFile = open(self.logPath, "w+", encoding="utf-8")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def write(self, line : str):
        if self.logFile is not None:
            self.logFile.write(line)

    def writeLine(self, line : str):
        self.write(line + "\n")

    def close(self):
        self.logFile.close()