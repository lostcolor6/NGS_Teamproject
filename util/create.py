from src.database import sqlcontroller

def create_tables():
    """Create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE hpo_gene_associations (
            id SERIAL PRIMARY KEY,
            hpo_id VARCHAR(255),
            hpo_name VARCHAR(255),
            ncbi_gene_id INT,
            gene_symbol VARCHAR(255),
            disease_id VARCHAR(255)
        )
        """,
        """
        CREATE TABLE patients (
            id SERIAL PRIMARY KEY,
            firstname VARCHAR(255),
            lastname VARCHAR(255),
            age INT
        )
        """,
        """
        CREATE TABLE phenotypes_associations (
            id SERIAL PRIMARY KEY,
            patientid INT,
            hpoid INT,
            FOREIGN KEY (patientid) REFERENCES patients(id),
            FOREIGN KEY (hpoid) REFERENCES hpo_gene_associations(id)
        )
        """,

        # VEP TABLE SECTION
        """
        CREATE TABLE vep (
            id SERIAL PRIMARY KEY,
            chrom VARCHAR(5),
            pos INT,
            ref VARCHAR(255),
            alt VARCHAR(255),
            most_severe_consequence VARCHAR(255)
        )
        """,
        """
        CREATE TABLE vep_transcript_consequences (
            id SERIAL PRIMARY KEY,
            vep_id INT,
            cadd_phred REAL,
            cadd_raw REAL,
            hgvsc VARCHAR(255),
            hgvsp VARCHAR(255),
            mane_plus_clinical VARCHAR(255),
            mane_select VARCHAR(255),
            transcript_id VARCHAR(255),
            gene_id VARCHAR(255),
            gene_symbol VARCHAR(255),
            gene_symbol_source VARCHAR(255),
            biotype VARCHAR(255),
            impact VARCHAR(255),
            hgnc_id VARCHAR(255),
            FOREIGN KEY (vep_id) REFERENCES vep(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE vep_colocated_variants (
            id SERIAL PRIMARY KEY,
            vep_id INT,
            clin_sig VARCHAR(255),
            clin_sig_allele VARCHAR(255),
            phenotype_or_disease INT,
            FOREIGN KEY (vep_id) REFERENCES vep(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE vep_alphamissense (
            id SERIAL PRIMARY KEY,
            transcript_consequence_id INT,
            am_pathogenicity REAL,
            am_class VARCHAR(255),
            FOREIGN KEY (transcript_consequence_id) REFERENCES vep_transcript_consequences(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE vep_spliceai (
            id SERIAL PRIMARY KEY,
            transcript_consequence_id INT,
            SYMBOL VARCHAR(255),
            DP_AG REAL,
            DS_DG REAL,
            DS_DL REAL,
            DP_DL REAL,
            DS_AG REAL,
            DP_AL REAL,
            DS_AL REAL,
            DP_DG REAL,
            FOREIGN KEY (transcript_consequence_id) REFERENCES vep_transcript_consequences(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE vep_consequence_terms (
            id SERIAL PRIMARY KEY,
            transcript_consequence_id INT,
            term VARCHAR(255),
            FOREIGN KEY (transcript_consequence_id) REFERENCES vep_transcript_consequences(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE vep_frequencies (
            id SERIAL PRIMARY KEY,
            colocated_variant_id INT,
            gnomade_amr REAL,
            gnomade_nfe REAL,
            gnomade_sas REAL,
            gnomade_afr REAL,
            gnomade_eas REAL,
            FOREIGN KEY (colocated_variant_id) REFERENCES vep_colocated_variants(id) ON DELETE CASCADE
        )
        """
    )

    for command in commands:
        sqlcontroller.db_run(command, fetch=False)

if __name__ == "__main__":
    create_tables()
