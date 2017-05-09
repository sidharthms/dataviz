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

def plot_data(table):
    plot = sns.tsplot(data=table, time='Assignment', unit='Student Name',
           condition='Type', value='Value', ci=[68, 95])
    plot.savefig(save_path, dpi=100)

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
    scores = data['scores_matrices'][s]
    time = data['time_matrices'][s]
    lengths = data['lengths_matrices'][s]
    names = data['student_names']

    anum = np.arange(1, scores.shape[1]+1)[np.newaxis,:]

    scores = np.concatenate([scores, 0 * np.ones((1, scores.shape[1])), anum], axis=0)
    time = np.concatenate([time, 1 * np.ones((1, time.shape[1])), anum], axis=0)
    lengths = np.concatenate([lengths / 100, 2 * np.ones((1, lengths.shape[1])), anum], axis=0)
    merged_matrix = np.concatenate([scores, time, lengths], axis=1)

    names = names + ['Type', 'Assignment']

    table = pd.DataFrame(data=merged_matrix, index=names)
    table.index.name = 'Students'
    table_t = table.T
    table_t['Type'] = table_t['Type'].map({0.0: 'Grade', 1.0: 'Submit Time', 2.0: 'Total Post Length'})
    table_melted = pd.melt(table_t, id_vars=['Assignment', 'Type'], var_name='Student Name', value_name='Value')

    table_pivot = pd.pivot_table(table_melted, index=['Student Name', 'Assignment'], columns='Type', values='Value')
    table_pivot.reset_index(inplace=True)
    table_pivot = table_pivot[['Assignment', 'Grade', 'Submit Time', 'Total Post Length']]

    plt.figure()
    ax = sns.pairplot(table_pivot, hue='Grade', size=10)
    # ax.set(ylabel='Submit Time  |  Post Length/100  |  Score')
    # ax.set_xticks(range(1, scores.shape[1]+1))
    # plt.legend(loc='best')
    ax.fig.savefig(os.path.join(args.dir, args.output + '_s' + str(s) + '.png'), dpi=100)
