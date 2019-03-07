import glob
import os
cwd = os.getcwd()

with open('SMA_manifest.csv', 'w') as out:

    files_list = glob.glob('reads/*.fq.gz')
    id_set = set()
    for file in files_list:
        name = file.split('/')[-1].replace('_forward_paired.fq.gz','').replace('_reverse_paired.fq.gz','')
        id_set.add(name)

    id_list = list(id_set)

    out.write('sample-id,absolute-filepath,direction\n')

    for i in id_list:
        out.write(','.join([str(i), cwd + '/reads/' + str(i) + '_forward_paired.fq.gz', 'forward\n']))
out.write(','.join([str(i), cwd + '/reads/' + str(i) + '_reverse_paired.fq.gz', 'reverse\n']))
