import unittest
import time
from Heuristics.bad_character_rule import BadCharacterRule
from Heuristics.strong_good_suffix_rule import StrongGoodSuffix
from Heuristics.weak_good_suffix_rule import WeakGoodSuffix
from Heuristics.composite_rule import CompositeRule
from Heuristics.last_two_characters import HorspoolSunday2
from boyer_moore import BoyerMoore
from util import get_alphabet


class TestBoyerMoore(unittest.TestCase):

    def test_util(self):
        pattern = ''
        alphabet = get_alphabet(pattern)
        self.assertEqual(alphabet, '')

        pattern = 'BABABABAAA'
        alphabet = get_alphabet(pattern)
        self.assertNotEqual(alphabet, 'BA')
        self.assertEqual(alphabet, 'AB')

        pattern = 'DADBFABDCFDFF'
        alphabet = get_alphabet(pattern)
        self.assertEqual(alphabet, 'ABCDF')

    def test_bad_character_rule1(self):
        text = 'CTGAAGTACGATTATA'
        pattern = 'TCTA'
        bc = BadCharacterRule()
        bc.preprocess(pattern, get_alphabet(pattern))
        self.assertEqual(bc.bad_char, [[0, 0, 0], [0, 0, 1], [0, 2, 1], [0, 2, 3]])
        shift = []
        alphabet = get_alphabet(pattern)
        for i in range(len(pattern)):
            row=[]
            for ch in alphabet:
                row.append(bc.offset(position=i, c=ch))
            shift.append(row)

        self.assertEqual(shift, [[1, 1, 1], [2, 2, 1], [3, 1, 2], [4, 2, 1]])

    def test_bad_character_rule2(self):
        pattern = 'ATCCCABTCCTA'
        alphabet = get_alphabet(pattern)
        test_bc = BadCharacterRule()
        test_bc.preprocess(pattern, alphabet)
        self.assertEqual(test_bc.amap, {'A': 0, 'B': 1, 'C': 2, 'T': 3})
        self.assertEqual(test_bc.bad_char, [[0, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 2], [1, 0, 3, 2],
                                            [1, 0, 4, 2], [1, 0, 5, 2], [6, 0, 5, 2], [6, 7, 5, 2],
                                            [6, 7, 5, 8], [6, 7, 9, 8], [6, 7, 10, 8], [6, 7, 10, 11]])

        shift = []
        for i in range(len(pattern)):
            row=[]
            for ch in alphabet:
                row.append(test_bc.offset(position=i, c=ch))
            shift.append(row)

        self.assertEqual(shift, [[1, 1, 1, 1], [1, 2, 2, 2], [2, 3, 3, 1], [3, 4, 1, 2],
                                 [4, 5, 1, 3], [5, 6, 1, 4], [1, 7, 2, 5], [2, 1, 3, 6],
                                 [3, 2, 4, 1], [4, 3, 1, 2], [5, 4, 1, 3], [6, 5, 2, 1]])

    def test_strong_good_suffix_rule1(self):
        pattern = 'CTTACTTAC'
        alphabet = get_alphabet(pattern)
        test_sgs = StrongGoodSuffix()
        test_sgs.preprocess(pattern, alphabet)
        shift = test_sgs.offset(position=5)
        self.assertEqual(shift, 8)

    def test_strong_good_suffix_rule2(self):
        pattern = 'CTTACTTAC'
        alphabet = get_alphabet(pattern)
        test_sgs = StrongGoodSuffix()
        test_sgs.preprocess(pattern, alphabet)
        self.assertEqual(test_sgs.jump, [4, 4, 4, 4, 8, 8, 8, 8, 0])

    def test_weak_good_suffix_rule1(self):
        pattern = 'CTTACTTAC'
        alphabet = get_alphabet(pattern)
        test_sgs = WeakGoodSuffix()
        test_sgs.preprocess(pattern, alphabet)
        shift = test_sgs.offset(position=5)
        self.assertEqual(shift, 4)

    def test_weak_good_suffix_rule2(self):
        pattern = 'CTTACTTAC'
        alphabet = get_alphabet(pattern)
        test_wgs = WeakGoodSuffix()
        test_wgs.preprocess(pattern, alphabet)
        shift = []
        for i in range(0, len(pattern)):
            shift.append(test_wgs.offset(position=i))
        self.assertEqual(shift, [4, 4, 4, 4, 4, 4, 4, 4, 0])

    def test_composite_rule1(self):
        pattern = 'TCTTAACT'
        alphabet = get_alphabet(pattern)
        test_cr = CompositeRule()
        test_cr.preprocess(pattern, alphabet)
        self.assertEqual(test_cr.composite_jumps, [[7, 7, 7, 7, 7, 5, 4, 1],
                                                   [7, 7, 7, 7, 7, 5, 4, 1],
                                                   [7, 7, 7, 7, 7, 5, 4, 1],
                                                   [7, 7, 7, 7, 7, 5, 4, 1],
                                                   [7, 7, 7, 7, 7, 5, 4, 1],
                                                   [7, 7, 7, 7, 7, 5, 4, 2],
                                                   [7, 7, 7, 7, 7, 5, 4, 3],
                                                   [7, 7, 7, 7, 7, 5, 7, 1],
                                                   [7, 7, 7, 7, 7, 5, 4, 0]])

    def test_composite_rule2(self):
        pattern = '101101'
        alphabet = get_alphabet(pattern)
        test_cr = CompositeRule()
        test_cr.preprocess(pattern, alphabet)
        self.assertEqual(test_cr.composite_jumps, [[3, 3, 3, 5, 2, 4], [3, 3, 3, 5, 2, 4], [3, 3, 3, 5, 2, 4], [3, 3, 3, 5, 2, 1],
                                                   [3, 3, 3, 5, 5, 4], [3, 3, 3, 5, 5, 6], [3, 3, 3, 5, 2, 0]])

    def test_last_two_characters_rule1(self):
        pattern = 'TGAAT'
        alphabet = get_alphabet(pattern)
        test_hs = HorspoolSunday2()
        test_hs.preprocess(pattern, alphabet)
        self.assertEqual(test_hs.last_occur_table, [3, 1, 4])

    def test_last_two_characters_rule2(self):
        pattern = 'TGAAT'
        alphabet = get_alphabet(pattern)
        test_hs = HorspoolSunday2()
        test_hs.preprocess(pattern, alphabet)

        shift = []
        for i in alphabet:
            row = []
            for j in alphabet:
                row.append(test_hs.offset(last=i, after_last=j))
            shift.append(row)
        self.assertEqual(shift, [[2, 5, 1], [3, 5, 5], [5, 4, 5]])

    def test_boyer_moore1(self):
        bm = BoyerMoore()
        self.assertEqual(bm.pattern, '')
        self.assertEqual(bm.heuristics, set([]))

        bc = BadCharacterRule()
        cr = CompositeRule()
        hs = HorspoolSunday2()
        sgs = StrongGoodSuffix()
        wgs = WeakGoodSuffix()


        pattern = 'TCAA'
        text = 'GCTAGCTCTACGAGTCTA'
        expected_result = []
        alphabet = get_alphabet(text)

        bm.add_heuristics(bc)
        self.assertEqual(bm.heuristics, {bc})
        bm.preprocess(p=pattern, alphabet=alphabet)
        result = bm.boyer_moore(pattern, text)
        self.assertEqual(result, expected_result)
        bm.remove_heuristics(bc)
        self.assertEqual(bm.heuristics, set([]))

        bm.add_heuristics(cr)
        self.assertEqual(bm.heuristics, {cr})
        bm.preprocess(p=pattern, alphabet=alphabet)
        result = bm.boyer_moore(pattern, text)
        self.assertEqual(result, expected_result)
        bm.remove_heuristics(cr)
        self.assertEqual(bm.heuristics, set([]))

        bm.add_heuristics(hs)
        self.assertEqual(bm.heuristics, {hs})
        bm.preprocess(p=pattern, alphabet=alphabet)
        result = bm.boyer_moore(pattern, text)
        self.assertEqual(result, expected_result)
        bm.remove_heuristics(hs)
        self.assertEqual(bm.heuristics, set([]))

        bm.add_heuristics(sgs)
        self.assertEqual(bm.heuristics, {sgs})
        bm.preprocess(p=pattern, alphabet=alphabet)
        result = bm.boyer_moore(pattern, text)
        self.assertEqual(result, expected_result)
        bm.remove_heuristics(sgs)
        self.assertEqual(bm.heuristics, set([]))

        bm.add_heuristics(wgs)
        self.assertEqual(bm.heuristics, {wgs})
        bm.preprocess(p=pattern, alphabet=alphabet)
        result = bm.boyer_moore(pattern, text)
        self.assertEqual(result, expected_result)
        bm.remove_heuristics(wgs)
        self.assertEqual(bm.heuristics, set([]))

    def test_boyer_moore2(self):
        bm = BoyerMoore()
        self.assertEqual(bm.heuristics, set([]))

        bc = BadCharacterRule()
        cr = CompositeRule()
        hs = HorspoolSunday2()
        sgs = StrongGoodSuffix()
        wgs = WeakGoodSuffix()

        pattern = 'TCTA'
        text = 'GCTAGCTCTACGAGTCTA'
        expected_result = [6, 14]
        alphabet = get_alphabet(text)

        bm.add_heuristics(bc)
        self.assertEqual(bm.heuristics, {bc})
        bm.preprocess(p=pattern, alphabet=alphabet)
        result = bm.boyer_moore(pattern, text)
        self.assertEqual(result, expected_result)
        bm.remove_heuristics(bc)
        self.assertEqual(bm.heuristics, set([]))

        bm.add_heuristics(cr)
        self.assertEqual(bm.heuristics, {cr})
        bm.preprocess(p=pattern, alphabet=alphabet)
        result = bm.boyer_moore(pattern, text)
        self.assertEqual(result, expected_result)
        bm.remove_heuristics(cr)
        self.assertEqual(bm.heuristics, set([]))

        bm.add_heuristics(hs)
        self.assertEqual(bm.heuristics, {hs})
        bm.preprocess(p=pattern, alphabet=alphabet)
        result = bm.boyer_moore(pattern, text)
        self.assertEqual(result, expected_result)
        bm.remove_heuristics(hs)
        self.assertEqual(bm.heuristics, set([]))

        bm.add_heuristics(sgs)
        self.assertEqual(bm.heuristics, {sgs})
        bm.preprocess(p=pattern, alphabet=alphabet)
        result = bm.boyer_moore(pattern, text)
        self.assertEqual(result, expected_result)
        bm.remove_heuristics(sgs)
        self.assertEqual(bm.heuristics, set([]))

        bm.add_heuristics(wgs)
        self.assertEqual(bm.heuristics, {wgs})
        bm.preprocess(p=pattern, alphabet=alphabet)
        result = bm.boyer_moore(pattern, text)
        self.assertEqual(result, expected_result)
        bm.remove_heuristics(wgs)
        self.assertEqual(bm.heuristics, set([]))

    def test_boyer_moore3(self):
        bm = BoyerMoore()
        self.assertEqual(bm.heuristics, set([]))

        bc = BadCharacterRule()
        cr = CompositeRule()
        hs = HorspoolSunday2()
        sgs = StrongGoodSuffix()
        wgs = WeakGoodSuffix()

        pattern = 'TGAAT'
        text = 'CTTATCGATGAAACTGAATCGTACTCAGGTCA'
        expected_result = [14]
        alphabet = get_alphabet(text)

        bm.add_heuristics(bc)
        self.assertEqual(bm.heuristics, {bc})
        bm.preprocess(p=pattern, alphabet=alphabet)
        result = bm.boyer_moore(pattern, text)
        self.assertEqual(result, expected_result)
        bm.remove_heuristics(bc)
        self.assertEqual(bm.heuristics, set([]))

        bm.add_heuristics(cr)
        self.assertEqual(bm.heuristics, {cr})
        bm.preprocess(p=pattern, alphabet=alphabet)
        result = bm.boyer_moore(pattern, text)
        self.assertEqual(result, expected_result)
        bm.remove_heuristics(cr)
        self.assertEqual(bm.heuristics, set([]))

        bm.add_heuristics(hs)
        self.assertEqual(bm.heuristics, {hs})
        bm.preprocess(p=pattern, alphabet=alphabet)
        result = bm.boyer_moore(pattern, text)
        self.assertEqual(result, expected_result)
        bm.remove_heuristics(hs)
        self.assertEqual(bm.heuristics, set([]))

        bm.add_heuristics(sgs)
        self.assertEqual(bm.heuristics, {sgs})
        bm.preprocess(p=pattern, alphabet=alphabet)
        result = bm.boyer_moore(pattern, text)
        self.assertEqual(result, expected_result)
        bm.remove_heuristics(sgs)
        self.assertEqual(bm.heuristics, set([]))

        bm.add_heuristics(wgs)
        self.assertEqual(bm.heuristics, {wgs})
        bm.preprocess(p=pattern, alphabet=alphabet)
        result = bm.boyer_moore(pattern, text)
        self.assertEqual(result, expected_result)
        bm.remove_heuristics(wgs)
        self.assertEqual(bm.heuristics, set([]))

    def test_boyer_moore4(self):
        bm = BoyerMoore()
        self.assertEqual(bm.heuristics, set([]))

        bc = BadCharacterRule()
        cr = CompositeRule()
        hs = HorspoolSunday2()
        sgs = StrongGoodSuffix()
        wgs = WeakGoodSuffix()

        pattern = 'ATA'
        text = 'ATATATATTAAAT'
        expected_result = [0,2,4]
        alphabet = get_alphabet(text)

        bm.add_heuristics(bc)
        self.assertEqual(bm.heuristics, {bc})
        bm.preprocess(p=pattern, alphabet=alphabet)
        result = bm.boyer_moore(pattern, text)
        self.assertEqual(result, expected_result)
        bm.remove_heuristics(bc)
        self.assertEqual(bm.heuristics, set([]))

        bm.add_heuristics(cr)
        self.assertEqual(bm.heuristics, {cr})
        bm.preprocess(p=pattern, alphabet=alphabet)
        result = bm.boyer_moore(pattern, text)
        self.assertEqual(result, expected_result)
        bm.remove_heuristics(cr)
        self.assertEqual(bm.heuristics, set([]))

        bm.add_heuristics(hs)
        self.assertEqual(bm.heuristics, {hs})
        bm.preprocess(p=pattern, alphabet=alphabet)
        result = bm.boyer_moore(pattern, text)
        self.assertEqual(result, expected_result)
        bm.remove_heuristics(hs)
        self.assertEqual(bm.heuristics, set([]))

        bm.add_heuristics(sgs)
        self.assertEqual(bm.heuristics, {sgs})
        bm.preprocess(p=pattern, alphabet=alphabet)
        result = bm.boyer_moore(pattern, text)
        self.assertEqual(result, expected_result)
        bm.remove_heuristics(sgs)
        self.assertEqual(bm.heuristics, set([]))

        bm.add_heuristics(wgs)
        self.assertEqual(bm.heuristics, {wgs})
        bm.preprocess(p=pattern, alphabet=alphabet)
        result = bm.boyer_moore(pattern, text)
        self.assertEqual(result, expected_result)
        bm.remove_heuristics(wgs)
        self.assertEqual(bm.heuristics, set([]))

    def test_same_occurences1(self):
        bm1 = BoyerMoore()
        bm2 = BoyerMoore()
        bm1.add_heuristics(BadCharacterRule())
        bm2.add_heuristics(CompositeRule())

        filepath = '.\\test\\random.fa'
        pattern = 'AAA'
        with open(filepath) as f:
            text = f.readlines()
            text = [line.rstrip("\n\r") for line in text if not line.startswith('>')]
            text = ''.join(text[1:])
            f.close()
            alphabet = get_alphabet(text)
        bm1.preprocess(pattern, alphabet)
        bm2.preprocess(pattern, alphabet)

        occur1 = bm1.boyer_moore(pattern, text)
        occur2 = bm2.boyer_moore(pattern, text)
        self.assertEqual(occur1, occur2)

    def test_same_occurences2(self):
        bm1 = BoyerMoore()
        bm2 = BoyerMoore()
        bm1.add_heuristics(BadCharacterRule())
        bm2.add_heuristics(HorspoolSunday2())

        filepath = '.\\test\\random.fa'
        pattern = 'AAA'
        with open(filepath) as f:
            text = f.readlines()
            text = [line.rstrip("\n\r") for line in text if not line.startswith('>')]
            text = ''.join(text[1:])
            f.close()
            alphabet = get_alphabet(text)
        bm1.preprocess(pattern, alphabet)
        bm2.preprocess(pattern, alphabet)

        occur1 = bm1.boyer_moore(pattern, text)
        occur2 = bm2.boyer_moore(pattern, text)
        self.assertEqual(occur1, occur2)

    def test_same_occurences3(self):
        bm1 = BoyerMoore()
        bm2 = BoyerMoore()
        bm1.add_heuristics(BadCharacterRule())
        bm2.add_heuristics(StrongGoodSuffix())

        filepath = '.\\test\\random.fa'
        pattern = 'AAA'
        with open(filepath) as f:
            text = f.readlines()
            text = [line.rstrip("\n\r") for line in text if not line.startswith('>')]
            text = ''.join(text[1:])
            f.close()
            alphabet = get_alphabet(text)
        bm1.preprocess(pattern, alphabet)
        bm2.preprocess(pattern, alphabet)

        occur1 = bm1.boyer_moore(pattern, text)
        occur2 = bm2.boyer_moore(pattern, text)
        self.assertEqual(occur1, occur2)

    def test_same_occurences4(self):
        bm1 = BoyerMoore()
        bm2 = BoyerMoore()
        bm1.add_heuristics(BadCharacterRule())
        bm2.add_heuristics(WeakGoodSuffix())

        filepath = '.\\test\\random.fa'
        pattern = 'AAA'
        with open(filepath) as f:
            text = f.readlines()
            text = [line.rstrip("\n\r") for line in text if not line.startswith('>')]
            text = ''.join(text[1:])
            f.close()
            alphabet = get_alphabet(text)
        bm1.preprocess(pattern, alphabet)
        bm2.preprocess(pattern, alphabet)

        occur1 = bm1.boyer_moore(pattern, text)
        occur2 = bm2.boyer_moore(pattern, text)
        self.assertEqual(occur1, occur2)

    def test_same_occurences5(self):
        bm1 = BoyerMoore()
        bm2 = BoyerMoore()
        bm1.add_heuristics(CompositeRule())
        bm2.add_heuristics(HorspoolSunday2())

        filepath = '.\\test\\random.fa'
        pattern = 'AAA'
        with open(filepath) as f:
            text = f.readlines()
            text = [line.rstrip("\n\r") for line in text if not line.startswith('>')]
            text = ''.join(text[1:])
            f.close()
            alphabet = get_alphabet(text)
        bm1.preprocess(pattern, alphabet)
        bm2.preprocess(pattern, alphabet)

        occur1 = bm1.boyer_moore(pattern, text)
        occur2 = bm2.boyer_moore(pattern, text)
        self.assertEqual(occur1, occur2)

    def test_same_occurences6(self):
        bm1 = BoyerMoore()
        bm2 = BoyerMoore()
        bm1.add_heuristics(CompositeRule())
        bm2.add_heuristics(StrongGoodSuffix())

        filepath = '.\\test\\random.fa'
        pattern = 'AAA'
        with open(filepath) as f:
            text = f.readlines()
            text = [line.rstrip("\n\r") for line in text if not line.startswith('>')]
            text = ''.join(text[1:])
            f.close()
            alphabet = get_alphabet(text)
        bm1.preprocess(pattern, alphabet)
        bm2.preprocess(pattern, alphabet)

        occur1 = bm1.boyer_moore(pattern, text)
        occur2 = bm2.boyer_moore(pattern, text)
        self.assertEqual(occur1, occur2)

    def test_same_occurences7(self):
        bm1 = BoyerMoore()
        bm2 = BoyerMoore()
        bm1.add_heuristics(CompositeRule())
        bm2.add_heuristics(WeakGoodSuffix())

        filepath = '.\\test\\random.fa'
        pattern = 'AAA'
        with open(filepath) as f:
            text = f.readlines()
            text = [line.rstrip("\n\r") for line in text if not line.startswith('>')]
            text = ''.join(text[1:])
            f.close()
            alphabet = get_alphabet(text)
        bm1.preprocess(pattern, alphabet)
        bm2.preprocess(pattern, alphabet)

        occur1 = bm1.boyer_moore(pattern, text)
        occur2 = bm2.boyer_moore(pattern, text)
        self.assertEqual(occur1, occur2)

    def test_same_occurences8(self):
        bm1 = BoyerMoore()
        bm2 = BoyerMoore()
        bm1.add_heuristics(HorspoolSunday2())
        bm2.add_heuristics(StrongGoodSuffix())

        filepath = '.\\test\\random.fa'
        pattern = 'AAA'
        with open(filepath) as f:
            text = f.readlines()
            text = [line.rstrip("\n\r") for line in text if not line.startswith('>')]
            text = ''.join(text[1:])
            f.close()
            alphabet = get_alphabet(text)
        bm1.preprocess(pattern, alphabet)
        bm2.preprocess(pattern, alphabet)

        occur1 = bm1.boyer_moore(pattern, text)
        occur2 = bm2.boyer_moore(pattern, text)
        self.assertEqual(occur1, occur2)

    def test_same_occurences9(self):
        bm1 = BoyerMoore()
        bm2 = BoyerMoore()
        bm1.add_heuristics(HorspoolSunday2())
        bm2.add_heuristics(WeakGoodSuffix())

        filepath = '.\\test\\random.fa'
        pattern = 'AAA'
        with open(filepath) as f:
            text = f.readlines()
            text = [line.rstrip("\n\r") for line in text if not line.startswith('>')]
            text = ''.join(text[1:])
            f.close()
            alphabet = get_alphabet(text)
        bm1.preprocess(pattern, alphabet)
        bm2.preprocess(pattern, alphabet)

        occur1 = bm1.boyer_moore(pattern, text)
        occur2 = bm2.boyer_moore(pattern, text)
        self.assertEqual(occur1, occur2)

    def test_same_occurences10(self):
        bm1 = BoyerMoore()
        bm2 = BoyerMoore()
        bm1.add_heuristics(StrongGoodSuffix())
        bm2.add_heuristics(WeakGoodSuffix())

        filepath = '.\\test\\random.fa'
        pattern = 'AAA'
        with open(filepath) as f:
            text = f.readlines()
            text = [line.rstrip("\n\r") for line in text if not line.startswith('>')]
            text = ''.join(text[1:])
            f.close()
            alphabet = get_alphabet(text)
        bm1.preprocess(pattern, alphabet)
        bm2.preprocess(pattern, alphabet)

        occur1 = bm1.boyer_moore(pattern, text)
        occur2 = bm2.boyer_moore(pattern, text)
        self.assertEqual(occur1, occur2)

if __name__ == '__main__':
    unittest.main()
