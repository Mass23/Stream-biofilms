#!/bin/bash

source activate qiime2-2019.1

qiime dada2 denoise-paired \
  --i-demultiplexed-seqs DATASET_raw.qza \
  --p-n-threads 16 \
  --p-trim-left-f int \
  --p-trunc-len-f int \
  --p-trim-left-r int \
  --p-trunc-len-r int \
  --o-table DATASET_dada2_table.qza \
  --o-representative-sequences DATASET_dada2_seqs.qza \
  --o-denoising-stats DATASET_dada2_stats.qza \

qiime metadata tabulate \
  --m-input-file DATASET_dada2_stats.qza \
  --o-visualization DATASET_dada2_stats.qzv

qiime feature-table summarize \
  --i-table DATASET_dada2_table.qza \
  --o-visualization DATASET_dada2_table.qzv \
  --m-sample-metadata-file sample-metadata.tsv

qiime feature-table tabulate-seqs \
  --i-data DATASET_dada2_seqs.qza \
  --o-visualization DATASET_dada2_seqs.qzv
