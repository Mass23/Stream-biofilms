import glob
import os
from Bio import SeqIO
import pandas as pd
import matplotlib.pyplot as plt
from multiprocessing import Pool

n_cores = 24
data_inputs = glob.glob('*')
data_inputs = [i for i in data_inputs if os.path.isdir(i) == True]

def GetForwardPrimerIndex(seq):
    # Forward primer: GTG*CAGC*GCCGCGGTAA
    #                 1234567891111111111
    #                          0123456789
    try:
        for i in range(0, len(seq) - 19):
            if seq[i:i+3] == 'GTG' and seq[i+4:i+8] == 'CAGC' and seq[i+9:i+19]:
                return(i + 1)
            else:
                continue
    except:
        return('NA')

def GetReversePrimerIndex(seq):
    # Reverse primer: GGACTAC**GGGT*TCTAAT
    #                 12345678911111111112
    #                          01234567890
    try:
        for i in range(len(seq), 0 + 19, -1):
            if seq[i-5:i+1] == 'TCTAAT' and seq[i-10:i-6] == 'GGGT' and seq[i-19:i-12] == 'GGACTAC':
                return(i + 1)
            else:
                continue
    except:
        return('NA')

def ProcessProject(project):
    samples_list = glob.glob(project + '/*')

    with open(project + '/' + project + '_stats.tsv', 'w') as out:
        out.write('SampleID\tSequenceID\tLength\tForwardPrimerIndex\tReversePrimerIndex\n')

        for sample in samples_list:
            sample_name = sample.split('/')[-1]

            with open(project + '/' + sample_name + '/' + sample_name + '.fna') as fasta:
                for record in SeqIO.parse(fasta, "fasta"):
                    sequence_name = record.id.split(' ')[0].replace('>','')

                    if len(record.seq) > 39:

                        forward_primer_index = GetForwardPrimerIndex(record.seq)
                        reverse_primer_index = GetReversePrimerIndex(record.seq)

                        if forward_primer_index == None and reverse_primer_index == None:
                            rc_forward_primer_index = GetForwardPrimerIndex(record.seq.reverse_complement())
                            rc_reverse_primer_index = GetReversePrimerIndex(record.seq.reverse_complement())

                            if rc_forward_primer_index == None and rc_reverse_primer_index == None:
                                out.write('\t'.join([sample_name, sequence_name, str(len(record.seq)), 'NA', 'NA']) + '\n')

                            elif rc_forward_primer_index == None:
                                out.write('\t'.join([sample_name, sequence_name, str(len(record.seq)), 'NA', str(rc_reverse_primer_index)]) + '\n')

                            elif rc_reverse_primer_index == None:
                                 out.write('\t'.join([sample_name, sequence_name, str(len(record.seq)), str(rc_forward_primer_index), 'NA']) + '\n')

                            else:
                                out.write('\t'.join([sample_name, sequence_name, str(len(record.seq)), str(rc_forward_primer_index), str(rc_reverse_primer_index)]) + '\n')

                        elif rc_forward_primer_index == None:
                            out.write('\t'.join([sample_name, sequence_name, str(len(record.seq)), 'NA', str(rc_reverse_primer_index)]) + '\n')

                        elif rc_reverse_primer_index == None:
                             out.write('\t'.join([sample_name, sequence_name, str(len(record.seq)), str(rc_forward_primer_index), 'NA']) + '\n')

                        else:
                            out.write('\t'.join([sample_name, sequence_name, str(len(record.seq)), str(forward_primer_index), str(reverse_primer_index)]) + '\n')

                    else:
                        out.write('\t'.join([sample_name, sequence_name, str(len(record.seq)), 'NA', 'NA']) + '\n')

    with open(project + '/' + project + '_stats.tsv') as file:
        col_names = ['SampleID', 'SequenceID', 'Length', 'ForwardPrimerIndex', 'ReversePrimerIndex']
        data = pd.read_csv(file, sep='\t', header=1, names = col_names, na_values = 'NA', dtype={'SampleID': str, 'SequenceID': str, 'Length': int, 'ForwardPrimerIndex': int, 'ReversePrimerIndex': int})

        plt.figure()
        plt.hist(data['Length'])
        plt.savefig(project + '/' + project + '_Length.png')
        plt.close()

        plt.figure()
        plt.hist(data['ForwardPrimerIndex'])
        plt.savefig(project + '/' + project + '_ForwardPrimerIndex.png')
        plt.close()

        plt.figure()
        plt.hist(data['ReversePrimerIndex'])
        plt.savefig(project + '/' + project + '_ReversePrimerIndex.png')
        plt.close()

        print('Project: ', project, ' done!')

pool = Pool(n_cores)
pool.map(ProcessProject, data_inputs)
pool.close()
pool.join()
