import subprocess
import glob
import argparse

# Arguments: python3 preprocess_emp.py -p ProjectID -n 24 -t 90 -q 30 -f 10
parser = argparse.ArgumentParser()

parser.add_argument('-p', '--ProjectID', help='Reference genome fasta file used for mapping', type=str, action = 'store', required = True)
parser.add_argument('-n', '--NumberCores', help='Number of cores to use', type=int, action = 'store', required = True)
parser.add_argument('-t', '--TrimmingLength', help='Value to put for the --p-trunc-len argument of Qiime2 dada2', type=int, action = 'store', required = True)
parser.add_argument('-q', '--QualityThreshold', help='Value to put for the --p-trunc-q argument of Qiime2 dada2', type=int, action = 'store', required = True)
parser.add_argument('-f', '--FrequencyFilter', help='Value to put for the --p-min-frequency argument of Qiime2 filter-features', type=int, action = 'store', required = True)

args = parser.parse_args()

project = args.ProjectID
n_cores = args.NumberCores
trimming_length = args.TrimmingLength
quality_threshold = args.QualityThreshold
frequency_filter = args.FrequencyFilter

subprocess.call('source activate qiime2-2019.1', shell = True)

data_inputs = glob.glob(project + '/*/*.fq')
studies_list = [i.replace('.fq','') for i in data_inputs]

def ProcessFasta(file):
    study = file.split('.')[0]

    import_args = ['qiime tools import', '--type EMPSingleEndSequences', '--input-path', file, '--output-path', study + '_raw.qza']
    subprocess.call(' '.join(import_args), shell = True)

    cutadapt_args = ['qiime cutadapt trim-single', '--i-demultiplexed-sequences', study + '_raw.qza', '--p-adapter TO_FIND', '--o-trimmed-sequences', study + '_trimmed.qza']
    subprocess.call(' '.join(import_args), shell = True)

    dada2_args = ['qiime dada2 denoise-single', '--i-demultiplexed-seqs', study + '_trimmed.qza', '--p-trunc-len', trimming_length, '--p-trunc-q', quality_threshold, '--o-table', study + '_raw_table.qza', '--o-representative-sequences', study + '_raw_seqs.qza', '--o-denoising-stats', study + '_denoising_stats.qza']
    subprocess.call(' '.join(dada2_args), shell = True)

pool = Pool(n_cores)
pool.map(ProcessFasta, data_inputs)
pool.close()
pool.join()

merge_tables_args = ['qiime feature-table merge', ' '.join([str('--i-tables ' + study + '_raw_table.qza') for study in studies_list]), '--o-merged-data', project + '_table_merged.qza']
subprocess.call(' '.join(merge_tables_args), shell = True)

merge_seqs_args = ['qiime feature-table merge-seqs', ' '.join([str('--i-data ' + study + '_raw_seqs.qza') for study in studies_list]), '--o-merged-data', project + '_seqs_merged.qza']
subprocess.call(' '.join(merge_seqs_args), shell = True)

filter_args = ['qiime feature-table filter-features', '--i-table', project + '_table_merged.qza', '--p-min-frequency', frequency_filter, '--o-filtered-table', project + '_table_filtered.qza']
subprocess.call(' '.join(filter_args), shell = True)

subprocess.call('source deactivate', shell = True)
