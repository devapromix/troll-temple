class Atrib(object):
    def __init__(self, max_value=1):
        self._max_value = max_value
        self.fill()

    @property
    def cur(self):
        return self._cur_value

    @cur.setter
    def cur(self, value):
        if value < 0:
            value = 0
        if value > self._max_value:
            value = self._max_value
        self._cur_value = value

    @property
    def max(self):
        return self._max_value

    @max.setter
    def max(self, value):
        self._max_value = value
        if self._cur_value > self._max_value:
            self.fill()

    def to_string(self):
        return str(round(self._cur_value)) + "/" + str(round(self._max_value))
        
    def fill(self):
        self._cur_value = self._max_value
     
    def inc(self, value):
        self._max_value += value
        if self._cur_value > self._max_value:
            self.fill()

    def dec(self, value):
        self._max_value -= value
        if self._max_value < 0:
            self._max_value = 0
        if self._cur_value > self._max_value:
            self.fill()
     
    def modify(self, value):
        self._cur_value += value
        if self._cur_value < 0:
            self._cur_value = 0
        if self._cur_value > self._max_value:
            self.fill()
