# Soil microbiome atlas

## 1. Downloading data

References:
- Article: http://science.sciencemag.org/content/359/6373/320/
- Data: https://figshare.com/s/82a2d3f5d38ace925492

## 2. Metadata

## 3. Qiime2
### 3.1 Import/Summarise/Dada2
https://docs.qiime2.org/2019.1/tutorials/importing/?highlight=import

Manifest file creation: https://github.com/Mass23/StreamBiofilms/blob/master/create_manifest_SMA.py

First, import the sequences and look at the quality:
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
```

According to the quality, choose values to truncate and trim the reads, here:
- Forward: 20 - 250
- Reverse: 10 - 215

```
#!/bin/bash

source activate qiime2-2019.1

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

qiime metadata tabulate \
  --m-input-file SMA_dada2_stats.qza \
  --o-visualization SMA_dada2_stats.qzv

qiime feature-table summarize \
  --i-table SMA_dada2_table.qza \
  --o-visualization SMA_dada2_table.qzv \
  --m-sample-metadata-file sample-metadata.tsv

qiime feature-table tabulate-seqs \
  --i-data SMA_dada2_seqs.qza \
  --o-visualization SMA_dada2_seqs.qzv
```
Yet, the data is ready to be analysed.

### 3.2 Phylogeny
Pipeline:
- Mafft: aignment
- Trimming: mask
- RAxML: builds tree
- Midpoint-root: root the tree

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

### 3.3 Diversity
```
#!/bin/bash

source activate qiime2-2019.1

qiime diversity core-metrics-phylogenetic \
  --i-phylogeny SMA_GTRCAT_100bs_rooted.qza \
  --i-table SMA_dada2_table.qza \
  --p-sampling-depth 1109 \
  --m-metadata-file SMA_metadata.txt \
  --output-dir SMA_diversity

# Alpha diversity
qiime diversity alpha-group-significance \
  --i-alpha-diversity SMA_diversity/faith_pd_vector.qza \
  --m-metadata-file SMA_metadata.txt \
  --o-visualization SMA_diversity/faith-pd-group-significance.qzv

qiime diversity alpha-group-significance \
  --i-alpha-diversity SMA_diversity/evenness_vector.qza \
  --m-metadata-file SMA_metadata.txt \
  --o-visualization SMA_diversity/evenness-group-significance.qzv

# Beta diversity
qiime diversity beta-group-significance \
  --i-distance-matrix SMA_diversity/unweighted_unifrac_distance_matrix.qza \
  --m-metadata-file SMA_metadata.txt \
  --m-metadata-column BodySite \
  --o-visualization SMA_diversity/unweighted-unifrac-body-site-significance.qzv \
  --p-pairwise

qiime diversity beta-group-significance \
  --i-distance-matrix SMA_diversity/unweighted_unifrac_distance_matrix.qza \
  --m-metadata-file SMA_metadata.txt \
  --m-metadata-column Subject \
  --o-visualization SMA_diversity/unweighted-unifrac-subject-group-significance.qzv \
  --p-pairwise

# Emperor plot
qiime emperor plot \
  --i-pcoa SMA_diversity/unweighted_unifrac_pcoa_results.qza \
  --m-metadata-file SMA_metadata.txt \
  --p-custom-axes DaysSinceExperimentStart \
  --o-visualization SMA_diversity/unweighted-unifrac-emperor-DaysSinceExperimentStart.qzv

qiime emperor plot \
  --i-pcoa SMA_diversity/bray_curtis_pcoa_results.qza \
  --m-metadata-file SMA_metadata.txt \
  --p-custom-axes DaysSinceExperimentStart \
  --o-visualization SMA_diversity/bray-curtis-emperor-DaysSinceExperimentStart.qzv

# Alpha rarefaction
qiime diversity alpha-rarefaction \
  --i-table table.qza \
  --i-phylogeny rooted-tree.qza \
  --p-max-depth 4000 \
  --m-metadata-file SMA_metadata.txt \
  --o-visualization alpha-rarefaction.qzv
```

### 3.4 Taxonomoy
```
#!/bin/bash

source activate qiime2-2019.1

qiime tools import \
  --type 'FeatureData[Sequence]' \
  --input-path 85_otus.fasta \
  --output-path 85_otus.qza

qiime tools import \
  --type 'FeatureData[Taxonomy]' \
  --input-format HeaderlessTSVTaxonomyFormat \
  --input-path 85_otu_taxonomy.txt \
  --output-path ref_taxonomy.qza
  
qiime feature-classifier extract-reads \
  --i-sequences 85_otus.qza \
  --p-f-primer CCTACGGGNBGCASCAG \
  --p-r-primer GACTACNVGGGTATCTAATCC \
  --p-trunc-len 250 \
  --p-min-length 200 \
  --p-max-length 464 \
  --o-reads ref-seqs.qza
  
qiime feature-classifier fit-classifier-naive-bayes \
  --i-reference-reads ref-seqs.qza \
  --i-reference-taxonomy ref-taxonomy.qza \
  --o-classifier classifier.qza
  
qiime feature-classifier classify-sklearn \
  --i-classifier classifier.qza \
  --i-reads SMA_dada2_seqs.qza \
  --o-classification SMA_taxonomy.qza
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

Download EMP dataset: qiita.ucsd.edu


