from Heuristics.weak_good_suffix_rule import n_array
from Heuristics.weak_good_suffix_rule import small_l_prime_array
from Heuristics.weak_good_suffix_rule import big_l_array
from Heuristics.weak_good_suffix_rule import big_l_prime_array


class StrongGoodSuffix:

    def __init__(self):
        self.jump = []
        self.amap = {}
        self.small_l_prime = []
        self.big_l = []
        self.lp = []
        self.p = ''
        self.alphabet = ''

    def clear(self):
        self.jump = []
        self.amap = {}
        self.small_l_prime = []
        self.big_l = []
        self.lp = []

    def preprocess(self, p, alphabet = 'ACGT'):
        self.clear()
        self.alphabet = alphabet
        self.p = p

        for i in range(len(self.alphabet)):
            self.amap[self.alphabet[i]] = i

        n = n_array(self.p)
        self.small_l_prime = small_l_prime_array(n)
        self.lp = big_l_prime_array(p, n)
        self.big_l = big_l_array(p, self.lp)
        length = len(self.big_l)

        for k in range(len(p) - 1):
            if self.big_l[k + 1] > 0:
                shift = length - self.big_l[k + 1]
                c = p[k - shift]
                assert c in self.amap
                if c != p[k]:
                    self.jump.append(shift)
                    continue

                for pos in range(length - 2, -1, -1):
                    i = length - 1
                    matched = True
                    j = pos
                    while j >= 0 and i > k:
                        if p[j] != p[i]:
                            matched = False
                            break
                        i = i - 1
                        j = j - 1

                    if not matched:
                        continue

                    if (j >= 0) and (i == k):
                        if p[j] == p[i]:
                            continue
                        shift = i - j
                    else:
                        shift = length - self.small_l_prime[k + 1]
            else:
                shift = length - self.small_l_prime[k + 1]
            self.jump.append(shift)

        self.jump.append(0)
        #for i in range(length):
        #   print(self.jump[i])

    def offset(self, **kwargs):
        """ Given a mismatch at offset i, return amount to shift
        as determined by (weak) good suffix rule. """
        i = kwargs['position']
        return self.jump[i]

    def offset_matched(self, **kwargs):
        return len(self.small_l_prime) - self.small_l_prime[1]

    def print_table(self):
        print(self.jump)

    def name(self):
        return "Strong Good Suffix"

