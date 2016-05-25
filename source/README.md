# This folder contains the source files of the GBSprep program

This files could be used for creating a binary code from the `GBSprep_main.py` for your computer.

In this folder there are all the modules of the GBSprep program in the main folder.

The different part of the code has been divided during development for clarity (especially my own!!).

The GBSprep.py file were created by concatenating the files in this folder (with minor modifications).

File list in this folder:

* `GBSprep_main.py` is the main script that parses the command line parameters and call all the other modules in this folder;

* `BCtool.py` contains functions for parsing barcodes and genotypes and for demultiplexing reads;

* `trimQC.py' contains functions for quality controls of the reads. These function include a clipping of adapter/chimeras, sliding window quality trimming and checking the presence of RE site remnants after the barcode;

* `process_read.py` is mainly an interface for calling functions inside the `trimQC.py` file;




