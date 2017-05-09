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

parser = argparse.ArgumentParser()
parser.add_argument('--dir', help='Working directory. This dir must contain the inputs. ' +
                    'Vis outputs and any intermediate outputs are written to this dir.')
parser.add_argument('--input', help='Input json filename in the working dir excluding the \'.json\' extension.')
parser.add_argument('--output', help='Output png filename int the working dir excluding the \'.png\' extension.')
parser.add_argument('--no_sort', default=True, action='store_true',
                    help='Do not sort students according to performance. Pick the first "numstudents" students ' +
                    'in the json data instead.')
parser.add_argument('--numstudents', type=int, help='Number of students to show violinplots for. ' +
                    'If "no_sort" is not set, students are first sorted based on performance and ' +
                    'violin plots for the lowest performing students are shown')
parser.add_argument('--split', type=int, help='Number of discussion assignments.')
args = parser.parse_args()

def plot_data(matrices, labels, save_path, y_name, reverse_sort=False):
    embs = matrices[0].mean(axis=1)
    if reverse_sort:
        embs = -embs
    labels = [labels[e] for e in embs.argsort()]
    matrices = [matrices[0][embs.argsort()], matrices[1][embs.argsort()]]

    numstudents = args.numstudents if args.numstudents else matrices[0].shape[0]
    numassigns = matrices[0].shape[1]

    disc_matrix = np.concatenate([matrices[0][:numstudents,:], np.zeros((1, numassigns))], axis=0)
    sf_matrix = np.concatenate([matrices[1][:numstudents,:], np.ones((1, numassigns))], axis=0)
    merged_matrix = np.concatenate([disc_matrix, sf_matrix], axis=1)

    labels = labels[:numstudents]
    labels.append('Type')

    table = pd.DataFrame(data=merged_matrix, index=labels)
    table_t = table.T
    table_t['Type'] = table_t['Type'].map({0.0: 'Discussion', 1.0: 'Seek & Find'})
    table_melted = pd.melt(table_t, id_vars=['Type'],
                     var_name='Student Name', value_name=y_name)


    sns.set(font_scale=1)
    fig, ax = plt.subplots(figsize=(1.6 * numstudents, 10))
    ax = sns.violinplot(x="Student Name", y=y_name, ax=ax, data=table_melted,
                        size=20, scale='width', cut=0, inner='stick', hue='Type', split=True, palette="Set2")
    fig.savefig(save_path, dpi=100)

data = common.load_data(os.path.join(args.dir, args.input + '.json'), [args.split])

base_path = os.path.join(args.dir, args.output)

plot_data(data['time_matrices'], data['student_names'], base_path + '_time.png', 'Submission Time', reverse_sort=True)
plot_data(data['lengths_matrices'], data['student_names'], base_path + '_lengths.png', 'Post Length')
