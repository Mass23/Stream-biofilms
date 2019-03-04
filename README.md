# Soil microbiome atlas

## 1. Downloading data

References:
- Article: http://science.sciencemag.org/content/359/6373/320/
- Data: https://figshare.com/s/82a2d3f5d38ace925492

## 2. Qiime2
### 2.1 Import/Summarise/Dada2
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

qiime metadata tabulate --m-input-file SMA_dada2_stats.qza --o-visualization SMA_dada2_stats.qzv
```

### 2.2 Phylogeny
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

Download EMP dataset: https://github.com/biocore/emp/blob/master/code/download-sequences/download_ebi_fastq.sh

- Single-end reads
- Already demultiplexed
- Primers are already trimmed

### 1.2 Download QC
#### 1.2.1 Control accessions
Verify that all the fasta files have been downloaded. If not, store the number of sequences available.

Script: [control_accessions.py](https://github.com/Mass23/StreamBiofilms/blob/master/control_accessions.py)

#### 1.2.2 Removing missing projects/samples from folder and metadata file
Update the metadata .tsv file removing the projects lacking sequences, as they will not be used. Also add the data type (for qiime2) as second header.

Script: [metadata_update.py](https://github.com/Mass23/StreamBiofilms/blob/master/metadata_update.py)

Following this, these projects were not used (as they had some or all sequences that were not available on EBI):
- ERP020884
- ERP006348
- ERP016384

#### 1.2.3 Get length for trimming values
Get tab-separated files and histograms for the length of the reads per project, in the projects directories. A heatmap and a tab-separated file store the overall results in the dataset directory.

Script: [get_length.py](https://github.com/Mass23/StreamBiofilms/blob/master/get_length.py)

## 2. Pre-processing

Script: [preprocess_emp.py](https://github.com/Mass23/StreamBiofilms/blob/master/preprocess_emp.py)

### 2.1 Import data
https://docs.qiime2.org/2019.1/tutorials/importing/?highlight=import
```
qiime tools import \
  --type EMPSingleEndSequences \
  --input-path emp-single-end-sequences \
  --output-path emp-single-end-sequences.qza
```

### 2.2 Remove adaptors contaminants
https://docs.qiime2.org/2019.1/plugins/available/cutadapt/trim-single/
```
qiime cutadapt trim-single \
  --i-demultiplexed-sequences emp-single-end-sequences.qza \
  --p-adapter emp-adapters \
  --o-trimmed-sequences emp-trimmed.qza \
```

### 2.3 Denoise and cluster
https://docs.qiime2.org/2019.1/plugins/available/dada2/denoise-single/
```
qiime dada2 denoise-single \
  --i-demultiplexed-seqs emp-trimmed.qza \
  --p-trunc-len 90 \
  --p-trunc-q 30 \
  --o-table emp-table \
  --o-representative-sequences emp-seqs \
  --o-denoising-stats emp-stats \
```

### 2.4 Merge studies per project
https://docs.qiime2.org/2019.1/tutorials/fmt/#merging-denoised-data
```
qiime feature-table merge \
  --i-tables table-1.qza \
  --i-tables table-2.qza \
  --o-merged-table table.qza
  
qiime feature-table merge-seqs \
  --i-data rep-seqs-1.qza \
  --i-data rep-seqs-2.qza \
  --o-merged-data rep-seqs.qza
```

### 2.5 Filter table
https://docs.qiime2.org/2019.1/tutorials/filtering/
```
qiime feature-table filter-features \
  --i-table table.qza \
  --p-min-frequency 10 \
  --o-filtered-table feature-frequency-filtered-table.qza
```

## 3. Data analysis
