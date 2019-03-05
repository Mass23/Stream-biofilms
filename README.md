# Soil microbiome atlas

## 1. Downloading data

References:
- Article: http://science.sciencemag.org/content/359/6373/320/
- Data: https://figshare.com/s/82a2d3f5d38ace925492

## 2. Metadata

## 3. Qiime2
### 3.1 Import/Summarise/Dada2
https://docs.qiime2.org/2019.1/tutorials/importing/?highlight=import

Manifest file creation: https://github.com/Mass23/StreamBiofilms/blob/master/create_manifest_SMA.py

```
#!/bin/bash

source activate qiime2-2019.1

qiime tools import \
  --type 'SampleData[PairedEndSequencesWithQuality]' \
  --input-path SMA_manifest.csv \
  --output-path SMA_raw.qza \
  --input-format PairedEndFastqManifestPhred33

qiime demux summarize \
  --i-data SMA_raw.qza \
  --o-visualization SMA_raw.qzv

qiime dada2 denoise-paired \
  --i-demultiplexed-seqs SMA_raw.qza \
  --p-trunc-len-f 250 \
  --p-trunc-len-r 215 \
  --p-trim-left-f 20 \
  --p-trim-left-r 10 \
  --p-trunc-q 20 \
  --p-n-threads 16 \
  --o-table SMA_dada2_table.qza \
  --o-representative-sequences SMA_dada2_seqs.qza \
  --o-denoising-stats SMA_dada2_stats.qza \

qiime metadata tabulate \
  --m-input-file SMA_dada2_stats.qza \
  --o-visualization SMA_dada2_stats.qzv

qiime feature-table summarize \
  --i-table SMA_dada2_table.qza \
  --o-visualization SMA_dada2_table.qzv \
  --m-sample-metadata-file sample-metadata.tsv

qiime feature-table tabulate-seqs \
  --i-data SMA_dada2_seqs.qza \
  --o-visualization SMA_dada2_seqs.qzv
```

### 3.2 Phylogeny
```
#!/bin/bash

source activate qiime2-2019.1

qiime alignment mafft \
  --i-sequences SMA_dada2_seqs.qza \
  --p-n-threads 16 \
  --o-alignment SMA_aln_seqs.qza \

qiime alignment mask \
  --i-alignment SMA_aln_seqs.qza \
  --o-masked-alignment SMA_masked_aln_seqs.qza

qiime phylogeny raxml-rapid-bootstrap \
  --i-alignment SMA_masked_aln_seqs.qza \
  --p-bootstrap-replicates 100 \
  --p-n-threads 16 \
  --p-raxml-version AVX2 \
  --p-substitution-model GTRCAT \
  --o-tree SMA_GTRCAT_100bs.qza

qiime phylogeny midpoint-root \
  --i-tree SMA_GTRCAT_100bs.qza \
  --o-rooted-tree SMA_GTRCAT_100bs_rooted.qza
```

***
# EMP dataset

## 1 Downloading data
### 1.1 Introduction

Qiime2:
- Site: https://qiime2.org/
- Paper: https://peerj.com/preprints/27295/

Earth microbiome project:
- Project	: http://www.earthmicrobiome.org/
- Article 	: https://www.nature.com/articles/nature24621
- Github 	: https://github.com/biocore/emp

Download EMP dataset: qiita.ucsd.edu


