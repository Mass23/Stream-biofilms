#!/bin/bash

source activate qiime2-2019.1

qiime tools import \
  --type 'FeatureData[Sequence]' \
  --input-path taxonomy/99_otus.fasta \
  --output-path taxonomy/99_otus.qza

qiime tools import \
  --type 'FeatureData[Taxonomy]' \
  --input-format HeaderlessTSVTaxonomyFormat \
  --input-path taxonomy/99_otu_taxonomy.txt \
  --output-path taxonomy/ref_taxonomy.qza
  
qiime feature-classifier extract-reads \
  --i-sequences taxonomy/99_otus.qza \
  --p-f-primer CCTACGGGNBGCASCAG \
  --p-r-primer GACTACNVGGGTATCTAATCC \
  --p-min-length 200 \
  --p-max-length 464 \
  --o-reads taxonomy/ref-seqs.qza
  
qiime feature-classifier fit-classifier-naive-bayes \
  --i-reference-reads taxonomy/ref-seqs.qza \
  --i-reference-taxonomy taxonomy/ref-taxonomy.qza \
  --o-classifier taxonomy/classifier.qza
  
qiime feature-classifier classify-sklearn \
  --i-classifier taxonomy/classifier.qza \
  --i-reads taxonomy/DATASET_dada2_seqs.qza \
  --o-classification taxonomy/DATASET_taxonomy.qza
