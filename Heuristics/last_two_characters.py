class HorspoolSunday2:

    def _init_(self):
        self.amap = {}
        self.two_map = {}
        self.last_occur_table = []
        self.p = ''
        self.alphabet = ''

    def clear(self):
        self.amap = {}
        self.two_map = {}
        self.last_occur_table = []

    def preprocess(self, p, alphabet = 'ACGT'):
        self.clear()
        self.alphabet = alphabet
        self.p = p

        for i in range(len(self.alphabet)):
            self.amap[self.alphabet[i]] = i

        table = [-1] * len(self.amap)
        for i in range(0, len(p)):
            c = p[i]
            assert c in self.amap
            table[self.amap[c]] = i
            if i > 0:
                self.two_map[p[i - 1] + p[i]] = i - 1
        self.last_occur_table = table

    """y and x are chars"""
    def offset(self, **kwargs):
        y = kwargs['last']
        x = kwargs['after_last']
        c = self.amap[x]
        if self.last_occur_table[c] == -1:
            return len(self.p) + 1
        if self.last_occur_table[c] == 0:
            return len(self.p)
        if y + x in self.two_map:
            return len(self.p) - self.two_map[y + x] - 1
        return len(self.p)

    def offset_matched(self, **kwargs):
        y = kwargs['last']
        x = kwargs['after_last']
        return self.offset(last=y, after_last=x)

    def name(self):
        return "Two Character"