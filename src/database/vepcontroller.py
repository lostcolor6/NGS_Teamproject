from src.database import sqlcontroller

def insert_vep(vep, chrom, pos, ref, alt):
    """
    Inserts a new VEP (Variant Effect Predictor) record into the database.
    Returns:
        int: The ID of the newly inserted VEP record.
    """
    vep = vep["entry_0"]
    transcript_consequences = vep["transcript_consequences"]
    colocated_variants = vep["colocated_variants"]
    most_severe_consequence = vep.get("most_severe_consequence")

    sql = """
        INSERT INTO vep (
            chrom,
            pos,
            ref,
            alt,
            most_severe_consequence
        ) 
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s
        )
        RETURNING id;
    """
    data = (chrom, pos, ref, alt, most_severe_consequence if most_severe_consequence else None)
    vep_id = sqlcontroller.db_run(sql, data=data, fetch=False, returning=True)
    insert_transcript_consequences(transcript_consequences, vep_id)
    insert_colocated_variants(colocated_variants, vep_id)
    return vep_id
    vep_id = sqlcontroller.db_run(sql, fetch=False, returning=True)
    insert_transcript_consequences(transcript_consequences, vep_id)
    insert_colocated_variants(colocated_variants, vep_id)
    return vep_id

def insert_transcript_consequences(transcript_consequences, vep_id):
    for transcript_consequence in transcript_consequences:
        cadd_phred = transcript_consequence.get("cadd_phred")
        cadd_raw = transcript_consequence.get("cadd_raw")
        hgvsc = transcript_consequence.get("hgvsc")
        hgvsp = transcript_consequence.get("hgvsp")
        mane_plus_clinical = transcript_consequence.get("mane_plus_clinical")
        mane_select = transcript_consequence.get("mane_select")
        transcript_id = transcript_consequence.get("transcript_id")
        gene_id = transcript_consequence.get("gene_id")
        gene_symbol = transcript_consequence.get("gene_symbol")
        gene_symbol_source = transcript_consequence.get("gene_symbol_source")
        biotype = transcript_consequence.get("biotype")
        impact = transcript_consequence.get("impact")
        hgnc_id = transcript_consequence.get("hgnc_id")

        sql = """
            INSERT INTO vep_transcript_consequences(
                vep_id,
                cadd_phred,
                cadd_raw,
                hgvsc,
                hgvsp,
                mane_plus_clinical,
                mane_select,
                transcript_id,
                gene_id,
                gene_symbol,
                gene_symbol_source,
                biotype,
                impact,
                hgnc_id
            )
            VALUES(
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            RETURNING id
        """
        
        data = (
            vep_id,
            cadd_phred,
            cadd_raw,
            hgvsc,
            hgvsp,
            mane_plus_clinical,
            mane_select,
            transcript_id,
            gene_id,
            gene_symbol,
            gene_symbol_source,
            biotype,
            impact,
            hgnc_id
        )

        transcript_consequence_id = sqlcontroller.db_run(sql, data=data, fetch=False, returning=True)
        
        consequence_terms = transcript_consequence.get("consequence_terms", None)
        spliceai = transcript_consequence.get("spliceai", None)
        alphamissense = transcript_consequence.get("alphamissense", None)
        
        if consequence_terms:
            insert_consequence_terms(consequence_terms, transcript_consequence_id)
        if spliceai:
            insert_spliceai(spliceai, transcript_consequence_id)
        if alphamissense:
            insert_alphamissense(alphamissense, transcript_consequence_id)
        
        return transcript_consequence_id

def insert_consequence_terms(consequence_terms, transcript_consequence_id):
    for consequence_term in consequence_terms:
        term = consequence_term if consequence_term else None

        sql = """
            INSERT INTO vep_consequence_terms (
                transcript_consequence_id,
                term
            )
            VALUES (
                %s,
                %s
            )
        """
        data = (transcript_consequence_id, term)
        sqlcontroller.db_run(sql, data=data, fetch=False)

