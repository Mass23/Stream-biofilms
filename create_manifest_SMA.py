with open('SMA_manifest.csv', 'w') as out:
    out.write('sample-id,absolute-filepath,direction\n')

    for i in range(1,270):
        out.write(','.join([str(i), str(i) + '_R1.fastq.gz', 'forward\n']))
        out.write(','.join([str(i), str(i) + '_R2.fastq.gz', 'reverse\n']))
