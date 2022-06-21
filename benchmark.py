import os.path
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from boyer_moore import BoyerMoore
from Heuristics.bad_character_rule import BadCharacterRule
from Heuristics.last_two_characters import HorspoolSunday2
from Heuristics.composite_rule import CompositeRule
from Heuristics.weak_good_suffix_rule import WeakGoodSuffix
from Heuristics.strong_good_suffix_rule import StrongGoodSuffix
from util import get_alphabet
import time
import tracemalloc

'''
    Usage example:
    benchmark.py -f C:\input.fa -p ACTTA
'''

heuristics = [[BadCharacterRule(), WeakGoodSuffix()],
              [HorspoolSunday2()],
              [CompositeRule()],
              [HorspoolSunday2(), CompositeRule()],
              [BadCharacterRule(), StrongGoodSuffix()]
              ]

colors = ['#FF3030', '#8E388E', '#228B22', '#436EEE', '#EEC900']
algorithms = ['Boyer Moore',
              'Heuristics 1',
              'Heuristics 2',
              'Heuristics 1 + Heuristics 2',
              'Boyer Moore Bad Character + Strong Good Suffix'
             ]

def read_args(arg_list):
    path_list = []
    pattern_list = []

    pattern_flag = False
    file_flag = False

    for arg in arg_list:
        if '-f' in arg:
            pattern_flag = False
            file_flag = True
        elif '-p' in arg:
            pattern_flag = True
            file_flag = False
        elif pattern_flag:
            pattern_list.append(arg)
        elif file_flag:
            if not os.path.isfile(arg):
                raise Exception("File " + arg + " not found")
            path_list.append(arg)
    return path_list, pattern_list

path_list, pattern_list = read_args(sys.argv)

if len(path_list) == 0:
    test_directory = "./test"
    dirpath = os.path.abspath(test_directory)
    all_files = (os.path.join(basedir, filename) for basedir, dirs, files in os.walk(dirpath) for filename in files)
    path_list = sorted(all_files, key=os.path.getsize)


index = 0
output_dir = os.path.abspath('./output') + '\\'

for filepath in path_list:
    bm = BoyerMoore()
    with open(filepath) as f:
        text = f.readlines()
        text = [line.rstrip("\n\r") for line in text if not line.startswith('>')]
        text = ''.join(text[1:])
        f.close()
        plotting_time = []
        plotting_memory = []
        test_names = []
        positions = []
        position = 0

        for pattern in pattern_list:
            test_name = pattern
            test_names.append(test_name)
            for algorithm in heuristics:
                bm.set_heuristics(algorithm)
                tracemalloc.start()
                bm.preprocess(pattern, get_alphabet(text))
                plotting_memory.append(round(tracemalloc.get_tracemalloc_memory(), 2))
                tracemalloc.stop()
                start = time.time()
                bm.boyer_moore(pattern, text)
                end = time.time()
                plotting_time.append(round(end - start, 2))
                bm.remove_all_heuristics()
    positions = np.arange(len(test_names))
    bar_width = 0.1
    f1 = plt.figure(1)
    for index in range(0, len(algorithms)):
        plt.bar(positions, [plotting_time[i] for i in range(len(plotting_time)) if i % len(algorithms) == index], bar_width, color=colors[index], label=algorithms[index])
        positions = [x + bar_width + 0.05 for x in positions]

    middle_points = np.arange(len(test_names))
    m = len(test_names) / 2
    plt.xticks([x + bar_width * m + 0.05 * m for x in middle_points] , test_names)
    plt.title('Time in seconds')
    plt.xlabel(filepath)
    plt.ylabel('Time')
    plt.legend()
    plt.show()

    f2 = plt.figure(2)
    positions = np.arange(len(test_names))
    for index in range(0, len(algorithms)):
        plt.bar(positions, [plotting_memory[i] for i in range(len(plotting_memory)) if i % len(algorithms) == index], bar_width, color=colors[index], label=algorithms[index])
        positions = [x + bar_width + 0.05 for x in positions]

    middle_points = np.arange(len(test_names))
    m = len(test_names) / 2
    plt.xticks([x + bar_width * m + 0.05 * m for x in middle_points], test_names)
    plt.title('Memory in bytes')
    plt.xlabel(filepath)
    plt.ylabel('Memory')
    plt.legend()
    plt.show()

    algorithms = ['BM',
     'Heur 1',
     'Heur 2',
     'Heur 1 + Heur 2',
     'Strong BM'
     ]

    columns_num = len(algorithms)
    list_2d_time = [plotting_time[i:i+columns_num] for i in range(0, len(plotting_time), columns_num)]
    list_2d_memory = [plotting_memory[i:i+columns_num] for i in range(0, len(plotting_memory), columns_num)]
    df_time = pd.DataFrame(list_2d_time, columns=algorithms, dtype=float, index=test_names)
    df_memory = pd.DataFrame(list_2d_memory, columns=algorithms, dtype=float, index=test_names)

    fig1, ax = plt.subplots()
    fig1.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    table_time = ax.table(cellText=df_time.values, colLabels=df_time.columns, loc='center', colColours=colors, rowLabels=test_names, colWidths=[0.11,0.11,0.11,0.22,0.11])
    table_time.auto_set_font_size(False)
    table_time.set_fontsize(14)
    table_time.set_label(filepath)
    #table.scale(2, 2)
    fig1.tight_layout()
    plt.show()

    fig2, ax = plt.subplots()
    fig2.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    table_memory = ax.table(cellText=df_memory.values, colLabels=df_memory.columns, loc='center', colColours=colors, rowLabels=test_names, colWidths=[0.11,0.11,0.11,0.22,0.11])
    table_memory.auto_set_font_size(False)
    table_memory.set_fontsize(14)
    fig2.tight_layout()
    plt.show()