def insert_spliceai(spliceai, transcript_consequence_id):
    symbol = spliceai.get("SYMBOL")
    dp_ag = spliceai.get("DP_AG")
    ds_dg = spliceai.get("DS_DG")
    ds_dl = spliceai.get("DS_DL")
    dp_dl = spliceai.get("DP_DL")
    ds_ag = spliceai.get("DS_AG")
    dp_al = spliceai.get("DP_AL")
    ds_al = spliceai.get("DS_AL")
    dp_dg = spliceai.get("DP_DG")

    sql = """
        INSERT INTO vep_spliceai (
            transcript_consequence_id,
            SYMBOL,
            DP_AG,
            DS_DG,
            DS_DL,
            DP_DL,
            DS_AG,
            DP_AL,
            DS_AL,
            DP_DG
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """
    data = (
        transcript_consequence_id,
        symbol,
        dp_ag,
        ds_dg,
        ds_dl,
        dp_dl,
        ds_ag,
        dp_al,
        ds_al,
        dp_dg
    )
    sqlcontroller.db_run(sql, data=data, fetch=False)

def insert_alphamissense(alphamissense, transcript_consequence_id):
    am_pathogenicity = alphamissense.get("am_pathogenicity")
    am_class = alphamissense.get("am_class")

    sql = """
        INSERT INTO vep_alphamissense (
            transcript_consequence_id,
            am_pathogenicity,
            am_class
        )
        VALUES (
            %s, %s, %s
        )
    """
    data = (
        transcript_consequence_id,
        am_pathogenicity,
        am_class
    )
    sqlcontroller.db_run(sql, data=data, fetch=False)

def insert_colocated_variants(colocated_variants, vep_id):
    for colocated_variant in colocated_variants:
        clin_sig = colocated_variant.get("clin_sig")
        clin_sig_allele = colocated_variant.get("clin_sig_allele")
        phenotype_or_disease = colocated_variant.get("phenotype_or_disease")

        sql = """
            INSERT INTO vep_colocated_variants (
                vep_id,
                clin_sig,
                clin_sig_allele,
                phenotype_or_disease
            )
            VALUES (
                %s, %s, %s, %s
            )
            RETURNING id
        """
        data = (
            vep_id,
            clin_sig,
            clin_sig_allele,
            phenotype_or_disease
        )
        colocated_variant_id = sqlcontroller.db_run(sql, data=data, fetch=False, returning=True)
        frequencies = colocated_variant.get("frequencies", [])
        insert_frequencies(frequencies, colocated_variant_id)
        return colocated_variant_id

def insert_frequencies(frequencies, colocated_variant_id):
    gnomade_amr = frequencies.get("gnomade_amr")
    gnomade_nfe = frequencies.get("gnomade_nfe")
    gnomade_sas = frequencies.get("gnomade_sas")
    gnomade_afr = frequencies.get("gnomade_afr")
    gnomade_eas = frequencies.get("gnomade_eas")

    sql = """
        INSERT INTO vep_frequencies (
            colocated_variant_id,
            gnomade_amr,
            gnomade_nfe,
            gnomade_sas,
            gnomade_afr,
            gnomade_eas
        )
        VALUES (
            %s, %s, %s, %s, %s, %s
        )
    """
    data = (
        colocated_variant_id,
        gnomade_amr,
        gnomade_nfe,
        gnomade_sas,
        gnomade_afr,
        gnomade_eas
    )
    sqlcontroller.db_run(sql, data=data, fetch=False)

