#!/bin/bash

source activate qiime2-2019.1

qiime tools import \
  --type 'SampleData[PairedEndSequencesWithQuality]' \
  --input-path DATASET_manifest.csv \
  --output-path DATASET_raw.qza \
  --input-format PairedEndFastqManifestPhred33

qiime demux summarize \
  --i-data DATASET_raw.qza \
  --o-visualization DATASET_raw.qzv
