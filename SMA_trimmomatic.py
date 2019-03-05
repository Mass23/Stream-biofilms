import glob
import subprocess
import argparse
from multiprocessing import Pool
from Bio import SeqIO
from gzip import open as gzopen

parser = argparse.ArgumentParser()

# E.g. python3 SMA_trimmomatic.py -n 6 -l 3 -t 3 -q 20 -m 244
parser.add_argument('-n', '--NumberCores', help='Number of cores to use.', type=int, action = 'store', required = True)
parser.add_argument('-l', '--LeadingQ', help='Quality threshold to trim nucleotides from the beginning of the read.', type=int, action = 'store', required = True)
parser.add_argument('-t', '--TrailingQ', help='Quality threshold to trim nucleotides from the end of the read.', type=int, action = 'store', required = True)
parser.add_argument('-q', '--SWqual', help='Minimal quality for 4-mers to be kept.', type=int, action = 'store', required = True)
parser.add_argument('-m', '--MinLength', help='Minimal length for a read to be kept.', type=int, action = 'store', required = True)

args = parser.parse_args()

n_cores = str(args.NumberCores)
leading_q = str(args.LeadingQ)
trailing_q = str(args.TrailingQ)
qual_sw = str(args.SWqual)
min_len = str(args.MinLength)

files_list = glob.glob('*.fastq.gz')
id_set = set()
for file in files_list:
    name = file.replace('_R1.fastq.gz','').replace('_R2.fastq.gz','')
    id_set.add(name)

id_list = list(id_set)
print('To process: ', id_list)

with open('trimmomatic_stats.tsv', 'w') as out:
    out.write('SampleID\tBeforeLength\tAfterLength\tPercentageOfRemoved\n')

    for name in id_list:
        print('Sample: ', name)

        data_before = SeqIO.parse(gzopen(name + "_R1.fastq.gz", "rt"), 'fastq')
        before_length = 0
        for i in data_before:
            before_length += 1

        trimo_args = ["trimmomatic", "PE", "-threads",  n_cores, "-phred33",
                    # Input R1, R2
                    name + "_R1.fastq.gz" , name + "_R2.fastq.gz",
                    # Output forward/reverse, paired/unpaired
                    name + "_forward_paired.fq.gz",
                    name + "_forward_unpaired.fq.gz",
                    name + "_reverse_paired.fq.gz",
                    name + "_reverse_unpaired.fq.gz",
                    "ILLUMINACLIP:TruSeq3-PE.fa:2:30:10",
                    "LEADING:" + leading_q,
                    "TRAILING:" + trailing_q,
                    "SLIDINGWINDOW:4:" + qual_sw,
                    "MINLEN:" + min_len]

        subprocess.call(' '.join(trimo_args), shell = True)

        data_after = SeqIO.parse(gzopen(name + "_forward_paired.fq.gz", "rt"), 'fastq')
        after_length = 0
        for i in data_after:
            after_length += 1

        try:
            removed_proportion = (after_length - before_length) / before_length
        except:
            removed_proportion = 'NA'

        out.write(name + '\t' + str(before_length) + '\t' + str(after_length) + '\t' + str(removed_proportion) + '\n')
        print(name + ' done!')
