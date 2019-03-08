import subprocess
import argparse

# python3 q2_taxonomy.py -i DATASET_NAME -fp STRING -rp STRING -min INT -max INT
parser = argparse.ArgumentParser()

parser.add_argument('-i', '--id', help='ID of the dataset', type=str, action = 'store', required = True)

parser.add_argument('-fp', '--ForwardPrimer', help='Forward primer sequence', type=str, action = 'store', required = True)
parser.add_argument('-rp', '--ReversePrimer', help='Reverse primer sequence', type=str, action = 'store', required = True)

parser.add_argument('-min', '--MinimalLength', help='Minimal length of the reads', type=str, action = 'store', required = True)
parser.add_argument('-max', '--MaximalLength', help='Maximal length of the reads', type=str, action = 'store', required = True)

args = parser.parse_args()

dataset_id = args.id

forward_primer = args.ForwardPrimer
reverse_primer = args.ReversePrimer

minimal_length = args.MinimalLength
maximal_length = args.MaximalLength

import1_args = ['qiime', 'tools', 'import', '--type', "'FeatureData[Sequence]'", '--input-path', 'taxonomy/99_otus.fasta', '--output-path', 'taxonomy/99_otus.qza']
subprocess.call(' '.join(import1_args), shell = True)

import2_args = ['qiime', 'tools', 'import', '--type', "'FeatureData[Taxonomy]'", '--input-format', 'HeaderlessTSVTaxonomyFormat', '--input-path', 'taxonomy/99_otu_taxonomy.txt', '--output-path', 'taxonomy/ref_taxonomy.qza']
subprocess.call(' '.join(import2_args), shell = True)

classifier_args = ['qiime', 'feature-classifier', 'extract-reads',
  '--i-sequences taxonomy/99_otus.qza',
  '--p-f-primer', forward_primer,
  '--p-r-primer', reverse_primer,
  '--p-min-length', minimal_length,
  '--p-max-length', maximal_length,
  '--o-reads', 'taxonomy/ref-seqs.qza']
subprocess.call(' '.join(classifier_args), shell = True)

fit_args = ['qiime', 'feature-classifier', 'fit-classifier-naive-bayes',
  '--i-reference-reads', 'taxonomy/ref-seqs.qza',
  '--i-reference-taxonomy', 'taxonomy/ref-taxonomy.qza',
  '--o-classifier' ,'taxonomy/classifier.qza']
subprocess.call(' '.join(fit_args), shell = True)

classify_args = ['qiime', 'feature-classifier', 'classify-sklearn',
  '--i-classifier', 'taxonomy/classifier.qza',
  '--i-reads', 'taxonomy/' + dataset_id + '_dada2_seqs.qza',
  '--o-classification', 'taxonomy/DATASET_taxonomy.qza']
subprocess.call(' '.join(classify_args), shell = True)
