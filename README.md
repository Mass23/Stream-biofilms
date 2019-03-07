# 1. Pipeline
## 1.1 Data and metadata
References:
- Article / Data / Metadata

Sequencing: 
  - Illumina MiSeq Amplicon - 16s / etc.
  
Reads length:
  - 300bp / 150bp / etc.
  
Primers: 
  - 341f / 805r / etc.

Environments:
  - Glacier fed streams (GS) / Glaciers (GL) / Sediments (SE) / Soils (SO) / River (RI) / Wet land (WL)
 
Types:
  - Local / Global

## 1.2 Pre-processing
### 1.2.1 Trimmomatic - reads filtering
Script: [trimmomatic.py](https://github.com/Mass23/StreamBiofilms/blob/master/trimmomatic.py)

Trimmomatic options:

- Sliding-window of 4-mers: filter < 15 quality in average

- Minimum read length: 200 (MiSeq)

Remove unpaired reads:
```
rm *unpaired*
```

### 1.2.2 Qiime2 - Import and visualise
Manifest file creation: https://github.com/Mass23/StreamBiofilms/blob/master/create_manifest.py

Script [q2_import_visualise.sh](https://github.com/Mass23/StreamBiofilms/blob/master/q2_import_visualise.sh)

### 1.2.3 Dada2 - denoising
https://docs.qiime2.org/2019.1/tutorials/importing/?highlight=import

Script [q2_dada2.sh](https://github.com/Mass23/StreamBiofilms/blob/master/q2_dada2.sh)
- Apply the thresholds defined at step 1.1.2

Dada2 options:

- Trimming forward
    - Leading:  int
    - Trailing: int
    
- Trimming reverse
    - Leading:  int
    - Trailing: int

### 1.3 Phylogeny
Script [q2_phylogeny.sh](https://github.com/Mass23/StreamBiofilms/blob/master/q2_phylogeny.sh)

### 1.4 Taxonomy
Script [q2_taxonomy.sh](https://github.com/Mass23/StreamBiofilms/blob/master/q2_phylogeny.sh)

# 2. Datasets
## 2.1 Soil microbiome atlas
References:
- Article: http://science.sciencemag.org/content/359/6373/320/
- Data: https://figshare.com/s/82a2d3f5d38ace925492
- Metadata: https://figshare.com/s/82a2d3f5d38ace925492

Sequencing: Illumina MiSeq Amplicon - 16s
Reads length: 3000
Primers: 341f / 805r
Environment: Soil
Type: global

Trimmomatic:
- Minimal length: 200
- 4-mer quality: 15

Dada2:
- Trimming forward
    - Leading:
    - Trailing:
    
- Trimming reverse
    - Leading:
    - Trailing:
