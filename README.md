# 1. Pipeline

## 1.1 Pre-processing
### 1.1.1 Trimmomatic - reads filtering
First, the sequences are filtered with trimmomatic:
- Sliding-window of 4-mers: filter < 15 quality in average
- Minimum read length: 200 (MiSeq)

Script: [trimmomatic.py](https://github.com/Mass23/StreamBiofilms/blob/master/trimmomatic.py)

Remove unpaired reads:
```
rm *unpaired*
```

### 1.1.2 Qiime2 - Import and visualise

Script [q2_import_visualise.sh](https://github.com/Mass23/StreamBiofilms/blob/master/q2_import_visualise.sh)
 
 According to the visualisation, decide for thresholds:
 - Trimming at the beginning
    - Forward: int
    - Reverse: int
 - Trimming at the end
    - Forward: int
    - Reverse: int

### 1.2.2 Dada2 - denoising
https://docs.qiime2.org/2019.1/tutorials/importing/?highlight=import

Manifest file creation: https://github.com/Mass23/StreamBiofilms/blob/master/SMA_create_manifest.py

Script [q2_dada2.sh](https://github.com/Mass23/StreamBiofilms/blob/master/q2_dada2.sh)
- Apply the thresholds defined at step 1.1.2


### 1.2.3 Phylogeny
Script [q2_phylogeny.sh](https://github.com/Mass23/StreamBiofilms/blob/master/q2_phylogeny.sh)

### 1.3.4 Taxonomy
Script [q2_taxonomy.sh](https://github.com/Mass23/StreamBiofilms/blob/master/q2_phylogeny.sh)

# 2. Datasets
## 2.1 Soil microbiome atlas
References:
- Article: http://science.sciencemag.org/content/359/6373/320/
- Data: https://figshare.com/s/82a2d3f5d38ace925492
- Metadata: https://figshare.com/s/82a2d3f5d38ace925492

Sequencing: Illumina MiSeq Amplicon - 16s
Primers: 341f / 805r
Environment: Soils
Type: global

- Trimming at the beginning
    - Forward:
    - Reverse:
 - Trimming at the end
    - Forward:
    - Reverse:

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


