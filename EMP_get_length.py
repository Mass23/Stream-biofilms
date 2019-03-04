import glob
import os
from Bio import SeqIO
import pandas as pd
import matplotlib.pyplot as plt
from multiprocessing import Pool
import numpy as np
import seaborn as sns

n_cores = 3
data_inputs = glob.glob('*')
data_inputs = [i for i in data_inputs if os.path.isdir(i) == True]
print(data_inputs)

def ProcessProject(project):
    samples_list = glob.glob(project + '/*')

    with open(project + '/' + project + '_stats.tsv', 'w') as out:
        out.write('SampleID\tSequenceID\tLength\n')

        for sample in samples_list:
            sample_name = sample.split('/')[-1]

            with open(project + '/' + sample_name + '/' + sample_name + '.fq') as fastq:
                try:
                    fastq_file = SeqIO.parse(fastq, "fastq")
                    for record in fastq_file:
                        sequence_name = record.id.split(' ')[0].replace('>','')

                        out.write('\t'.join([sample_name, sequence_name, str(len(record.seq))]) + '\n')
                except:
                    print(sample_name, '\t', sequence_name, '\t' 'Warning: Differing length between quality and sequence!')

    with open(project + '/' + project + '_stats.tsv') as file:
        col_names = ['SampleID', 'SequenceID', 'Length']
        data = pd.read_csv(file, sep='\t', header=1, names = col_names, na_values = 'NA', dtype={'SampleID': str, 'SequenceID': str, 'Length': int})

        plt.figure()
        plt.hist(data['Length'])
        plt.savefig(project + '/' + project + '_Length.png')
        plt.close()

        print('Project: ', project, ' done!')

pool = Pool(n_cores)
pool.map(ProcessProject, data_inputs)
pool.close()
pool.join()

with open('full_length.tsv', 'w') as out:
    out.write('ProjectID\tSample_size\tMeanLength' + '\t'.join([str(i) for i in range(1,300)]) + '\n')
    for project in data_inputs:
        with open(project + '/' + project + '_stats.tsv') as file:
            col_names = ['SampleID', 'SequenceID', 'Length']
            data = pd.read_csv(file, sep='\t', header=1, names = col_names, na_values = 'NA', dtype={'SampleID': str, 'SequenceID': str, 'Length': int})

            current_results = []
            current_results.append(project)
            current_results.append(str(len(data)))
            current_results.append(str(data['Length'].mean()))
            for i in range(1,300):
                current_results.append(str(len(data[data['Length'] == i])))

            out.write('\t'.join(current_results) + '\n')

with open('full_length.tsv') as file:
    col_names = ['ProjectID', 'Sample_size', 'MeanLength'] + [i for i in range(1,300)]
    data = pd.read_csv(file, sep='\t', names = col_names, na_values = 'NA')
    values = data[[i for i in range(1,300)]]

    plt.figure()
    sns.heatmap(values, ytickslabels = data['ProjectID'])
    plt.savefig('heatmap.png')
    plt.close()
