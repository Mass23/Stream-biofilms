import pandas as pd
import glob

metadata = pd.read_csv('emp_qiime_mapping_release1.tsv', sep = '\t', header = 0)

directories_list = glob.glob('*')

ebi_accessions = metadata.ebi_accession.unique()

with open('missing.csv', 'w') as out:
    out.write('ebi_accession\tn_metadata\tn_sequences\tn_fna_files\tmissing\n')
    count = 0
    for accession in ebi_accessions:

        accession_data = metadata[metadata['ebi_accession'] == accession]
        n_metadata = len(accession_data)

        if accession in directories_list:
            n_sequences = len(glob.glob(accession + '/*'))
            n_fna_files = len(glob.glob(accession + '/*/*.fna'))
            fna_files_list = glob.glob(accession + '/*/*.fna')

            if n_metadata == n_sequences and n_metadata == n_fna_files:
                out.write('\t'.join([accession, str(n_metadata), str(n_sequences), str(n_fna_files), 'No', '\n']))
            else:
                out.write('\t'.join([accession, str(n_metadata), str(n_sequences), str(n_fna_files), 'Yes', '\n']))

        else:
            out.write('\t'.join([accession, str(n_metadata), 'NA', 'NA', 'Yes', '\n']))
