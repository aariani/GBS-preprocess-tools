### script for processing single reads
### this script will do all the processing of the reads and will return the sequence and quality if they satisfy all the parameters
### 1) Trim chimeras: return trimmed reads
### 2) Quality filtering: return quality trimmed read if longer than minlen
### 3) Check overhang
### import accessory modules
import trimQC

def process(sequence, quality, REsite, contaminant, minQ, minlen, rem_site, rmRErem):
	sequence, quality=trimQC.clip_chimera_and_adapters(sequence, quality, REsite, contaminant)
	sequence, quality=trimQC.trim_qual(sequence,quality,minQ,minlen)
	if sequence: ## check quality filtering
		sequence, quality=trimQC.check_overhang(sequence, quality, rem_site, rmRErem)
		## Check overhang site
		if sequence:
			return sequence, quality
		else:
			return False,False
	else:
		return False,False
