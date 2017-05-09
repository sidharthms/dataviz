import pdb
import os
import pandas as pd
import numpy as np
import json
import argparse
import common
from subprocess import call

parser = argparse.ArgumentParser()
parser.add_argument('--dir', help='Working directory. This dir must contain the inputs. ' +
                    'Vis outputs and any intermediate outputs are written to this dir.')
parser.add_argument('--input', help='Input json filename in the working dir excluding the \'.json\' extension.')
parser.add_argument('--output', help='Output png filename int the working dir excluding the \'.png\' extension.')
parser.add_argument('--threshs', nargs='+', type=int, default=[30, 40],
                    help='Thresholds for grades in increasing order. E.g. --thresh 30 40 means 0-29 is C ' +
                    '30-39 is B and >=40 is A. This is used for color coding only.')
parser.add_argument('--split', nargs='+', type=int, help='Number of assignments of each type. ' +
                    'Typically just the number of discussion assignments, but can include further ' +
                    'kinds of assignments. E.g. `--split 20 40` means assignments 1-20 are of ' +
                    'one kind, 21-40 are of a 2nd kind, 40-end are of a 3rd kind.')
args = parser.parse_args()

data = common.load_data(os.path.join(args.dir, args.input + '.json'), args.split)
for s in range(len(args.split) + 1):
    scores = data['scores_matrices'][s].mean(axis=1)
    time = data['time_matrices'][s].mean(axis=1)
    lengths = data['lengths_matrices'][s].mean(axis=1)

    threshs = sorted([0] + args.threshs)

    grades = scores.copy()
    thresh_map = {}
    for i, thresh in enumerate(threshs):
        grades[scores > thresh] = i
        thresh_map[i] = chr(ord('A') + len(threshs) - i - 1)

    merged_matrix = np.stack([lengths, scores, time, grades], axis=1)

    table = pd.DataFrame(data=merged_matrix, columns=['lengths', 'scores', 'time', 'grades'])
    table['grades'] = table['grades'].map(thresh_map)

    r_input = '_r_pcoord_input' + str(s) + '.csv'
    table.to_csv(os.path.join(args.dir, r_input))
    call(["Rscript", "r2_parallelcoords.R", args.dir, r_input, args.output + '_s' + str(s) + '.png'])
    os.remove(os.path.join(args.dir, r_input))
