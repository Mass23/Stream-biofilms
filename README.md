# Soil microbiome atlas

## 1. Downloading data

References:
- Article: http://science.sciencemag.org/content/359/6373/320/
- Data: https://figshare.com/s/82a2d3f5d38ace925492

## 2. Processing
### 2.1 Trimmomatic - reads filtering
Script: [SMA_trimmomatic.py](https://github.com/Mass23/StreamBiofilms/blob/master/SMA_trimmomatic.py)

Arguments used:
- Minlen: 200
- Trailing: 3
- Leading: 3
- Sliding-window: 4-mers / qual<15

Remove unpaired sequences as we want paired-end input in Qiime2:
```
rm *unpaired*
```

### 2.2 Dada2 - denoising
https://docs.qiime2.org/2019.1/tutorials/importing/?highlight=import

Manifest file creation: https://github.com/Mass23/StreamBiofilms/blob/master/SMA_create_manifest.py
```
#!/bin/bash

source activate qiime2-2019.1

qiime demux summarize \
  --i-data SMA_raw.qza \
  --o-visualization SMA_raw.qzv

qiime tools import \
  --type 'SampleData[PairedEndSequencesWithQuality]' \
  --input-path SMA_manifest.csv \
  --output-path SMA_raw.qza \
  --input-format PairedEndFastqManifestPhred33

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

### 2.3 Phylogeny
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
  --o-alignment phylogeny/SMA_aln_seqs.qza \

qiime alignment mask \
  --i-alignment phylogeny/SMA_aln_seqs.qza \
  --o-masked-alignment phylogeny/SMA_masked_aln_seqs.qza

qiime phylogeny raxml-rapid-bootstrap \
  --i-alignment phylogeny/SMA_masked_aln_seqs.qza \
  --p-bootstrap-replicates 100 \
  --p-n-threads 16 \
  --p-raxml-version AVX2 \
  --p-substitution-model GTRCAT \
  --o-tree phylogeny/SMA_GTRCAT_100bs.qza

qiime phylogeny midpoint-root \
  --i-tree phylogeny/SMA_GTRCAT_100bs.qza \
  --o-rooted-tree phylogeny/SMA_GTRCAT_100bs_rooted.qza
```

### 3.4 Taxonomy
```
#!/bin/bash

source activate qiime2-2019.1

qiime tools import \
  --type 'FeatureData[Sequence]' \
  --input-path taxonomy/85_otus.fasta \
  --output-path taxonomy/85_otus.qza

qiime tools import \
  --type 'FeatureData[Taxonomy]' \
  --input-format HeaderlessTSVTaxonomyFormat \
  --input-path taxonomy/85_otu_taxonomy.txt \
  --output-path taxonomy/ref_taxonomy.qza
  
qiime feature-classifier extract-reads \
  --i-sequences taxonomy/85_otus.qza \
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
  --i-reads taxonomy/SMA_dada2_seqs.qza \
  --o-classification taxonomy/SMA_taxonomy.qza
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


