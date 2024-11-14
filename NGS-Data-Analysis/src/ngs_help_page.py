bold_start = '\033[1m'
bold_end = '\033[0m'

def help():
    """
    Prints the help page for the NGS-Analysis-Pipeline
    """
    bold_start = '\033[1m'
    bold_end = '\033[0m'

    help_page =f"""Help page for {bold_start}NGS-Analysis-Pipeline{bold_end}

{bold_start}Description:{bold_end}
The NGS-Analysis-Pipeline performs the mapping of NGS-Sequencing data, the finding genetic variants, and overall data analysis to make the data more useable and more accurate.
The program takes the forward read, reverse read, and a reference genome and creates a VCF file containing the genetic variants of the determined genom/sequence.

It is important to to input the correct filepath to the programms and to set LC_ALL= en_US.UTF-8. Otherwise the pipeline cannot run without errors.

{bold_start}Arguments and Options{bold_end}


{bold_start}run:{bold_end} runs the pipeline with the provided input arguments

    ngs_analysis.py run [{bold_start}reference genome{bold_end} filepath] [{bold_start}read1{bold_end} filepath] [{bold_start}read2{bold_end} filepath] [{bold_start}output-file{bold_end} filepath; {bold_start}optional{bold_end}]

    {bold_start}Mandatory Arguments:{bold_end}
      {bold_start}Reference Genome:{bold_end} filepath to indexed, reference genome (file-format: .fasta file)
      {bold_start}Read1:{bold_end} filepath to sequenced read1 (file-format: gzipped .fastq file)
      {bold_start}Read2:{bold_end} filepath to sequenced read2 (file-format: gzipped .fastq file)

    {bold_start}Optional Arguments:{bold_end}
      {bold_start}Output-file:{bold_end} filepath to output file (file-format: .vcf file)
        {bold_start}default:{bold_end} /PathToFolder/NGS-Data-Analysis/output/output.vcf


{bold_start}reset:{bold_end} Resets the config file

    ngs_analysis.py {bold_start}reset{bold_end}


{bold_start}-h or --help:{bold_end} Prints this help page

ngs_analysis.py {bold_start}-h{bold_end}
ngs_analysis.py {bold_start}--help{bold_end}


For more detailed info please look at the README.md"""

    print(help_page)