def get_vep(chrom, pos, ref, alt):
    """
    Retrieves VEP (Variant Effect Predictor) data from the database based on provided identifiers.
    Returns:
        list: A list of dictionaries containing VEP data.
    """
    sql = f"""
        SELECT id, chrom, pos, ref, alt, most_severe_consequence
        FROM vep
        WHERE (chrom='{chrom}' AND pos={pos} AND ref='{ref}' AND alt='{alt}')
    """
    veps = sqlcontroller.db_run(sql, multi=True)
    if veps: 
        keys = [
            "id",
            "chrom",
            "pos",
            "ref",
            "alt",
            "most_severe_consequence"
        ]
        veps = [dict(zip(keys, values)) for values in veps]

        for vep in veps:
            vep_id = vep.pop("id")
            vep["transcript_consequences"] = get_transcript_consequences(vep_id)
            vep["colocated_variants"] = get_colocated_variants(vep_id)
        return veps
    else:
        return None

def get_transcript_consequences(vep_id):
    sql = f"""
        SELECT * FROM vep_transcript_consequences
        WHERE vep_id={vep_id}
    """
    transcript_consequences = sqlcontroller.db_run(sql, multi=True)
    if transcript_consequences:
        keys = [
            "id", 
            "vep_id", 
            "cadd_phred",
            "cadd_raw", 
            "hgvsc", 
            "hgvsp", 
            "mane_plus_clinical", 
            "mane_select", 
            "transcript_id",
            "gene_id",
            "gene_symbol",
            "gene_symbol_source",
            "biotype",
            "impact",
            "hgnc_id"
        ]
        transcript_consequences = [dict(zip(keys, values)) for values in transcript_consequences]
        for transcript_consequence in transcript_consequences:
            transcript_consequence_id = transcript_consequence.pop("id")
            consequence_terms = get_consequence_terms(transcript_consequence_id)
            if consequence_terms:
                transcript_consequence["consequence_terms"] = consequence_terms
            spliceai = get_spliceai(transcript_consequence_id)
            if spliceai:
                transcript_consequence["spliceai"] = spliceai
            alphamissense = get_alphamissense(transcript_consequence_id)
            if alphamissense:
                transcript_consequence["alphamissense"] = alphamissense
            del transcript_consequence["vep_id"]
        return transcript_consequences
    else:
        return None

def get_consequence_terms(transcript_consequence_id):
    sql = f"""
        SELECT * FROM vep_consequence_terms
        WHERE transcript_consequence_id={transcript_consequence_id}
    """
    consequence_terms = sqlcontroller.db_run(sql, multi=True)
    if consequence_terms:
        keys = [
            "id",
            "transcript_consequence_id",
            "term"
        ]
        consequence_terms = [dict(zip(keys, values)) for values in consequence_terms]
        terms = []
        for consequence_term in consequence_terms: 
            del consequence_term["id"]
            del consequence_term["transcript_consequence_id"]
            terms.append(consequence_term["term"])
        return terms
    else:
        return None

def get_spliceai(transcript_consequence_id):
    sql = f"""
        SELECT * FROM vep_spliceai
        WHERE transcript_consequence_id={transcript_consequence_id}
    """
    spliceai = sqlcontroller.db_run(sql)
    if spliceai:
        keys = [
            "id",
            "transcript_consequence_id",
            "SYMBOL",
            "DP_AG",
            "DS_DG",
            "DS_DL",
            "DP_DL",
            "DS_AG",
            "DP_AL",
            "DS_AL",
            "DP_DG"
        ]
        spliceai = dict(zip(keys, spliceai))
        del spliceai["id"]
        del spliceai["transcript_consequence_id"]
        return spliceai
    else:
        return None

def get_alphamissense(transcript_consequence_id):
    sql = f"""
        SELECT * FROM vep_alphamissense
        WHERE transcript_consequence_id={transcript_consequence_id}
    """
    alphamissense = sqlcontroller.db_run(sql)
    if alphamissense:
        keys = [
            "id",
            "transcript_consequence_id",
            "am_pathogenicity",
            "am_class"
        ]
        alphamissense = dict(zip(keys, alphamissense))
        del alphamissense["id"]
        del alphamissense["transcript_consequence_id"]
        return alphamissense
    else:
        return None

