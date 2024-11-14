from src.database import vepcontroller

def get_vep(chrom, pos, alt, ref):
    database_result = vepcontroller.get_vep(chrom=chrom, pos=pos, alt=alt, ref=ref)
    if bool(database_result):
        return database_result
    return []

def resolve_vcf(content):
    # Initialize an empty list to store the results
    results = []
    
    # Split the content into lines
    lines = content.splitlines()
    
    # Iterate over each line with an index
    for index, line in enumerate(lines):
        # Skip lines that start with '#' (comments and headers)
        if line.startswith('#'):
            continue
        
        # Split each line into columns
        columns = line.strip().split()

        # Extract the chrom, pos, ref, and alt values
        chrom = columns[0]
        pos = columns[1]
        ref = columns[3]
        alt = columns[4]
        
        # Append a tuple of these values along with the index to the results list
        results.append((index, chrom, pos, ref, alt))
    
    # Return the results list
    return results

def lookup_identifiers(identifiers):
    for i, identifier in enumerate(identifiers):
        database_result = vepcontroller.get_vep(chrom=identifier[1], pos=identifier[2], ref=identifier[3], alt=identifier[4])
        if bool(database_result):
            identifiers[i] = database_result
    return identifiers

def reduce_vcf(vcf, identifiers):
    # Split the VCF string into lines
    lines = vcf.splitlines()
    
    # Create a set of line numbers to be deleted
    lines_to_delete = {identifier[0] for identifier in identifiers if isinstance(identifier, tuple)}
    
    # Collect lines that are not in the set of lines to be deleted
    remaining_lines = [line for index, line in enumerate(lines) if index not in lines_to_delete]
    
    # Filter out the tuples from the identifiers list that have their line numbers in the set of lines to be deleted
    updated_identifiers = [identifier for identifier in identifiers if not (isinstance(identifier, tuple) and identifier[0] in lines_to_delete)]
    
    # Join the remaining lines back into a single string
    modified_vcf = '\n'.join(remaining_lines)
    
    # Return the modified VCF string and the updated identifiers list
    return modified_vcf, updated_identifiers

def lookup_vcf(vcf_string):
    identifiers = resolve_vcf(vcf_string)
    lookup_list = lookup_identifiers(identifiers)
    missing_vcf, result = reduce_vcf(vcf_string, lookup_list)
    return {"annotations": result[0], "missing": missing_vcf}


if __name__ == "__main__":
    veps = get_vep(chrom=1, pos=1, ref="A", alt="T")
    if veps:
        for i in veps:
            for j,k in i.items():
                print(j, ": ", k)
    content = open('test.vcf').read()
    veps = lookup_vcf(content)["annotations"]
    print("veps:")
    if veps:
        print(len(veps))
        for i in veps:
            print(type(i), len(i))
            for j,k in i.items():
                print(j, ": ", k)
    print("remaining vcf:")
    print(lookup_vcf(content)["missing"])
