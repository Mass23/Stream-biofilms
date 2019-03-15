import subprocess
import argparse

# python3 q2_denoise_single.py -i DATASET_NAME -n Ncores -l 20 -r 20
parser = argparse.ArgumentParser()

parser.add_argument('-i', '--id', help='ID of the dataset', type=str, action = 'store', required = True)
parser.add_argument('-n', '--Nthreads', help='Number of threads to use', type=int, action = 'store', required = True)

parser.add_argument('-l', '--Left', help='Index to trim the left part of the reads.', type=int, action = 'store', required = True)
parser.add_argument('-r', '--Right', help='Index to trim the right part of the reads.', type=int, action = 'store', required = True)

args = parser.parse_args()

dataset_id = args.id
n_threads = args.Nthreads

l = args.Left
r = args.Right


denoise_args = ['qiime','dada2', 'denoise-single',
  '--i-demultiplexed-seqs', dataset_id + '_raw.qza',
  '--p-n-threads', str(n_threads),
  '--p-trim-left', str(l),
  '--p-trunc-len', str(r),
  '--p-trunc-q 15',
  '--o-table', dataset_id + '_dada2_table.qza',
  '--o-representative-sequences', dataset_id + '_dada2_seqs.qza',
  '--o-denoising-stats', dataset_id + '_dada2_stats.qza']
subprocess.call(' '.join(denoise_args), shell = True)

stats_args = ['qiime', 'metadata', 'tabulate', '--m-input-file', dataset_id + '_dada2_stats.qza', '--o-visualization', dataset_id + '_dada2_stats.qzv']
subprocess.call(' '.join(stats_args), shell = True)

seqs_args = ['qiime', 'feature-table', 'tabulate-seqs', '--i-data', dataset_id + '_dada2_seqs.qza', '--o-visualization', dataset_id + '_dada2_seqs.qzv']
subprocess.call(' '.join(seqs_args), shell = True)
