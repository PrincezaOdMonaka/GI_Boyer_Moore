class BadCharacterRule:
    def __init__(self):
        self.amap = {}
        self.bad_char = []
        self.p = ''

    def preprocess(self, p, alphabet='ACGT'):
        """ Given pattern string and list with ordered alphabet characters, create
            and return a dense bad character table.  Table is indexed by offset
            then by character. """
        self.p = p
        self.alphabet = alphabet
        # Create map from alphabet characters to integers
        self.amap = {}
        for i in range(len(self.alphabet)):
            self.amap[self.alphabet[i]] = i
        # Make bad character rule table
        self.bad_char = []
        nxt = [0] * len(self.amap)
        for i in range(0, len(p)):
            c = p[i]
            assert c in self.amap
            self.bad_char.append(nxt[:])
            nxt[self.amap[c]] = i + 1

    def offset(self, **kwargs):
        """ Return # skips given by bad character rule at offset i """
        i = kwargs['position']
        c = kwargs['c']
        if c not in self.amap:
            print(c)
        assert c in self.amap
        ci = self.amap[c]
        assert i > (self.bad_char[i][ci] - 1)
        return i - (self.bad_char[i][ci] - 1)

    def offset_matched(self, **kwargs):
        return 1

    def name(self):
        return "Bad Character"

