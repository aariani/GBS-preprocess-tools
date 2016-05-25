#! /usr/bin/env python

### Main script for preprocessing GBS reads generated with different enzymes
### you need to specify the import in the different modules of the program

from __future__ import print_function
import gzip
import os
import argparse
import BCtool
import process_read
from commands import getoutput

parser=argparse.ArgumentParser(prog='GBSprep', description='Program for preprocessing GBS reads')
parser.add_argument('-i', '--input-folder', dest='reads', help='The folder with your raw reads in gz compressed format (REQUIRED)')
parser.add_argument('-o', '--output-folder', dest='clean_reads', help='The output folder for the final cleaned and demultiplexed reads (REQUIRED)')
parser.add_argument('-bc', '--barcode-file', dest='bc_file', help='The barcode file for your raw reads (REQUIRED)')
parser.add_argument('-s', '--restriction_enzyme_site', dest='REsites', help='The Restriction Enzyme (RE) recognition site (REQUIRED). If your RE has ambiguous nucleotide you should write all the possible sites separated by a comma (ex. For ApeKI you should use -s GCAGC,GCTGC)')
parser.add_argument('-SR', '--site-remnant', dest='RErem', help='The RE remnant site after the digestion (REQUIRED). Only reads with the remnant site after the barcode will be kept. For RE with ambiguous nucleotide you should write all the possible remnant sites separated by a comma (as in the -s parameter)')
parser.add_argument('-l', '--min-length', dest='minlen', type=int, default=30, help='Minimum length of reads after quality trimming and adapter/chimeras clipping (default: 30bp)')
parser.add_argument('-q', '--min-qual', dest='minQ',type=int, default=20, help='Mean minimum quality (in a sliding window of 5bp) for trimming reads, assumed Sanger quality (Illumina 1.8+, default: 20)')
parser.add_argument('-gz', '--binary-output', dest='gz', action='store_true', default=False, help='Do you want to output the fastq file in a compressed format (i.e. gz compressed)? This option save disk space, but writing binary files requires a considerable higher amount of time (Default: False)')
parser.add_argument('-ad', '--adapter-contaminants', dest='contaminant', default='AGATCGG', help='The initial sequence of the adapter contaminant (default: AGATCGG)')
parser.add_argument('--remove-remnant-site', dest='rmRErem', action='store_true', default=False, help='Do you want to remove the RE remnant site from the final cleaned reads? (default: False)')

args=parser.parse_args()

## Check if there is some parameter missing
if 'None' in str(args):
	parser.error('Input parameter missing!! Please check your command line parameters with -h or --help')

## Assigning paramters to variables
reads=args.reads.split('/')[0]
clean_reads=args.clean_reads
bc=args.bc_file
REsite=args.REsites.split(',')  ## This will be a list
rem_site=args.RErem.split(',') ## And this too. Remember for the final filtering
minlen=args.minlen
minQ=args.minQ
gz=args.gz
contaminant=args.contaminant
rmRErem=args.rmRErem

### Get barcode info and open all the file
barcode_d,l,demInfo=BCtool.getBCInfo(bc, gz)

### Start preprocess the files
all_reads=getoutput('ls %s/*.gz' % reads).split()
for i in all_reads:
	print('Start preprocessing %s file' % i)
	read_f=gzip.open(i, 'rb')
	while True:
		name=read_f.readline()
		if name=='': break  ## stop parsing the file at the end
		sequence=read_f.readline()
		plus=read_f.readline()
		quality=read_f.readline()
		if '1:Y:0' not in name:  ## keep only reads passing initial Illumina filtering
			index,sequence,quality=BCtool.getBCindex(name,sequence,quality,barcode_d,l)			
			if index:
				sequence, quality= process_read.process(sequence, quality, REsite, contaminant, minQ, minlen, rem_site, rmRErem)
				if sequence:
					if gz:
						a=gzip.open(barcode_d[index], 'ab')
						a.write(name+sequence+plus+quality)
						a.close()
					else:
						a=open(barcode_d[index], 'a')
						a.write(name+sequence+plus+quality)
						a.close()
					demInfo[barcode_d[index]]+=1
	read_f.close()

os.system('mkdir %s' % clean_reads)
os.system('mv *fq* %s' % clean_reads)

print('Sample\tTotalReads', file=open('Demultiplexing_stats.txt', 'a'))
for i in demInfo.keys():
	print(i.split('.')[0], demInfo[i], sep='\t', file=open('Demultiplexing_stats.txt', 'a'))
