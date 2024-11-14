from src.database import sqlcontroller

def insert_hpo(datasets):
    """Populate the HPO gene association table with the provided data set"""

    sql_list = []
    for dataset in datasets:
        sql_list.append(
            f"""
                INSERT INTO hpo_gene_associations(
                    hpo_id,
                    hpo_name,
                    ncbi_gene_id,
                    gene_symbol,
                    disease_id
                )
                VALUES(
                    '{dataset[0]}', 
                    '{dataset[1].replace("'","''")}', 
                    {dataset[2]}, 
                    '{dataset[3]}', 
                    '{dataset[4]}'
                );
            """
        )
    sqlcontroller.db_run_batch(sql_list, fetch=False)

def fetch_hpo(gene_symbol):
    # fetch all rows where gene_symbol matches
    sql = """
        select * from hpo_gene_associations where gene_symbol=%s
    """
    rows = sqlcontroller.db_run(sql, (gene_symbol,), fetch=True, multi=True)
    return rows

def fetch_genes(hpo_id: str):
    """recieves a hpo_id and fetches all gene symbols associated with the id

    Args:
        hpo_term (string): a hpo id
    """
    sql = """
        select * from hpo_gene_associations where hpo_id=%s
    """
    rows = sqlcontroller.db_run(sql, (hpo_id,), fetch=True, multi=True)
    return rows


if __name__ == "__main__":
    insert_hpo([
        ("foo", "bar", 42, "baz", 42),
        ("lorem", "ipsum", 43, "dolor", 43)
    ])
    print(fetch_hpo("baz"))
