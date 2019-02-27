import pandas as pd

metadata = pd.read_csv('emp_qiime_mapping_release1.tsv', sep = '\t', header = 0)

metadata = metadata[(metadata['ebi_accession'] != 'ERP020884') & (metadata['ebi_accession'] != 'ERP006348') & (metadata['ebi_accession'] != 'ERP016384')]

type_list = list()
type_list.append('#q2:types')
for column in metadata:
    if column == '#SampleID':
        continue
    else:
        if type(metadata[column][2]) is str:
            type_list.append('categorical')
        else:
            type_list.append('numeric')

# https://stackoverflow.com/questions/43408621/add-a-row-at-top-in-pandas-dataframe
metadata.loc[-1] = type_list
metadata.index = metadata.index + 1
metadata = metadata.sort_index()

metadata.to_csv('filtered_emp_qiime_mapping.tsv', sep='\t', index = False)
