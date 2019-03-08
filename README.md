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
https://docs.qiime2.org/2019.1/tutorials/importing/?highlight=import

Script [q2_dada2.sh](https://github.com/Mass23/StreamBiofilms/blob/master/q2_dada2.sh)
- Apply the thresholds defined at step 1.2.1

Dada2 options:

- Trimming forward
    - Leading:  int
    - Trailing: int
    
- Trimming reverse
    - Leading:  int
    - Trailing: int

### 1.3 Phylogeny
Script: [q2_phylogeny.sh](https://github.com/Mass23/StreamBiofilms/blob/master/q2_phylogeny.sh)

### 1.4 Taxonomy
Script: [q2_taxonomy.sh](https://github.com/Mass23/StreamBiofilms/blob/master/q2_phylogeny.sh)

# 2. Datasets
## 2.1 Soil microbiome atlas

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

Comments: 
- Very bad quality reverse reads!
