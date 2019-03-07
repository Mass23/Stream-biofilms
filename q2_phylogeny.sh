#!/bin/bash

source activate qiime2-2019.1

qiime alignment mafft \
  --i-sequences DATASET_dada2_seqs.qza \
  --p-n-threads 16 \
  --o-alignment phylogeny/DATASET_aln_seqs.qza \

qiime alignment mask \
  --i-alignment phylogeny/DATASET_aln_seqs.qza \
  --o-masked-alignment phylogeny/DATASET_masked_aln_seqs.qza

qiime phylogeny raxml-rapid-bootstrap \
  --i-alignment phylogeny/DATASET_masked_aln_seqs.qza \
  --p-bootstrap-replicates 100 \
  --p-n-threads 16 \
  --p-raxml-version AVX2 \
  --p-substitution-model GTRCAT \
  --o-tree phylogeny/DATASET_GTRCAT_100bs.qza

qiime phylogeny midpoint-root \
  --i-tree phylogeny/DATASET_GTRCAT_100bs.qza \
  --o-rooted-tree phylogeny/DATASET_GTRCAT_100bs_rooted.qza
