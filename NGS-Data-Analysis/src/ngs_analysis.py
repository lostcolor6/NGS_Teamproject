import subprocess
import os
import sys

import config_setup
import ngs_help_page

def is_en_US_UTF_8():
    """
    Checks if the LC_ALL environment variable is set to en_US.UTF-8
    :return: true if LC_ALL is set to en_US.UTF-8, false if not
    """
    LC_ALL = os.environ.get('LC_ALL')
    return LC_ALL == 'en_US.UTF-8'


def run_command(command):
    """
    Executes a command in the shell and prints the output or in case of an error the error message.
    :param command: String with the command that is to be executed.
    """
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable='/bin/bash')
        print(f"Command executed successfully.")
        print("Output:", result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.cmd}")
        print("Exit code:", e.returncode)
        print("Error message:", e.stderr.decode())

def command_list(paths_dict, ref_path, read1_path, read2_path, outputpath):
    """
    Creates a list of command that contains the individual commands of the NGS analysis pipeline.
    :param paths_dict: file paths to the programs used in the pipeline
    :param ref_path: filepath to the reference genome
    :param read1_path: filepath to the first read
    :param read2_path: filepath to the second read
    :param outputpath: filepath to the output file
    :return: returns the list of commands
    """
    command_list = []
    command_list.append(f"{paths_dict['SeqPurge_Path']} -in1 {read1_path} -in2 {read2_path} -out1 ../analysis_storage/read1_SeqPurge.fastq.gz -out2 ../analysis_storage/read2_SeqPurge.fastq.gz")
    command_list.append(f"{paths_dict['BWA_Path']} mem -t 4 {ref_path} ../analysis_storage/read1_SeqPurge.fastq.gz ../analysis_storage/read2_SeqPurge.fastq.gz | gzip -3 > ../analysis_storage/bwa_mapped_ngs.sam.gz")
    command_list.append(f"{paths_dict['samtools_Path']} sort -n -o ../analysis_storage/bwa_mapped_id_sorted.sam ../analysis_storage/bwa_mapped_ngs.sam.gz")
    command_list.append(f"{paths_dict['samblaster_Path']} --removeDups -i ../analysis_storage/bwa_mapped_id_sorted.sam -o ../analysis_storage/samblaster_output.sam.gz")
    command_list.append(f"{paths_dict['samtools_Path']} sort -o ../analysis_storage/samtools_resorted.sam.gz ../analysis_storage/samblaster_output.sam.gz")
    command_list.append(f"{paths_dict['samtools_Path']} view -b -o ../analysis_storage/samtools_output.bam ../analysis_storage/samtools_resorted.sam.gz")
    command_list.append(f"{paths_dict['samtools_Path']} index ../analysis_storage/samtools_output.bam")
    command_list.append(f"java -Xmx16G -jar {paths_dict['ABRA2_Path']} --in ../analysis_storage/samtools_output.bam --out ../analysis_storage/abra2_output.bam  --ref {ref_path}")
    command_list.append(f"{paths_dict['freebayes_Path']} -q 20 -f {ref_path} ../analysis_storage/abra2_output.bam > ../analysis_storage/freebayes_output.vcf")
    command_list.append(f"{paths_dict['vcfallelicprimitives_Path']} ../analysis_storage/freebayes_output.vcf > ../analysis_storage/allelicprimitives_output.vcf")
    command_list.append(f"{paths_dict['VcfBreakMulti_Path']} -in ../analysis_storage/allelicprimitives_output.vcf -out ../analysis_storage/breakmulti_output.vcf ")
    command_list.append(f"{paths_dict['VcfLeftNormalize_Path']} -in ../analysis_storage/breakmulti_output.vcf -out {outputpath} -ref {ref_path}")

    return command_list


def run_analysis(file_paths):
    """
    Runs the analysis pipeline with the command line parameters.
    if the paths are not valid or do nott exist, the function will return.
    if there is no output path provided, the output will be saved in ../output/output.vcf
    """
    if not is_en_US_UTF_8():
        print("Error: LC_ALL is not set to en_US.UTF-8.\n")
        print("Due to ABRA2 the locale must be set to en_US.UTF-8. The pipeline cannot run without this setting.")
        print("You can use the following command to set the locale: export LC_ALL=en_US.UTF-8")
        return
    if len(sys.argv) < 5:
        print("Error: Insufficient amount of arguments.\n")
        print("Please provide the paths to the reference genome, read1, and read2. The path to the output file is optional.")
        return
    if not config_setup.are_paths_valid(file_paths):
        print("Error: Paths in the config file are invalid.\n")
        print("Please check the paths in the config file.")
        return
    for x in sys.argv[2:5]:
        if not os.path.isfile(x):
            print("Error: File does not exist.\n")
            print(f"File {x} does not exist. Please provide a valid file path.")
            return
    paths_dict = config_setup.get_Paths()
    ref_path = sys.argv[2]
    read1_path = sys.argv[3]
    read2_path = sys.argv[4]
    outputpath = ""
    if len(sys.argv) < 6:
        outputpath = "../output/output.vcf"
    elif sys.argv[5][-4:0] == ".vcf":
        output_path = sys.argv[5]
    else:
        print("Error: Invalid output path.\n")
        print("Please provide a valid output path. Should end in .vcf")
        return
    print("Running analysis:")
    commands = command_list(paths_dict, ref_path, read1_path, read2_path, outputpath)
    counter = 1

    for command in commands:
        print("Running command:", command, "\nProgramm:", counter, "of", len(commands))
        run_command(command)
        counter+=1

    print("Analysis finished sucessfully. Output can be found in", outputpath)



def main():
    """
    Main function that is called when the program is executed.
    calls the programm corresponding to the first argument provided.
    """
    file_paths = config_setup.get_Paths()

    if len(sys.argv) == 1:
        print("Please provide an argument. You can use --help or -h to look at accetable commands.")
    else:
        match sys.argv[1]:
            case "reset":
                config_setup.reset_config()
            case "run":
                run_analysis(file_paths)
            case "--help" | "-h":
                print("\n")
                ngs_help_page.help()
            case _:
                print("Error: Invalid argument.\n")
                print("Invalid argument: You can call you can use --help to look at accetable commands.")



if __name__ == "__main__":
    main()