def get_colocated_variants(vep_id):
    sql = f"""
        SELECT * FROM vep_colocated_variants
        WHERE vep_id={vep_id}
    """
    colocated_variants = sqlcontroller.db_run(sql, multi=True)
    if colocated_variants:
        keys = [
            "id",
            "vep_id",
            "clin_sig",
            "clin_sig_allele",
            "phenotype_or_disease"
        ]
        colocated_variants = [dict(zip(keys, values)) for values in colocated_variants]
        for colocated_variant in colocated_variants:
            colocated_variant_id = colocated_variant.pop("id")
            frequencies = get_frequencies(colocated_variant_id)
            if frequencies:
                colocated_variant["frequencies"] = frequencies
            del colocated_variant["vep_id"]
        return colocated_variants
    else:
        return None

def get_frequencies(colocated_variant_id):
    sql = f"""
        SELECT * FROM vep_frequencies
        WHERE colocated_variant_id={colocated_variant_id}
    """
    frequencies = sqlcontroller.db_run(sql)
    if frequencies:
        keys = [
            "id",
            "colocated_variant_id",
            "gnomade_amr",
            "gnomade_nfe",
            "gnomade_sas",
            "gnomade_afr",
            "gnomade_eas"
        ]
        frequencies = dict(zip(keys, frequencies))
        del frequencies["id"]
        del frequencies["colocated_variant_id"]
        return frequencies
    else:
        None

def print_list(lst):
    for element in lst:
        if isinstance(element, list):
            print_list(element)
        elif isinstance(element, dict):
            print_dict(element)
        else:
            print(element)
def print_dict(dic):
    for key, value in dic.items():
        if isinstance(value, dict):
            print(key, ":")
            print_dict(value)
        elif isinstance(value, list):
            print(key, ":")
            print_list(value)
        else:
            print(key, ": ", value)

if __name__ == "__main__":
    vep = {
        "chrom": "chr1",
        "pos": 2556714,
        "ref": "A",
        "alt": "G",
        "most_severe_consequence": "foobar",
        "transcript_consequences": [
            {
                "transcript_id": "foobar",
                "gene_id": "foobar",
                "gene_symbol": "foobar",
                "gene_symbol_source": "foobar",
                "biotype": "foobar",
                "impact": "foobar",
                "cadd_phred": 1234567.891,
                "cadd_raw": 1234.567891,
                "hgvsc": "foobar",
                "hgvsp": "foobar",
                "hgnc_id": "foobar",
                "mane_plus_clinical": "foobar",
                "mane_select": "foobar",
                "consequence_terms": [
                    "foo",
                    "bar"
                ],#consequence_terms
                "spliceai": {
                    "DS_AG": 12345.67891,
                    "DP_DG": 12345.67891,
                    "DP_AL": 12345.67891,
                    "SYMBOL": "foobar",
                    "DS_DL": 12345.67891,
                    "DP_DL": 12345.67891,
                    "DS_AL": 12345.67891,
                    "DS_DG": 12345.67891,
                    "DP_AG": 12345.67891,
                },#spliceai
                "alphamissense": {
                    "am_pathogenicity": 123456.7891,
                    "am_class": "foobar",
                }#alphamissense
            }#transcript_consequence
        ],#transcript_consequences
        "colocated_variants": [
            {
                "clin_sig": "foobar",
                "clin_sig_allele": "foobar",
                "phenotype_or_disease": 42,
                "frequencies": {
                    "gnomade_amr": 12345.67891,
                    "gnomade_afr": 12345.67891,
                    "gnomade_eas": 12345.67891,
                    "gnomade_sas": 12345.67891,
                    "gnomade_nfe": 12345.67891,
                }#frequencies
            }#colocated_variant
        ]#colocated_variants
    }#vep

    print("now going to insert vep")
    id = insert_vep(vep)
    print(f"vep inserted under id={id}")
    print("vep:")
    print_dict(vep)
    print("now going to extract vep")
    extract = get_vep(chrom="chr1", pos=2556714, ref="A", alt="G")
    for element in extract:
        print_dict(element)
        print("Equal in and out: ", vep == element)
