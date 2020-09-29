'''
默认规则，17位，4位header，5位时间，2位保留，6位自然数

'''
import time

local_header = 'header'
local_timestamp = 'timestamp'
local_natural = 'natural'

defaultFormatterWithTime = {
    local_header: 5,
    local_timestamp: 5,
    local_natural: 7
}

defaultFormatterWithoutTime = {
    local_header: 5,
    local_timestamp: 0,
    local_natural: 12
}

class Uuid():
    def __init__(self, bias : int = 0, formatter : dict = defaultFormatterWithoutTime, header = None):
        self.formatter = formatter
        # header
        if header is None:
            self.header = "0".zfill(self.formatter[local_header])
        else:
            self.resetHeader(header)

        self.naturalIdLimit = int("9"*self.formatter[local_natural])

        self._naturalId : str = None
        self._innerCounter : int = 0 + bias
        self._checkFormatter()

    def _checkFormatter(self):
        if(self.formatter[local_timestamp] < 0 or
        self.formatter[local_header] < 0 or
        self.formatter[local_natural] <= 0):
            raise AttributeError

    # def resetHeader(self, header):
    #     if (isinstance(header, str)  and len(header) == self.formatter[local_header]):
    #         self.header = header
    #     else:
    #         raise AttributeError

    def resetHeader(self, header):
        hl = self.formatter[local_header]
        if isinstance(header, int):
            _h = str(header).zfill(hl)
        elif isinstance(header, str):
            _h = header.zfill(hl)
        else:
            raise TypeError("header should be int or str only")

        if len(_h) != hl:
            raise AttributeError("header too long, should be {} digits or less".format(hl))
        else:
            self.header = _h

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


