# Soil microbiome atlas

## 1. Downloading data

References:
- Article: http://science.sciencemag.org/content/359/6373/320/
- Data: https://figshare.com/s/82a2d3f5d38ace925492

## 2. Metadata

## 3. Qiime2
### 3.1 Trimmomatic
Script: [SMA_trimmomatic.py](https://github.com/Mass23/StreamBiofilms/blob/master/SMA_trimmomatic.py)

Arguments used:
- Minlen: 200
- Trailing: 3
- Leading: 3
- Sliding-window: 4-mers / qual>20

Remove unpaired sequences as we want paired-end input in Qiime2:
```
rm *unpaired*
```

### 3.2 Import data in Qiime2
https://docs.qiime2.org/2019.1/tutorials/importing/?highlight=import

Manifest file creation: https://github.com/Mass23/StreamBiofilms/blob/master/create_manifest_SMA.py

First, import the sequences and look at the quality:
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
```

According to the quality, choose values to truncate and trim the reads, here:
- Forward: 20 - 250
- Reverse: 10 - 215

```
#!/bin/bash

source activate qiime2-2019.1

qiime dada2 denoise-paired \
  --i-demultiplexed-seqs SMA_raw.qza \
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
Yet, the data is ready to be analysed.

### 3.3 Phylogeny
Pipeline:
- Mafft: alignment
- Mask: trimming
- RAxML: builds tree
- Midpoint-root: root the tree

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

### 3.4 Taxonomoy
```
#!/bin/bash

source activate qiime2-2019.1

qiime tools import \
  --type 'FeatureData[Sequence]' \
  --input-path 85_otus.fasta \
  --output-path 85_otus.qza

qiime tools import \
  --type 'FeatureData[Taxonomy]' \
  --input-format HeaderlessTSVTaxonomyFormat \
  --input-path 85_otu_taxonomy.txt \
  --output-path ref_taxonomy.qza
  
qiime feature-classifier extract-reads \
  --i-sequences 85_otus.qza \
  --p-f-primer CCTACGGGNBGCASCAG \
  --p-r-primer GACTACNVGGGTATCTAATCC \
  --p-trunc-len 250 \
  --p-min-length 200 \
  --p-max-length 464 \
  --o-reads ref-seqs.qza
  
qiime feature-classifier fit-classifier-naive-bayes \
  --i-reference-reads ref-seqs.qza \
  --i-reference-taxonomy ref-taxonomy.qza \
  --o-classifier classifier.qza
  
qiime feature-classifier classify-sklearn \
  --i-classifier classifier.qza \
  --i-reads SMA_dada2_seqs.qza \
  --o-classification SMA_taxonomy.qza
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


