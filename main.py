import sys
import os.path
from Heuristics.bad_character_rule import BadCharacterRule
from Heuristics.last_two_characters import HorspoolSunday2
from Heuristics.composite_rule import CompositeRule
from Heuristics.weak_good_suffix_rule import WeakGoodSuffix
from Heuristics.strong_good_suffix_rule import StrongGoodSuffix
from util import get_alphabet
from performance_analyser import PerformanceAnalyser


heuristics_choices = ['bc', 'sgs', 'wgs', 'hs', 'cr']

heuristics_dictionary = { 'bc' : BadCharacterRule,
                          'sgs' : StrongGoodSuffix,
                          'wgs' : WeakGoodSuffix,
                          'hs' : HorspoolSunday2,
                          'cr' : CompositeRule
                        }

def read_args(arg_list):
    algo_set = set([])
    path_list = []
    pattern_list = []

    heur_flag = False
    pattern_flag = False
    file_flag = False
    for arg in arg_list:
        if '-h' in arg:
            heur_flag = True
            pattern_flag = False
            file_flag = False
        elif '-f' in arg:
            heur_flag = False
            pattern_flag = False
            file_flag = True
        elif '-p' in arg:
            heur_flag = False
            pattern_flag = True
            file_flag = False
        elif heur_flag:
            if arg not in heuristics_choices:
                raise Exception('Heuristics not supported')
            algo_set.add(heuristics_dictionary[arg]())
        elif pattern_flag:
            pattern_list.append(arg)
        elif file_flag:
            if not os.path.isfile(arg):
                raise Exception("File " + arg + " not found")
            path_list.append(arg)
    return algo_set, path_list, pattern_list


if __name__ == '__main__':
    '''
        Usage example:
        main.py -f C:\input.fa -p ACTG TCTCA -h bc sgs
    '''
    algo_set, path_list, pattern_list = read_args(sys.argv)
    pa = PerformanceAnalyser()
    if len(path_list) == 0:
        test_directory = "./test"
        dirpath = os.path.abspath(test_directory)
        all_files = (os.path.join(basedir, filename) for basedir, dirs, files in os.walk(dirpath) for filename in files)
        path_list = sorted(all_files, key=os.path.getsize)

    pa.set_algos(algo_set)
    pa.set_patterns(pattern_list)
    for filepath in path_list:
        with open(filepath) as f:
            text = f.readlines()
            text = [line.rstrip("\n\r") for line in text if not line.startswith('>')]
            text = ''.join(text[1:])
            f.close()
            alphabet = get_alphabet(text)
            print(filepath)
            pa.analyse(text, alphabet)
            print("")

