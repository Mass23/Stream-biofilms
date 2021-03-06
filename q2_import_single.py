import subprocess
import argparse

# python3 q2_create_visualise.py -i NAME
parser = argparse.ArgumentParser()

parser.add_argument('-i', '--id', help='ID of the dataset', type=str, action = 'store', required = True)
args = parser.parse_args()
dataset_id = args.id

import_args = ['qiime', 'tools', 'import', '--type', "'SampleData[SequencesWithQuality]'", '--input-path', dataset_id + '_manifest.csv', '--output-path', dataset_id + '_raw.qza',  '--input-format', 'SingleEndFastqManifestPhred33']
subprocess.call(' '.join(import_args), shell=True)

visualise_args = ['qiime', 'demux', 'summarize', '--i-data', dataset_id + '_raw.qza', '--o-visualization', dataset_id + '_raw.qzv']
subprocess.call(' '.join(visualise_args), shell = True)
