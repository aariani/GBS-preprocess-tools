## Tool for parsing barcode files and read files
from __future__ import print_function
import gzip ## just in case the --gz param in the main file is active

def getBcInfo(bcfile, suffix, gz):
### Get barcodes infos, open files accordingly to the Genotypes available in the barcode (and the gz option)
### Return a barcode dictionary and the longer barcode (useful for further demultiplexing), and a dictionary used for demultiplexing stats
	barcode_d={}
	for line in open(bcfile):
		line=line.strip().split()
		barcode_d[line[0]]=line[1]+'.'+suffix
		gzip.open(line[1]+'.gz', 'wb') ### this is bad because I cannot decide in the first file if it is gz or not!! Probably I should just then use different pipelines (redundant??)

l=max([len(i) for i in barcode_d.keys()])
sample={k:0 for k in barcode_d.values()}

