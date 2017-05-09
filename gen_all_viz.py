import pdb
import os
import argparse
import glob

parser = argparse.ArgumentParser()
parser.add_argument('--dir', help='Working directory. This dir must contain the inputs. ' +
                    'Vis outputs and any intermediate outputs are written to this dir.')
parser.add_argument('--input', help='Input json filename in the working dir excluding the \'.json\' extension.')
parser.add_argument('--split', nargs='+', type=int, help='Number of assignments of each type. ' +
                    'Typically just the number of discussion assignments, but can include further ' +
                    'kinds of assignments. E.g. `--split 20 40` means assignments 1-20 are of ' +
                    'one kind, 21-40 are of a 2nd kind, 40-end are of a 3rd kind.')
args = parser.parse_args()

norun = ['gen_all_viz.py', 'common.py']
scripts = [s for s in glob.glob('*.py') if s not in norun]

for s in scripts:
    call('python', s, '--dir', args.dir, '--input', args.input, '--split', args.split, '--output', s[:2])

# Additional runs:
call('python', 'p2_students_violin.py', '--dir', args.dir, '--input', args.input, '--split', args.split, '--output', 'p2_20',
     '--numstudents', 20)
call('python', 'r5_students_fancy_3d.py', '--dir', args.dir, '--input', args.input, '--split', args.split, '--output', 'r5_nosort',
     '--no_sort')
