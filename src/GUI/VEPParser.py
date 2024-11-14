def get_vep_columns(vep_dict: dict):
    out = {
        'chrom': vep_dict['chrom'],
        'pos': vep_dict['pos'],
        'ref': vep_dict['ref'],
        'alt': vep_dict['alt'],
    }
    try:
        out['gene symbol'] = vep_dict['transcript_consequences'][0]['gene_symbol']
    except:
        out['gene symbol'] = 'None'
        
    try:
        out['clinical significance'] = vep_dict['colocated_variants'][0]['clin_sig']
    except:
        out['clinical significance'] = 'None'
        
    try:
        out = out | {'gnomAD amr': vep_dict['colocated_variants'][0]['frequencies']['gnomade_amr'],
        'gnomAD nfe': vep_dict['colocated_variants'][0]['frequencies']['gnomade_nfe'],
        'gnomAD sas': vep_dict['colocated_variants'][0]['frequencies']['gnomade_sas'],
        'gnomAD afr': vep_dict['colocated_variants'][0]['frequencies']['gnomade_afr'],
        'gnomAD eas': vep_dict['colocated_variants'][0]['frequencies']['gnomade_eas']}
    except:
        out = out | {'gnomAD amr': 'None',
        'gnomAD nfe': 'None',
        'gnomAD sas': 'None',
        'gnomAD afr': 'None',
        'gnomAD eas': 'None'}
        
    try:
        out['impact'] = vep_dict['transcript_consequences'][0]['impact']
    except:
        out['impact'] = 'None'
        
    try:
        out['consequence terms'] = ','.join(vep_dict['transcript_consequences'][0]['consequence_terms'])
    except:
        out['consequence terms'] = 'None'
    
    return out