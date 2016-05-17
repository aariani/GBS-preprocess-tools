## Tool for parsing barcode files and read files

from __future__ import print_function
import gzip ## just in case the --gz param in the main file is active

def getBCInfo(bcfile,gz):
### Get barcodes infos, open files accordingly to the Genotypes available in the barcode (and the gz option)
### Return a barcode dictionary and the longer barcode (useful for further demultiplexing), and a dictionary used for demultiplexing stats
	barcode_d={}
	for line in open(bcfile):
		line=line.strip().split()
		if gz:
			barcode_d[line[0]]=line[1]+'.fq.gz'
			gzip.open(line[1]+'.fq.gz', 'wb') 
		else:
			barcode_d[line[0]]=line[1]+'.fq'
			open(line[1]+'.fq', 'w')
	l=max([len(i) for i in barcode_d.keys()])
	demInfo={k:0 for k in barcode_d.values()}
	return barcode_d, l, demInfo


def getBCindex(name,sequence,quality,barcode_d,l):
### Script for getting the barcode file index for the sequence. If not not found write the reads to the unmatched.fa.gz file.
### If find the barcode return the sequence and quality without the barcode sequence
	frag=sequence[:l] ## Extract the initial part of the sequence
	index=[i for i in barcode_d.keys() if i == frag[:len(i)]]
	if len(index)==0:
### Write non demultiplexed reads
		a=gzip.open('unmatched.fq.gz', 'ab')
		a.write(name+sequence+'+\n'+quality)
		a.close()
		return False,False,False  ## index is not defined previously, so it will be just none, without any name associated
	else:
		index=index[0]
		sequence=sequence[len(index):]
		quality=quality[len(index):]
		return index,sequence,quality


