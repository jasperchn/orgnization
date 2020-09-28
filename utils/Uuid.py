'''
默认规则，17位，4位header，5位时间，2位保留，6位自然数

'''

local_header = 'header'
local_timestamp = 'timestamp'
local_natural = 'natural'

defaultFormatterWithTime = {
    local_header: 4,
    local_timestamp: 5,
    local_natural: 6
}

defaultFormatterWithoutTime = {
    local_header: 4,
    local_timestamp: 0,
    local_natural: 13
}

class Uuid():
    def __init__(self, bias : int = 0, formatter : dict = defaultFormatterWithoutTime):
        self.formatter = formatter

        self.header = "0".zfill(self.formatter[local_header])
        self.naturalIdLimit = int("9"*self.formatter[local_natural])

        self._naturalId : str = None
        self._innerCounter : int = 0 + bias
        self._checkFormatter()

    def _checkFormatter(self):
        if(self.formatter[local_timestamp] < 0 or
        self.formatter[local_header] < 0 or
        self.formatter[local_natural] <= 0):
            raise AttributeError

    def resetHeader(self, header):
        if (isinstance(header, str)  and len(header) == self.formatter[local_header]):
            self.header = header
        else:
            raise AttributeError

    def _timestamp(self):
        ts = ""
        tsLength = self.formatter[local_timestamp]

        if tsLength > 0:
            ts = str(int(time.time()))
            if len(ts) >= tsLength:
                ts = ts[-tsLength:]
            else:
                ts = ts.zfill(tsLength)
        return ts

    def _autoincrement(self):
        if self._innerCounter >= self.naturalIdLimit:
            raise KeyError("oversize!")
        else:
            self._naturalId = str(self._innerCounter).zfill(self.formatter[local_natural])
            self._innerCounter += 1
        return self._naturalId

    def generate(self):
        return "{}{}{}".format(self.header, self._timestamp(), self._autoincrement())


