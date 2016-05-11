### Script for quality filtering and trimming adapters
from __future__ import division


def clip_chimera_and_adapters(sequence, quality, REsite, adapter):
### Main function for simultaneously remove chimeras or sequencing errors (i.e. sequences that showed the RE site)
### and the adapter sequence. It determines if there is an ambigous RE recognition site and it will pass its agruments accordingly	
	if len(REsite) > 1:
		sequence, quality=ambigous_RE_site(sequence, quality, REsite, adapter)
	else:
		sequence, quality=single_RE_site(sequence, quality, REsite, adapter)
	if adapter in sequence:
		pos=sequence.index(adapter)
		sequence=sequence[:pos]+'\n'
		quality=quality[:p]+'\n'
	return sequence, quality

def ambigous_RE_site(sequence, quality, REsite, adapter):
### Function for simultaneously remove chimeras or sequencing errors (i.e. sequences that showed the RE site)
### Only for RE with ambigous nucleotide in RE
        RE=[i in sequence for i in REsite] ## test for RE sites
	if True in RE:
                pos=[sequence.index(i) for i in REsite] ### Index RE site
		firstpos=min(pos) ## first occurrence
                sequence=sequence[:firstpos]+'\n'
                quality=quality[:firstpos] +'\n'
        return sequence, quality

####################################################

def single_RE_site(sequence, quality, REsite, adapter):
### Function for simultaneously remove chimeras or sequencing errors (i.e. sequences that showed the RE site)
### Only for RE with non ambigous genotype
        if REsite in sequence:
                pos=sequence.index(REsite)
                sequence=sequence[:pos]+'\n'
                quality=quality[:pos] +'\n'
        return sequence, quality

############### Low quality trimming

def trim_qual(sequence, quality, minQ):
        n_qual=[ord(x)-33 for x in quality[:-1]]
        for i in range(len(n_qual)-4): ###### trim with a sliding window of 5, the 4 at the end is for avoid error
                clip=n_qual[i:i+5]
                m=float(sum(clip)/5)
                if m <= minQ:
                        quality=quality[:i]+'\n'
                        sequence=sequence[:i]+'\n'
                        break
        return sequence, quality


