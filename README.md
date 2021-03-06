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

Paired-end: [q2_import_paired.py](https://github.com/Mass23/StreamBiofilms/blob/master/q2_import_paired.py)

Single-end: [q2_import_single.py](https://github.com/Mass23/StreamBiofilms/blob/master/q2_import_single.py)

```
python3 q2_import_paired.py -i DATASET_NAME

python3 q2_import_single.py -i DATASET_NAME
```

### 1.2.2 Dada2 - denoising

Paired-end: [q2_denoise_paired.py](https://github.com/Mass23/StreamBiofilms/blob/master/q2_denoise_paired.py)

Single-end: [q2_denoise_single.py](https://github.com/Mass23/StreamBiofilms/blob/master/q2_denoise_single.py)

Apply the following thresholds:
- Trimming (forward and reverse, leading and trailing):
  - 75% >= qual. 15
  - 50% >= qual. 25

```
python3 q2_denoise_paired.py -i DATASET_NAME -n N_THREADS -lf FORWARD_LEFT_TRIM -rf FORWARD_RIGHT_TRIM -lr REVERSE_LEFT_TRIM -rr REVERSE_RIGHT_TRIM

python3 q2_denoise_single.py -i DATASET_NAME -n N_THREADS -l LEFT_TRIM -r RIGHT_TRIM
```

### 1.3 Phylogeny
Script: [q2_phylogeny.py](https://github.com/Mass23/StreamBiofilms/blob/master/q2_phylogeny.py)

```python3 q2_phylogeny.py -i DATASET_NAME -n N_THREADS -b N_BOOTSTRAP```

### 1.4 Taxonomy
Script: [q2_taxonomy.py](https://github.com/Mass23/StreamBiofilms/blob/master/q2_taxonomy.py)

```python3 q2_taxonomy.py -i DATASET_NAME -fp STRING -rp STRING -min INT -max INT```

***
# 2. Datasets
___
## 2.1 Glacier-fed streams
### 2.1.1 - GS01 (Alpine glacier-fed streams)
**References**:

- Article: https://www.nature.com/articles/ismej201344.pdf
- Data: https://www.ncbi.nlm.nih.gov/sra?linkname=bioproject_sra_all&from_uid=177803
- Metadata: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3721114/bin/ismej201344x1.pdf

**Specifications**:

- Sequencing: 454 Pyrosequencing Amplicon - 16s single-end
- Reads length: 447
- Primers:
  - 515f: GTGNCAGCMGCCGCGGTAA
  - 926r: CCGYCAATTYMTTTRAGTTT

**Dada2**:

- Trimming forward
    - Leading: 0
    - Trailing: 448

**Comments**: 



### 2.1.2 - GS02 (China, glacier-fed streams in the Tianshan mountains)
**References**:

- Article: https://www.nature.com/articles/s41598-017-13086-9
- Data: https://www.ncbi.nlm.nih.gov/bioproject/PRJNA398147/
- Metadata: https://www.ncbi.nlm.nih.gov/bioproject/PRJNA398147/

**Specifications**:

- Sequencing: Illumina MiSeq Amplicon - 16s
- Reads length: 420
- Primers:
  - 338f: ACTCCTACGGGAGGCAGCA
  - 806r: GGACTACHVGGGTWTCTAAT

**Dada2**:

- Trimming forward
    - Leading:
    - Trailing:

**Comments**: 



### 2.1.3 - GS03 (McMurdo valley glacier-fed streams, Antarctica)
**References**:

- Article: https://academic.oup.com/femsec/article/92/10/fiw148/2197762#supplementary-data
- Data: https://www.ncbi.nlm.nih.gov/bioproject/PRJNA228951
- Metadata: https://www.ncbi.nlm.nih.gov/bioproject/PRJNA228951

**Specifications**:

- Sequencing: 454 Pyrosequencing - 16s
- Reads length: 
- Primers:
  - 939f: TTGACGGGGGCCCGCACAAG
  - 1492r: GTTTACCTTGTTACGACTT

**Dada2**:

- Trimming forward
    - Leading:
    - Trailing:

**Comments**: 



### 2.1.4 - GS04 ()
**References**:

- Article: 
- Data: 
- Metadata: 

**Specifications**:

- Sequencing: 
- Reads length: 
- Primers:

**Dada2**:

- Trimming forward
    - Leading:
    - Trailing:

**Comments**: 



### 2.1.5 - GS05 (Microbial communities of the Lemon Creek Glacier)
**References**:

- Article: https://www.frontiersin.org/articles/10.3389/fmicb.2015.00495/full#B3
- Data: https://www.ncbi.nlm.nih.gov/bioproject/PRJNA248307
- Metadata: 

**Specifications**:

- Sequencing: 454 Pyrosequencing - 16s
- Reads length: 300
- Primers:
  - 515f: GTGCCAGCMGCCGCGGTAA
  - 806r: GGACTACVSGGGTATCTAAT

**Dada2**:

- Trimming forward
    - Leading: 
    - Trailing: 

**Comments**: 



___
## 2.2 Meltwater

___
## 2.3 Glaciers

___
## 2.4 Cryoconites

___
## 2.5 Sediments

___
## 2.6 Soils
### 2.6.1 - SO01 (Soil microbiome atlas)
**References**:

- Article: http://science.sciencemag.org/content/359/6373/320/
- Data: https://figshare.com/s/82a2d3f5d38ace925492
- Metadata: https://figshare.com/s/82a2d3f5d38ace925492

**Specifications**:

- Sequencing: Illumina MiSeq Amplicon - 16s paired-end
- Reads length: 300
- Primers: 
  - 341f: CCTACGGGNBGCASCAG
  - 805r: GACTACNVGGGTATCTAATCC

**Dada2**:

- Trimming forward
    - Leading: 17
    - Trailing: 277
    
- Trimming reverse
    - Leading: 7
    - Trailing: 223

**Comments**: 
- Very bad quality reverse reads!

___
## 2.7 Rivers

___
## 2.8 Wet lands

___
## 2.9 Arctic soils

___
## 2.10 Lakes

___
## 2.11 Fjords

___
## 2.12 Multiple


