import subprocess
import argparse

# python3 q2_denoise.py -i DATASET_NAME -n Ncores -lf 20 -rf 20 -lr 20 -rr 20
parser = argparse.ArgumentParser()

parser.add_argument('-i', '--id', help='ID of the dataset', type=str, action = 'store', required = True)
parser.add_argument('-n', '--Nthreads', help='Number of threads to use', type=int, action = 'store', required = True)

parser.add_argument('-lf', '--TrimLeftForward', help='Index to trim the left part of forward reads.', type=int, action = 'store', required = True)
parser.add_argument('-rf', '--TrimRightForward', help='Index to trim the right part of forward reads.', type=int, action = 'store', required = True)
parser.add_argument('-lr', '--TrimLeftReverse', help='Index to trim the left part of reverse reads.', type=int, action = 'store', required = True)
parser.add_argument('-rr', '--TrimRightReverse', help='Index to trim the right part of reverse reads.', type=int, action = 'store', required = True)

args = parser.parse_args()

dataset_id = args.id
n_threads = args.Nthreads

lf = args.TrimLeftForward
rf = args.TrimRightForward
lr = args.TrimLeftReverse
rr = args.TrimRightReverse

denoise_args = ['qiime','dada2', 'denoise-paired',
  '--i-demultiplexed-seqs', dataset_id + '_raw.qza',
  '--p-n-threads', str(n_threads),
  '--p-trim-left-f', str(lf),
  '--p-trunc-len-f', str(rf),
  '--p-trim-left-r', str(lr),
  '--p-trunc-len-r', str(rr),
  '--o-table', dataset_id + '_dada2_table.qza',
  '--o-representative-sequences', dataset_id + '_dada2_seqs.qza',
  '--o-denoising-stats', dataset_id + '_dada2_stats.qza']
subprocess.call(' '.join(denoise_args), shell = True)

stats_args = ['qiime', 'metadata', 'tabulate', '--m-input-file', dataset_id + '_dada2_stats.qza', '--o-visualization', dataset_id + '_dada2_stats.qzv']
subprocess.call(' '.join(stats_args), shell = True)

seqs_args = ['qiime', 'feature-table', 'tabulate-seqs', '--i-data', dataset_id + '_dada2_seqs.qza', '--o-visualization', dataset_id + '_dada2_seqs.qzv']
subprocess.call(' '.join(seqs_args), shell = True)

