"""this file will fill the database with static data necessary for filtering
"""

from src.database import hpocontroller    

def fill_hpo():
    datasets = []
    with open("data/phenotype_to_genes.txt", 'r') as vcf:
        for line in vcf:
            if line.startswith('#'):
                continue
            else:
                datasets.append(line.strip().split("\t"))
    hpocontroller.insert_hpo(datasets)
    
if __name__ == "__main__":
    fill_hpo()
