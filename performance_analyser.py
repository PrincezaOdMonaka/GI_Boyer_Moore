import time
from boyer_moore import BoyerMoore
import tracemalloc


class PerformanceAnalyser:
    def __init__(self):
        self.patterns=[]
        self.text=""
        self.algos=set([])
        self.tick_labels = []

    def set_algos(self, algos):
        for a in algos:
            self.algos.add(a)

    def set_patterns(self, patterns):
        for p in patterns:
            self.patterns.append(p)

    def analyse(self, text, alphabet):
        bm = BoyerMoore()
        for pattern in self.patterns:
            print("For pattern: ", pattern)
            bm.set_pattern(pattern)
            occur = []
            for heur in self.algos:
                bm.add_heuristics(heur)
                tracemalloc.start()
                bm.preprocess(pattern, alphabet)
                memory_in_bytes = round(tracemalloc.get_tracemalloc_memory(), 2)
                tracemalloc.stop()
                start = time.time()
                occur.append(bm.boyer_moore(pattern, text))
                end = time.time()
                print("Time ", heur.name(), " ", round(end - start, 2))
                print("Memory ", heur.name(), " ", memory_in_bytes)
                bm.remove_heuristics(heur)
            first = occur[0]
            for elem in occur:
                assert elem == first
            print()