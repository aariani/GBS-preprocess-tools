### Script for quality filtering and trimming adapters
from __future__ import division


def clip_chimera_and_adapters(sequence, quality, REsite, adapter):
### Main function for simultaneously remove chimeras or sequencing errors (i.e. sequences that showed the RE site)
### and the adapter sequence.
### It will also do a sliding window analysis for filtering the sequences
    RE=[i in sequence for i in REsite]
    if True in RE:
        pos=[sequence.find(i) for i in REsite] ### Index RE site ## use find cause index raise an error in case 1 site is ok and the other not.
        pos=[i for i in pos if i >= 0] ### In case it did not find any modification in one of the sites it will raise a -1
        firstpos=min(pos) ## first occurrence
        sequence=sequence[:firstpos]+'\n'
        quality=quality[:firstpos] +'\n'
    elif adapter in sequence:
        pos=sequence.index(adapter)
        sequence=sequence[:pos]+'\n'
        quality=quality[:pos]+'\n'
    return sequence, quality

############### Low quality trimming

def trim_qual(sequence, quality, minQ, minlen):
    n_qual=[ord(x)-33 for x in quality[:-1]]
    for i in range(len(n_qual)-4): ###### trim with a sliding window of 5, the 4 at the end is for avoid error
        clip=n_qual[i:i+5]
        m=float(sum(clip)/5)
        if m <= minQ:
            quality=quality[:i]+'\n'
            sequence=sequence[:i]+'\n'
            break
    if len(sequence.strip()) >=minlen:
        return sequence,quality
    else:
        return False,False

###################
def check_overhang(sequence, quality, rem_sites, rmRErem):
#### script for checking the overhang sequences
    overhangLength=len(rem_sites[0])
    if sequence[:overhangLength] in rem_sites:
        if rmRErem:
            sequence=sequence[overhangLength:]
            quality=quality[overhangLength:]
        return sequence, quality
    else:
        return False,False
