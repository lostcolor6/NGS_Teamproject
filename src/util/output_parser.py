import json
import sys
import re

def repair_json(json_string):
    # Replace single quotes around keys and values with double quotes
    repaired_json = re.sub(r"(?<!\\)'", '"', json_string)
    return repaired_json

def json_loader(json_string):
    try:
        # Try to parse the JSON string as is
        json.loads(json_string)
        return json_string
    except json.JSONDecodeError:
        # If parsing fails, attempt to repair the JSON string
        repaired_json = repair_json(json_string)
        try:
            # Try to parse the repaired JSON string
            json.loads(repaired_json)
            return repaired_json
        except json.JSONDecodeError:
            # Raise an error if the repaired JSON is still invalid
            raise ValueError("Invalid JSON format")

def json_parser(json_string):
    # loading the JSON data from the given string
    # data = json.loads(json_string)
    string = json_loader(json_string)
    data = json.loads(string)
    with open('in.json', 'w') as file:
        file.write(string)

    result = {}

    for index, entry in enumerate(data):
        most_severe_consequence = entry.get('most_severe_consequence', None) # extract the "most_severe_consequence" field (which is not inside other fields)

        # using index for the dictionary key
        result_key = f"entry_{index}"

        # processing the "colocated_variants"
        colocated_variants = entry.get('colocated_variants', [])
        colocated_variants_data = []
        for variant_entry in colocated_variants:
            # making extraction of "frequencies"" dictionary
            frequencies = variant_entry.get('frequencies', {})
            # to access the "C" dictionary within frequencies
            c_frequencies = frequencies.get('C', {})

            colocated_variant_entry = {
                'clin_sig_allele': variant_entry.get('clin_sig_allele', None),
                'clin_sig': variant_entry.get('clin_sig', None),
                'phenotype_or_disease': variant_entry.get('phenotype_or_disease', None),
                'frequencies': {
                    'gnomade_amr': c_frequencies.get('gnomade_amr', None),
                    'gnomade_afr': c_frequencies.get('gnomade_afr', None),
                    'gnomade_eas': c_frequencies.get('gnomade_eas', None),
                    'gnomade_sas': c_frequencies.get('gnomade_sas', None),
                    'gnomade_nfe': c_frequencies.get('gnomade_nfe', None),
                }
            }
            colocated_variants_data.append(colocated_variant_entry)

        # processing the "transcript_consequences"
        transcript_consequences = entry.get('transcript_consequences', [])
        transcript_consequences_data = []
        for transc_entry in transcript_consequences:
            # extracting the fields from spliceai
            spliceai = transc_entry.get('spliceai', {})
            transcript_consequence_entry = {
                'transcript_id': transc_entry.get('transcript_id', None),
                'gene_id': transc_entry.get('gene_id', None),
                'gene_symbol': transc_entry.get('gene_symbol', None),
                'gene_symbol_source': transc_entry.get('gene_symbol_source', None),
                'biotype': transc_entry.get('biotype', None),
                'impact': transc_entry.get('impact', None),
                'cadd_raw': transc_entry.get('cadd_raw', None),
                'cadd_phred': transc_entry.get('cadd_phred', None),
                'hgvsc': transc_entry.get('hgvsc', None),
                'hgvsp': transc_entry.get('hgvsp', None),
                'hgnc_id': transc_entry.get('hgnc_id', None),
                'consequence_terms': transc_entry.get('consequence_terms', []),
                'spliceai': {
                    'DS_AG': spliceai.get('DS_AG', None),
                    'DP_DG': spliceai.get('DP_DG', None),
                    'DP_AL': spliceai.get('DP_AL', None),
                    'SYMBOL': spliceai.get('SYMBOL', None),
                    'DS_DL': spliceai.get('DS_DL', None),
                    'DP_DL': spliceai.get('DP_DL', None),
                    'DS_AL': spliceai.get('DS_AL', None),
                    'DS_DG': spliceai.get('DS_DG', None),
                    'DP_AG': spliceai.get('DP_AG', None)
                }
            }
            transcript_consequences_data.append(transcript_consequence_entry)

        # to organize the processed data into the result dictionary
        result[result_key] = {
            'most_severe_consequence': most_severe_consequence,
            'transcript_consequences': transcript_consequences_data,
            'colocated_variants': colocated_variants_data
        }

    return json.dumps(result, indent=4)


if __name__ == "__main__":
    # json_string = '''

    # '''
    json_string = open(sys.argv[1]).read()

    parsed_data = json_parser(json_string) # call the function to parse the JSON data

    # print the dictionary in a format that is readable
    # [print(key, ": ", type(value)) for key,value in parsed_data.items()]

    # Write the serialized dictionary to a file
    with open('out.json', 'w') as file:
        file.write(parsed_data)
