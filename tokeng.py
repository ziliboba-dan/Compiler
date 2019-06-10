class Token(object):
    def __init__(self, type, value, x, y):
        self.type = type
        self.value = value
        self.x = x
        self.y = y

    def __str__(self):
        return 'Token({type}, {value}, {x}, {y})'.format(
            type=self.type,
            value=repr(self.value),
            x = self.x,
            y = self.y
        )

    def __repr__(self):
        return self.__str__()
