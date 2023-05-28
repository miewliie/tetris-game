class Color:
    r: int
    g: int
    b: int

    def __init__(self, r,g,b):
        if r not in range(0,256):
            raise ValueError('r value out of range: {}'.format(r))
        if g not in range(0,256):
            raise ValueError('g value out of range: {}'.format(g))
        if b not in range(0,256):
            raise ValueError('b value out of range: {}'.format(b))
        self.r = r
        self.g = g
        self.b = b

