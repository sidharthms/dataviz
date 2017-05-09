import pdb
import os
import pandas as pd
import numpy as np
import json
import argparse
import common
import math

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

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

data = common.load_data(os.path.join(args.dir, args.input + '.json'), args.split, req=True)
for s in range(len(args.split) + 1):
    posts_req_dict = data['posts_req_dict'][s]

    dists = []
    keys = sorted(posts_req_dict[0].keys())
    for l in range(2):
        for k in keys:
            dist = np.array(posts_req_dict[l][k])
            dists.append(np.stack([dist, k * np.ones((dist.shape[0])), l * np.ones((dist.shape[0]))], axis=1))
    merged_matrix = np.concatenate(dists, axis=0)

    table = pd.DataFrame(data=merged_matrix, columns=['Posts', 'Num. Req. Posts', 'Late'])
    table['Late'] = table['Late'].map({0.0: 'On-Time', 1.0: 'Late'})

    plt.figure()
    ax = sns.lmplot(data=table, x='Num. Req. Posts', y='Posts', hue='Late', x_estimator=np.mean, size=5)
    max_ytick = math.ceil(max(ax.facet_axis(0,0).get_yticks()))
    ax.set(xticks=keys, yticks=range(1, max_ytick+1))
    ax.fig.savefig(os.path.join(args.dir, args.output + '_s' + str(s) + '.png'), dpi=100)
