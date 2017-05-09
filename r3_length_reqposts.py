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
parser.add_argument('--split', nargs='+', type=int, help='Number of assignments of each type. ' +
                    'Typically just the number of discussion assignments, but can include further ' +
                    'kinds of assignments. E.g. `--split 20 40` means assignments 1-20 are of ' +
                    'one kind, 21-40 are of a 2nd kind, 40-end are of a 3rd kind.')
args = parser.parse_args()

data = common.load_data(os.path.join(args.dir, args.input + '.json'), args.split, req=True)
for s in range(len(args.split) + 1):
    postlengths_req_dict = data['postlengths_req_dict'][s]

    dists = []
    keys = sorted(postlengths_req_dict.keys())
    for k in keys:
        dist = np.array(postlengths_req_dict[k])
        dists.append(np.stack([dist, k * np.ones((dist.shape[0]))], axis=1))
    merged_matrix = np.concatenate(dists, axis=0)

    table = pd.DataFrame(data=merged_matrix, columns=['Length', 'NumReqPosts'])
    table['NumReqPosts'] = table['NumReqPosts'].map(lambda p: 'Req: ' + str(p))

    r_input = '_r_length_dist_input' + str(s) + '.csv'
    table.to_csv(os.path.join(args.dir, r_input))
    call(["Rscript", "r3_length_reqposts.R", args.dir, r_input, args.output + '_s' + str(s) + '.png'])
    os.remove(os.path.join(args.dir, r_input))
