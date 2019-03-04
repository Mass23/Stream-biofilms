import glob

with open('SMA_manifest.csv', 'w') as out:

    files_list = glob.glob('reads/*.fastq.gz')
    id_set = set()
    for file in files_list:
        name = file.split('/')[-1].replace('_R1.fastq.gz','').replace('_R2.fastq.gz','')
        id_set.add(name)

    id_list = list(id_set)

    out.write('sample-id,absolute-filepath,direction\n')

    for i in id_list:
        out.write(','.join([str(i), 'path/to/reads/' + str(i) + '_R1.fastq.gz', 'forward\n']))
        out.write(','.join([str(i), 'path/to/reads/' + str(i) + '_R2.fastq.gz', 'reverse\n']))
