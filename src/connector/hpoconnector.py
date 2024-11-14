from src.database import hpocontroller

def get_hpo(searchterm, searchfield=None):
    if (searchfield == None):
        return None
    elif (searchfield == "symbol"):
        hpos = hpocontroller.fetch_hpo(searchterm)
    elif (searchfield == "id"):
        hpos = hpocontroller.fetch_genes(searchterm)

    keys = [
        "hpo_id",
        "hpo_name",
        "ncbi_gene_id",
        "gene_symbol",
        "disease_id"
    ]
    list_of_dicts = [dict(zip(keys, values[1:])) for values in hpos]
    return list_of_dicts


if __name__ == "__main__":
    hpo = get_hpo("dolor")
    print(hpo)
