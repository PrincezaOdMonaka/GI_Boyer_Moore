from Heuristics.strong_good_suffix_rule import StrongGoodSuffix


class CompositeRule(StrongGoodSuffix):

    def __init__(self):
        super().__init__()
        self.composite_jumps = []
        self.p = ''
        self.alphabet = ''

    def clear(self):
        super().clear()
        self.composite_jumps = []

    def preprocess(self, p, alphabet = 'ACGT'):
        self.alphabet = alphabet
        self.p = p
        self.clear()

        super().preprocess(p, alphabet)

        for i in range(0, len(p), 1):
            nxt = [0] * len(p)
            for j in range(0, len(p), 1):
                nxt[j] = self.jumps(p, i, j)
            self.composite_jumps.append(nxt)
        self.composite_jumps.append(self.jump)

    def jumps(self, p, i, j):
        isMatch = True
        m = len(p)
        SJump = []
        for k in range(len(p)):
            rule = super().offset(position=k)
            if rule == 0:
                rule = 1
            SJump.append(rule)
        jmp = SJump[j]

        if jmp >= m or j == 0:
            return jmp

        for jump in range(jmp, m + 1):
            isMatch = True
            k = m - 1
            while k > j and k >= jump:
                if p[k] != p[k - jump]:
                    isMatch = False
                    break
                k = k - 1
            if not isMatch:
                continue
            if (j >= jump) and (p[j] == p[j - jump]):
                continue

            isMatch = True
            delta = jump + SJump[i]
            k = m - 1
            while k > i and k >= delta:
                if p[k] != p[k - delta]:
                    isMatch = False
                    break
                k = k - 1
            if not isMatch:
                continue
            if (i >= delta) and (p[i] == p[i - delta]):
                continue
            return jump
        return jump

    def offset(self, **kwargs):
        i = kwargs['prev_mismatch_pos']
        j = kwargs['curr_mismatch_pos']
        return self.composite_jumps[i][j]

    def offset_matched(self, **kwargs):
        return len(self.small_l_prime) - self.small_l_prime[1]

    def print_jump(self):
        for i in range(len(self.p)):
            for j in range(len(self.p)):
                print(self.composite_jumps[i][j], end = " ")
            print("")

    def name(self):
        return "Composite"


