# StreamBiofilms - EMP dataset

Qiime2:
- Site: https://qiime2.org/
- Paper: https://peerj.com/preprints/27295/

Earth microbiome project:
- Project	: http://www.earthmicrobiome.org/
- Article 	: https://www.nature.com/articles/nature24621
- Github 	: https://github.com/biocore/emp

## 1. Data verification

### 1.1 Missing projects/samples
Verify that all the fasta files have been downloaded. If not, store the number of sequences available.

Script: [control_accessions.py](https://github.com/Mass23/StreamBiofilms/blob/master/control_accessions.py)

Following this, these projects were not used (as they had some or all sequences that were not available on EBI):
- ERP020884
- ERP006348
- ERP016384

### 1.2 Removing missing projects/samples from metadata file
Update the metadata .tsv file removing the projects lacking sequences, as they will not be used. Also add the data type (for qiime2) as second header.

Script: [metadata_update.py](https://github.com/Mass23/StreamBiofilms/blob/master/metadata_update.py)

### 1.3 Get stats for trimming values
Get .tsv file and histograms for each project for the following metrics:
- Length of sequences per project
- Forward primer position
- Reverse primer position

Script: [get_stats.py](https://github.com/Mass23/StreamBiofilms/blob/master/get_stats.py)

- The reads seem already trimmed (similar length for many, no primers found in the sequences)
