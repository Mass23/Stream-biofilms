# StreamBiofilms - EMP dataset

## 1. Data verification

### 1.1 Missing projects/samples
Script: [control_accessions.py](https://github.com/Mass23/StreamBiofilms/blob/master/control_accessions.py)

Aims: Verify that all the fasta files have been downloaded. If not, store the number of sequences available.

### 1.2 Removing missing projects/samples from metadata file
Script: [metadata_update.py](https://github.com/Mass23/StreamBiofilms/blob/master/metadata_update.py)

Aims: Update the metadata .tsv file removing the projects lacking sequences, as they will not be used.
