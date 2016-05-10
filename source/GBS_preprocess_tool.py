#! /usr/bin/env python

### Main script for preprocessing GBS reads generated with different enzymes
### you need to specify the import in the different modules of the program

from __future__ import print_function
import argparse
#import gzip, os, argparse ### These 2 are good only for a single script
#from commands import getoutput

parser=argparse.ArgumentParser(prog='GBS_preprocess_tool', description='Program for preprocessing GBS reads')
parser.add_argument('-i', '--input-folder', dest='reads', help='The folder with your raw reads in fq.gz format')
parser.add_argument('-o', '--output-folder', dest='clean_reads', help='The output folder for the final cleaned reads')
parser.add_argument('-bc', '--barcode-file', dest='bc_file', help='The barcode file for your raw reads')
parser.add_argument('-s', '--restriction_enzyme_site', dest='REsites', help='The Restriction Enzyme (RE) recognition site. If your RE has  ambiguous nucleotide you should write all the possible sites separated by a comma (ex. For ApeKI you should use -s GCAGC,GCTGC)')
parser.add_argument('-SR', '--site-remnant', dest='RErem', help='The RE remnant site after the digestion, only the reads having the remnant site after the barcode will be kept. For RE with ambiguous nucleotide you should write all the possible remnant sites separated by a comma (as in the -s parameter)')
parser.add_argument('-l', '--min-length', dest='minlen', type=int, default=30, help='Minimum length of reads after quality trimming and adapter removal (default: 30bp)')
parser.add_argument('-q', '--min-qual', dest='minQ',type=int, default=20, help='Mean minimum quality (in a sliding window of 5bp) for trimming reads, assumed Sanger quality (Illumina 1.8+, default: 20)')
parser.add_argument('-gz', '--binary-output', dest='gz', action='store_true', default=False, help='Do you want to output the fastq file in a compressed format (i.e. gzip compressed)? This option save disk space, but writing of binary files require a considerable higher amount of time')

args=parser.parse_args()

## Check if there is some parameter missing
if 'None' in str(args):
        parser.error('Input parameter missing!! Please check your command line parameters with -h or --help')

reads=args.reads
clean_reads=args.clean_reads
bc=args.bc
REsite=args.REsites.split(',')
rem_sites=args.RErem.split(',')
minlen=args.minlen
minQ=args.minQ



#### Determine if the parameter gz is true and modify the write,append (w,a) and file suffix accordingly 
#### if the output need to be binary

if gz:
	w='wb';a='ab';suffix='fq.gz'
else:
	w='w';a='a';suffix='fq'




