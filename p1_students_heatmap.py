import pdb
import os
import pandas as pd
import numpy as np
import json
import argparse
import common

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

def plot_data(matrix, labels, save_path, x_name='Assignments', y_name='Students', reverse_sort=False):
    embs = matrix.mean(axis=1)
    if reverse_sort:
        embs = -embs
    labels = [labels[e] for e in embs.argsort()]
    matrix = matrix[embs.argsort()]

    table = pd.DataFrame(data=matrix, index=labels)
    table.index.name = y_name
    table.columns.name = x_name
    table.columns = table.columns = range(1, len(table.columns)+1)

    plt.figure()
    width = 12
    cbar_ratio = .1 / table.shape[0]

    grid_kws = {"height_ratios": (.9, .02), "hspace": .3}
    f, (ax, cbar_ax) = plt.subplots(2, gridspec_kw=grid_kws)
    f.set_size_inches(width, .25 * table.shape[0])
    sns.heatmap(table, ax=ax, cbar_ax=cbar_ax, cbar_kws={"orientation": "horizontal"})
    f.savefig(save_path, dpi=100)

parser = argparse.ArgumentParser()
parser.add_argument('--dir', help='Working directory. This dir must contain the inputs. ' +
                    'Vis outputs and any intermediate outputs are written to this dir.')
parser.add_argument('--input', help='Input json filename in the working dir excluding the \'.json\' extension.')
parser.add_argument('--output', help='Output png filename int the working dir excluding the \'.png\' extension.')
parser.add_argument('--split', nargs='+', type=int, help='Number of assignments of each type. ' +
                    'Typically just the number of discussion assignments, but can include further ' +
                    'kinds of assignments. E.g. `--split 20 40` means assignments 1-20 are of ' +
                    'one kind, 21-40 are of a 2nd kind, 40-end are of a 3rd kind.')
args = parser.parse_args()

data = common.load_data(os.path.join(args.dir, args.input + '.json'), args.split)
for s in range(len(args.split) + 1):
    base_path = os.path.join(args.dir, args.output + '_s' + str(s) + '_')

    plot_data(data['scores_matrices'][s], data['student_names'], base_path + 'scores.png')
    plot_data(data['time_matrices'][s], data['student_names'], base_path + 'time.png', reverse_sort=True)
    plot_data(data['lengths_matrices'][s], data['student_names'], base_path + 'lengths.png')
