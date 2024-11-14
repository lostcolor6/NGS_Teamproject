# NGS-ANALYSIS-PIPELINE

## Table of Contents

- [Description](#description)
- [Programs Used/Needed](#programs-usedneeded)
- [Preparation and Setup](#preparation-and-setup)
  - [Example of a correct config file](#example-of-a-correct-config-file)
- [Usage](#usage)
  - [run](#run)
  - [reset](#reset)
  - [--help or -h](#--help-or--h)
- [Further citation of the used programs](#further-citation-of-the-used-programs)

## Description
The NGS-Analysis-Pipeline performs the mapping of NGS-Sequencing data, the finding genetic variants, and overall data analysis to make the data more useable and more accurate.
The program takes the forward read, reverse read, and a reference genome and creates a VCF file containing the genetic variants of the determined genom/sequence.


## Programs Used/Needed

* [SeqPurge](https://github.com/imgag/ngs-bits/blob/master/README.md) -
* [BWA](https://github.com/lh3/bwa) -
* [samtools](https://github.com/samtools/samtools) -
* [samblaster](https://github.com/GregoryFaust/samblaster) -
* [ABRA2](https://github.com/mozack/abra2) -
* [freebayes](https://github.com/freebayes/freebayes) -
* [vcfallelicprimitives](https://github.com/vcflib/vcflib/blob/master/doc/vcfallelicprimitives.md) -
* [VcfBreakMulti](https://github.com/imgag/ngs-bits/blob/master/doc/tools/VcfBreakMulti.md) -
* [VcfLeftNormalize](https://github.com/imgag/ngs-bits/blob/master/doc/tools/VcfLeftNormalize.md) -

These programs are necessary and need to be installed for the NGS-Pipeline to work.

## Preparation and Setup
After installing the programs listed above you need to add the file paths to the programs to the `ngs_analysis_config.txt` file.
You can either add the full path or if the installed program lies in `$PATH` you can just input the name that would call in the program in the console.
If you want to reset the config file. Please click [here](#reset)

**Important:**
Before you can use the programm, you must use `bwa` to index your reference genome.
To do that you use the following command with the path to your reference genome for `ref.fa`

```console
user@machine:~$ bwa index ref.fa
```
For further information on how to index a reference genome, please visit the [bwa Github page](https://github.com/lh3/bwa)


### Example of a correct config file
```
SeqPurge_Path=/user/home/dict/ngs-bits/bin/SeqPurge
>
BWA_Path=/user/home/dict/bwa-0.7.18/bwa
>
samblaster_Path=/user/home/dict/samblaster-v.0.1.26/samblaster
>
samtools_Path=samtools
>
ABRA2_Path=/user/home/dict/abra2-2.23.jar
>
freebayes_Path=/user/home/dict/freebayes-1.3.6-linux-amd64-static
>
vcfallelicprimitives_Path=vcfallelicprimitives
>
VcfBreakMulti_Path=/user/home/dict/ngs-bits/bin/VcfBreakMulti
>
VcfLeftNormalize_Path=/user/home/dict/ngs-bits/bin/VcfLeftNormalize
>
```
In the example the programs `samtools` and `vcfallelicprimitives` lie in the $PATH, therefore just the name is sufficient.

## Usage

The program has 3 commands that can be called:

    * run: used for running the NGS-Analysis-Pipeline for NGS-Data

    * reset: resets the config file

    * --help or -h: prints help page

### run
**Important:** Due to ABRA2 `LC_ALL` must be set to `en_US.UTF-8`.
               You can use `~ export LC_ALL=en_US.UTF-8`.

```console
user@machine:~$ python ngs_analysis.py run [arguments]
```
#### Arguments and Options

```
ngs_analysis.py run [reference genome filepath] [read1 filepath] [read2 filepath] [output-file filepath; optional]

    Mandatory Arguments:
      Reference Genome: filepath to indexed, reference genome (file-format: .fasta file)
      Read1: filepath to sequenced read1 (file-format: gzipped .fastq file)
      Read2: filepath to sequenced read2 (file-format: gzipped .fastq file)

    Optional Arguments:
      Output-file: filepath to output file (file-format: .vcf file)
        default: /PathToFolder/NGS-Data-Analysis/output/output.vcf

```
#### Example run command
```console
user@machine:~$ python ngs_analysis.py run /path-0/ref.fa /path-1/read1.fastq.gz /path-2/read2.fastq.gz /path-3/variants.vcf

user@machine:~$ python ngs_analysis.py run /path-0/ref.fa /path-1/read1.fastq.gz /path-2/read2.fastq.gz
```
The first command will save the output data in: `/path-3/variants.vcf`

The second command will save the output data in: `/PathToFolder/NGS-Data-Analysis/output/output.vcf`



### reset

If the config-file is not present or has been altered and needs to be reset you can use:

```console
user@machine:~$ python ngs_analysis.py reset
```

This will reset the file to:
```
SeqPurge_Path=
>
BWA_Path=
>
samblaster_Path=
>
samtools_Path=
>
ABRA2_Path=
>
freebayes_Path=
>
vcfallelicprimitives_Path=
>
VcfBreakMulti_Path=
>
VcfLeftNormalize_Path=
>
```

### --help or -h

This prints a help text to the console, providing information about the commands and arguments.
```console
user@machine:~$ python ngs_analysis.py -h
user@machine:~$ python ngs_analysis.py --help

```

## Further citation of the used programs
* **SeqPurge, VcfBreakMulti, VcfLeftNormalize:**

  [ngs-bits](https://github.com/imgag/ngs-bits)
* **BWA:**

  [Citation 1](https://pubmed.ncbi.nlm.nih.gov/19451168/)

  [Citation 2](https://pubmed.ncbi.nlm.nih.gov/20080505/)

  [Citation 3](http://arxiv.org/abs/1303.3997)

* [samtools](https://academic.oup.com/gigascience/article/10/2/giab008/6137722?login=true)
* [samblaster](https://academic.oup.com/gigascience/article/10/2/giab008/6137722?login=true)
* [ABRA2](https://academic.oup.com/bioinformatics/article/35/17/2966/5289536?login=true)
* [freebayes](http://arxiv.org/abs/1207.3907)
* **vcfallelicprimitives:**

  [vcflib](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1009123)
