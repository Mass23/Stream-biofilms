import subprocess
import argparse

# python3 q2_phylogeny.py -i DATASET_NAME -n N_THREADS -b N_BOOTSTRAP
parser = argparse.ArgumentParser()

parser.add_argument('-i', '--id', help='ID of the dataset', type=str, action = 'store', required = True)
parser.add_argument('-n', '--Nthreads', help='Number of threads to use', type=int, action = 'store', required = True)

parser.add_argument('-b', '--BootStraps', help='Number of bootstraps for the RAxML inference.', type=int, action = 'store', required = True)

args = parser.parse_args()

dataset_id = args.id
n_threads = args.Nthreads
n_bootstraps = args.BootStraps

mafft_args = ['qiime', 'alignment', 'mafft', '--i-sequences', dataset_id + '_dada2_seqs.qza', '--p-n-threads', n_threads, '--o-alignment', 'phylogeny/' + dataset_id + '_aln_seqs.qza']
subprocess.call(' '.join(mafft_args), shell = True)

mask_args = ['qiime', 'alignment', 'mask', '--i-alignment', 'phylogeny/' + dataset_id + '_aln_seqs.qza', '--o-masked-alignment', 'phylogeny/' + dataset_id + '_masked_aln_seqs.qza']
subprocess.call(' '.join(mask_args), shell = True)

raxml_args = ['qiime', 'phylogeny', 'raxml-rapid-bootstrap',
    '--i-alignment', 'phylogeny/' + dataset_id + '_masked_aln_seqs.qza',
    '--p-bootstrap-replicates', n_bootstraps,
    '--p-n-threads', n_threads,
    '--p-raxml-version', 'AVX2',
    '--p-substitution-model', 'GTRCAT',
    '--o-tree', 'phylogeny/' + dataset_id + '_GTRCAT_' + n_bootstraps + 'bs.qza']
subprocess.call(' '.join(raxml_args), shell = True)

root_args = ['qiime', 'phylogeny', 'midpoint-root', '--i-tree', 'phylogeny/' + dataset_id + '_GTRCAT_' + n_bootstraps + 'bs.qza', '--o-rooted-tree', 'phylogeny/' + dataset_id + '_GTRCAT_' + n_bootstraps + 'bs.qza']
subprocess.call(' '.join(root_args), shell = True)
