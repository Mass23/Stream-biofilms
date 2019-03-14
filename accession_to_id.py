import os
import argparse
import pandas as pd
import glob

# python3 accession_to_id.py -i STUDY_ID -l PAIRED_OR_SINGLE
parser = argparse.ArgumentParser()

parser.add_argument('-i', '--id', help='ID of the dataset', type=str, action = 'store', required = True)
parser.add_argument('-l', '--Layout', help='Layout: paired / single end sequencing', type=str, action = 'store', required = True)

args = parser.parse_args()

dataset_id = args.id
layout = args.Layout

# Parse metadata
metadata_path = str('metadata/' + dataset_id + '_metadata.csv')
data = pd.read_csv(metadata_path, header = 0)
data = data.iloc[1:]
accession_list = data['ERS_accession']

# Iterate over accessions to change the name
for accession in accession_list:
    # Verify that each accession resulted in two fastq files and change the name
    accession_data = data[data['ERS_accession'] == accession]

    # Verify if the accession is unique
    if len(accession_data['#SampleID']) > 1 and len(accession_data['#SampleID']) < 1:
        print('Accession duplicate or not downloaded: ', accession)
        break
    else:
        # If unique, store the sample id
        sample_id = accession_data['#SampleID'].iloc[0]

    # Change the name
    if layout == 'paired':
        try:
            forward_read_path = str('reads/' + accession + '_1.fastq.gz')
            reverse_read_path = str('reads/' + accession + '_2.fastq.gz')

            forward_new_path = str('reads/' + sample_id + '_1.fastq.gz')
            reverse_new_path = str('reads/' + sample_id + '_2.fastq.gz')

            os.rename(forward_read_path, forward_new_path)
            os.rename(reverse_read_path, reverse_new_path)

        except:
            print(accession, ' - Warning, maybe not the right layout!')

    elif layout == 'single':
        try:
            read_path = str('reads/' + accession + '.fastq.gz')
            new_path = str('reads/' + sample_id + '.fastq.gz')

            os.rename(read_path, new_path)

        except:
            print(accession, ' - Warning, maybe not the right layout!')

    else:
        print('Layout not accepted, paired or single!')
        break
