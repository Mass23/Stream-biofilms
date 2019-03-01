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

Following this, these projects were not used (as they had some or all sequences that were not available on EBI):
- ERP020884
- ERP006348
- ERP016384

#### 1.2.2 Removing missing projects/samples from folder and metadata file
Update the metadata .tsv file removing the projects lacking sequences, as they will not be used. Also add the data type (for qiime2) as second header.

Script: [metadata_update.py](https://github.com/Mass23/StreamBiofilms/blob/master/metadata_update.py)

#### 1.2.3 Get stats for trimming values
Get .tsv file and histograms for each project for the following metrics:
- Length of sequences per project

Script: [get_stats.py](https://github.com/Mass23/StreamBiofilms/blob/master/get_stats.py)

## 2. Processing data
### 2.2 Import in qiime2 format, remove adaptors contamination and process using dada2



