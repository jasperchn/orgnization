import time

'''
默认规则，17位，4位header，5位时间，2位保留，6位自然数

'''

local_header = 'header'
local_timestamp = 'timestamp'
local_reserve = 'reserve'
local_natural = 'natural'

defaultFormatter = {
    local_header: 4,
    local_timestamp: 5,
    local_reserve: 2,
    local_natural: 6
}


class Uuid():
    def __init__(self, formatter = defaultFormatter):
        self.formatter = formatter
        self.header = "0".zfill(self.formatter[local_header])
        self.timestamp = None
        # 控制一下高位
        self.reserve = "1" + "0".zfill(self.formatter[local_reserve] - 1)
        self.naturalId = None
        self.naturalIdLimit = int("9"*self.formatter[local_natural])
        self._innerCounter = 0
        self._checkFormatter()

    def _checkFormatter(self):
        if(self.formatter[local_timestamp] <=0 or
        self.formatter[local_reserve] <= 0 or
        self.formatter[local_header] <= 0 or
        self.formatter[local_natural] <= 0):
            raise AttributeError

    def setHeader(self, header):
        if (isinstance(header, str)  and len(header) == self.formatter[local_header]):
            self.header = header
        else:
            raise AttributeError

    def setReserve(self, reserve):
        if(isinstance(reserve, str) and len(reserve) == self.formatter[local_reserve]):
            self.reserve = reserve
        else:
            raise AttributeError

    def generate(self):
        self.timestamp = str(int(time.time()))
        if(len(self.timestamp) >= self.formatter[local_timestamp]):
            self.timestamp = self.timestamp[-self.formatter[local_timestamp]:]
        else:
            self.timestamp = self.timestamp.zfill(self.formatter[local_timestamp])

        if(self._innerCounter > self.naturalIdLimit):
            raise KeyError("oversize!")
        else:
            self.naturalId = str(self._innerCounter).zfill(self.formatter[local_natural])
            self._innerCounter += 1
        # return "{}{}{}{}".format(self.header, self.timestamp, self.reserve, self.naturalId)
        # 修改逻辑
        return "{}{}{}{}".format(self.header, self.reserve, self.timestamp, self.naturalId)
