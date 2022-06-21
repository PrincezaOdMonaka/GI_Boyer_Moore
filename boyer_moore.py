class BoyerMoore:

    def __init__(self):
        self.heuristics = set([])
        self.pattern = ""

    def set_pattern(self, p):
        self.pattern = p

    def add_heuristics(self, h):
        self.heuristics.add(h)

    def remove_heuristics(self, h):
        if h in self.heuristics:
            self.heuristics.remove(h)

    def remove_all_heuristics(self):
        self.heuristics.clear()

    def set_heuristics(self, H):
        for h in H:
            self.heuristics.add(h)

    def preprocess(self, p, alphabet):
        self.pattern = p
        if len(self.heuristics) == 0:
            return
        for h in self.heuristics:
            h.preprocess(self.pattern, alphabet=alphabet)

    def offset(self, **kwargs):
        if len(self.heuristics) == 0:
            return 1
        return max([h.offset(**kwargs) for h in self.heuristics])

    def offset_matched(self, **kwargs):
        if len(self.heuristics) == 0:
            return 1
        return max([h.offset_matched(**kwargs) for h in self.heuristics])

    def boyer_moore(self, p, t):
        """ Do Boyer-Moore matching """
        i = 0
        occurrences = []
        cnt = 0
        prev_mismatched = -1
        while i < len(t) - len(p) + 1:
            shift = 1
            mismatched = False
            for j in range(len(p) - 1, -1, -1):
                cnt += 1
                if p[j] != t[i + j]:
                    shift = max(shift, self.offset(position=j, c=t[i + j],
                                          prev_mismatch_pos=prev_mismatched, curr_mismatch_pos=j,
                                          last=t[i + len(p) - 1], after_last= t[i + len(p) if i + len(p) < len(t) else -1]))
                    mismatched = True
                    prev_mismatched = j
                    break
            if not mismatched:
                occurrences.append(i)
                shift = max(shift, self.offset_matched(last=t[i + len(p) - 1], after_last= t[i + len(p) if i + len(p) < len(t) else -1]))
            i += shift
        return occurrences

    def get_shifts(self, p, t):
        """ Do Boyer-Moore matching """
        i = 0
        search_pos = []
        occurrences = []
        cnt = 0
        prev_mismatched = -1
        while i < len(t) - len(p) + 1:
            shift = 1
            mismatched = False
            for j in range(len(p) - 1, -1, -1):
                cnt += 1
                if p[j] != t[i + j]:
                    shift = max(shift, self.offset(position=j, c=t[i + j],
                                          prev_mismatch_pos=prev_mismatched, curr_mismatch_pos=j,
                                          last=t[i + len(p) - 1], after_last= t[i + len(p) if i + len(p) < len(t) else -1]))
                    mismatched = True
                    prev_mismatched = j
                    search_pos.append(shift)
                    break
            if not mismatched:
                occurrences.append(i)
                shift = max(shift, self.offset_matched(last=t[i + len(p) - 1], after_last= t[i + len(p) if i + len(p) < len(t) else -1]))
            i += shift
        return occurrences, search_pos