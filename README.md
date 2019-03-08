# 1. Pipeline
## 1.1 Data and metadata
References:
- Article / Data / Metadata

Sequencing: 
  - Illumina MiSeq Amplicon - 16s / 454 Pyrosequencing Amplicon - 16s / etc.
  
Reads length:
  - 300bp / 150bp / 100bp / etc.
  
Primers: 
  - 341f / 805r / etc.

Environments:
  - Glacier fed streams (GS) / Meltwater (MW) / Glaciers (GL) / Cryoconites (CC) / Sediments (SD) / Soils (SO) / River (RI) / Wet land (WL) / Arctic soils (AS) / Lakes (LA) / Fjords ( FJ) / Multiple (MU)
 
Types:
  - Local / Global

## 1.2 Pre-processing

### 1.2.1 Qiime2 - Import and visualise

```source activate qiime2-2019.1```

Manifest file creation: https://github.com/Mass23/StreamBiofilms/blob/master/create_manifest.py

Script: [q2_import_visualise.py](https://github.com/Mass23/StreamBiofilms/blob/master/q2_import_visualise.py)

```python3 q2_import_visualise.py -i DATASET_NAME```

### 1.2.2 Dada2 - denoising

Script [q2_denoise.py](https://github.com/Mass23/StreamBiofilms/blob/master/q2_denoise.py)
- Apply the thresholds defined at step 1.2.1

```python3 q2_denoise.py -i DATASET_NAME -n NCORES -lf FORWARD_LEFT_TRIM -rf FORWARD_RIGHT_TRIM -lr REVERSE_LEFT_TRIM -rr REVERSE_RIGHT_TRIM```

Dada2 options:

- Trimming forward
    - Leading:  int
    - Trailing: int
    
- Trimming reverse
    - Leading:  int
    - Trailing: int

### 1.3 Phylogeny
Script: [q2_phylogeny.py](https://github.com/Mass23/StreamBiofilms/blob/master/q2_phylogeny.py)

```python3 q2_phylogeny.py -i DATASET_NAME -n N_THREADS -b N_BOOTSTRAP```

### 1.4 Taxonomy
Script: [q2_taxonomy.py](https://github.com/Mass23/StreamBiofilms/blob/master/q2_taxonomy.py)

# 2. Datasets
## 2.1 Glacier-fed streams
### 2.1.1 - GS01 (Alpine glacier-fed streams)
**References**:

- Article: https://www.nature.com/articles/ismej201344.pdf
- Data: https://www.ncbi.nlm.nih.gov/sra?linkname=bioproject_sra_all&from_uid=177803
- Metadata: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3721114/bin/ismej201344x1.pdf

**Specifications**:

- Sequencing: 454 Pyrosequencing Amplicon - 16s
- Reads length: 447
- Primers: 515f / 926r
- Environment: Glacier-fed streams
- Type: local

**Dada2**:

- Trimming forward
    - Leading: 
    - Trailing: 
    
- Trimming reverse
    - Leading: 
    - Trailing: 

**Comments**: 

## 2.2 Meltwater
## 2.3 Glaciers
## 2.4 Cryoconites
## 2.5 Sediments
## 2.6 Soils
### 2.6.1 - SO01 (Soil microbiome atlas)
**References**:

- Article: http://science.sciencemag.org/content/359/6373/320/
- Data: https://figshare.com/s/82a2d3f5d38ace925492
- Metadata: https://figshare.com/s/82a2d3f5d38ace925492

**Specifications**:

- Sequencing: Illumina MiSeq Amplicon - 16s
- Reads length: 300
- Primers: 341f / 805r
- Environment: Soil
- Type: global

**Dada2**:

- Trimming forward
    - Leading: 17
    - Trailing: 277
    
- Trimming reverse
    - Leading: 7
    - Trailing: 223

**Comments**: 
- Very bad quality reverse reads!

## 2.7 Rivers
## 2.8 Wet lands
## 2.9 Arctic soils
## 2.10 Lakes
## 2.11 Fjords
## 2.12 Multiple


