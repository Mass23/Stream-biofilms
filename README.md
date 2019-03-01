# StreamBiofilms - EMP dataset

## 1. Downloading data

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

### 1.2 Downloading QC
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
Get .tsv file and histograms for the length of the reads per project.

Script: [get_length.py](https://github.com/Mass23/StreamBiofilms/blob/master/get_length.py)

## 2. Pre-processing
### 2.2 Import in qiime2 format, remove adaptors contamination and process using dada2

The following qiime2 plugins are used:
- Import: https://docs.qiime2.org/2019.1/tutorials/importing/?highlight=import
- Cutadapt: https://docs.qiime2.org/2019.1/plugins/available/cutadapt/trim-single/
- Dada2: https://docs.qiime2.org/2019.1/plugins/available/dada2/denoise-single/
- Merging: https://docs.qiime2.org/2019.1/tutorials/fmt/#merging-denoised-data

#### 2.1 Import data
```
qiime tools import \
  --type EMPSingleEndSequences \
  --input-path emp-single-end-sequences \
  --output-path emp-single-end-sequences.qza
```

#### 2.2 Remove adaptors contaminants
```
qiime cutadapt trim-single \
  --i-demultiplexed-sequences emp-single-end-sequences.qza \
  --p-adapter emp-adapters \
  --o-trimmed-sequences emp-trimmed.qza \
```

#### 2.3 Denoise and cluster
```
qiime dada2 denoise-single \
  --i-demultiplexed-seqs emp-trimmed.qza \
  --p-trunc-len int \
  --p-trunc-q 30 \
  --o-table emp-table \
  --o-representative-sequences emp-seqs \
  --o-denoising-stats emp-stats \
```

#### 2.4 Merge studies per project
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

#### 2.5 Filter table
```
qiime feature-table filter-features \
  --i-table table.qza \
  --p-min-frequency 10 \
  --o-filtered-table feature-frequency-filtered-table.qza
```

## 3. Data analysis

### 3.1 Taxonomic composition of the bioms

### 3.2 Phylogeny

