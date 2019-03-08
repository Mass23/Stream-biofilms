import glob
import os
import argparse

# python3 create_manifest.py -i NAME
parser = argparse.ArgumentParser()

parser.add_argument('-i', '--id', help='ID of the dataset', type=str, action = 'store', required = True)
args = parser.parse_args()
dataset_id = args.id 

cwd = os.getcwd()

with open(dataset_id + '_manifest.csv', 'w') as out:

    files_list = glob.glob('reads/*.fastq.gz')
    id_set = set()
    for file in files_list:
        name = file.split('/')[-1].replace('_R1.fastq.gz','').replace('_R2.fastq.gz','')
        id_set.add(name)

    id_list = list(id_set)

    out.write('sample-id,absolute-filepath,direction\n')

    for i in id_list:
        out.write(','.join([str(i), cwd + '/reads/' + str(i) + '_R1.fastq.gz', 'forward\n']))
        out.write(','.join([str(i), cwd + '/reads/' + str(i) + '_R2.fastq.gz', 'reverse\n']))
