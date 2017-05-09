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
parser.add_argument('--output', help='Output png filename in the working dir excluding the \'.png\' extension.')
parser.add_argument('--split', nargs='+', type=int, help='Number of assignments of each type. ' +
                    'Typically just the number of discussion assignments, but can include further ' +
                    'kinds of assignments. E.g. `--split 20 40` means assignments 1-20 are of ' +
                    'one kind, 21-40 are of a 2nd kind, 40-end are of a 3rd kind.')
args = parser.parse_args()

def create_vis(matrix, type):
    embs = matrix.mean(axis=1)
    matrix = matrix[embs.argsort()]

    r_input = '_r_length_dist_input' + str(s) + '.csv'
    pd.DataFrame(matrix).to_csv(os.path.join(args.dir, r_input), index=False)
    call(["Rscript", "r5_students_fancy_3d.R", args.dir, r_input, args.output + '_s' + str(s) +
          '_' + type + '.html'])
    os.remove(os.path.join(args.dir, r_input))

data = common.load_data(os.path.join(args.dir, args.input + '.json'), args.split)
for s in range(len(args.split) + 1):
    create_vis(data['lengths_matrices'][s], 'lengths')
    create_vis(data['scores_matrices'][s], 'scores')
    create_vis(data['time_matrices'][s], 'time')
