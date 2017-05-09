import pdb
import os
import pandas as pd
import numpy as np
import json
import argparse
import common
from collections import defaultdict
from subprocess import call

parser = argparse.ArgumentParser()
parser.add_argument('--dir', help='Working directory. This dir must contain the inputs. ' +
                    'Vis outputs and any intermediate outputs are written to this dir.')
parser.add_argument('--input', help='Input json filename in the working dir excluding the \'.json\' extension.')
parser.add_argument('--output', help='Output png filename int the working dir excluding the \'.png\' extension.')
parser.add_argument('--split', nargs='+', type=int, help='Number of assignments of each type. ' +
                    'Typically just the number of discussion assignments, but can include further ' +
                    'kinds of assignments. E.g. `--split 20 40` means assignments 1-20 are of ' +
                    'one kind, 21-40 are of a 2nd kind, 40-end are of a 3rd kind.')
parser.add_argument('--bins', type=int, default=30, help='Number of bins used to create stramgraph.')
args = parser.parse_args()

data = common.load_data(os.path.join(args.dir, args.input + '.json'), args.split)
for s in range(len(args.split) + 1):
    scores = data['scores_matrices'][s]
    lengths = data['lengths_matrices'][s]
    numstudents, numassigns = data['scores_matrices'][s].shape

    # Get distribution of lengths for each grade.
    lengths_dict = defaultdict(list)
    for st in range(numstudents):
        for a in range(numassigns):
            lengths_dict[int(scores[st, a])].append(lengths[st, a])

    # Split distribution of lengths into bins and count occurences for each bin for each grade.
    counts = []
    grades = sorted(lengths_dict.keys())
    bins = np.histogram(lengths, bins=args.bins)[1]
    for grade in grades:
        counts.append(np.histogram(lengths_dict[grade], bins=bins)[0])

    # Normalize counts to total to 1 for each bin.
    counts_m = np.stack(counts, axis=1)
    counts_m = counts_m / counts_m.sum(axis=1)[:,np.newaxis]

    # Create table, add bin info and drop bins with no occurences.
    table = pd.DataFrame(data=counts_m, columns=grades)
    table.index.name = 'Students'
    table.columns.name = 'Discussions'
    table['bins'] = bins[1:]
    table = table.dropna(axis=0)

    table_melted = pd.melt(table, id_vars=['bins'], var_name='grade', value_name='ratio')

    r_input = '_r_grad_dist_input' + str(s) + '.csv'
    table_melted.to_csv(os.path.join(args.dir, r_input))
    call(["Rscript", "r1_grades_length.R", args.dir, r_input, args.output + '_s' + str(s) + '.html'])
    # os.remove(os.path.join(args.dir, r_input))
