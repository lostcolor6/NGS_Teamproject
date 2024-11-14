from typing import List, Tuple

def parseVCFfile(filepath: str, delimiter: str, mode='dict') -> dict:
    """parse a vcf file"""
    header, data = openVCFfile(filepath)

    #extract column names from the last header line
    col_line = header[-1].strip().lstrip('#')
    cols = col_line.split(delimiter)

    if mode=='dict':
        ret = {"header": header, "data" : {}}
        for i, line in enumerate(data):
            ret["data"][str(i)] = parseVCFline(line, delimiter, cols)
    else:
        ret = {"header": header, "data" : []}
        for i, line in enumerate(data):
            ret["data"].append(parseVCFline(line, delimiter, cols))

    return ret


def parseVCFline(line: str, delimiter: str, cols: List[str]) -> dict:
    """parse a single vcf data line and return a dictionary"""
    ret = {}
    cells = line.strip().split(delimiter)

    if len(cells) != len(cols):
        raise ValueError("Number of columns in data does not match header")

    for i in range(len(cols)):
        ret[cols[i]] = cells[i]

    return ret
    

def openVCFfile(filepath: str) -> Tuple[List, List]:
    """opens a vcf file and returns the header lines and the data lines as two lists

    Args:
        filepath (str): path to vcf file

    Returns:
        Tuple[List, List]: header lines (starting with '#') and data lines
    """
    ret = ([], [])
    with open(filepath, 'r') as vcf:
        for line in vcf:
            if line.startswith('#'):
                ret[0].append(line)
            else:
                ret[1].append(line)
    return ret

if __name__ == "__main__":
    import os
    # print(os.getcwd())

    vcfData = parseVCFfile("data/NA12878_73_var.vcf", "\t")
    print(vcfData["data"]["0"]["CHROM"] == "chr1")
    print(vcfData["data"]["0"])