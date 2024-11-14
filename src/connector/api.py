from flask import Flask, jsonify
from src.connector import hpoconnector, vepconnector


app = Flask(__name__)

@app.route('/hpo/<gene_symbol>', methods=['GET'])
def hpo_lookup(gene_symbol):
    return jsonify(hpoconnector.get_hpo(gene_symbol, searchfield="symbol"))
    # Placeholder:
    # return jsonify({'gene_symbol': gene_symbol})

@app.route('/hpo_gs/<hpo_id>', methods=['GET'])
def hpo_gs_lookup(hpo_id):
    return jsonify(hpoconnector.get_hpo(hpo_id, searchfield="id"))

@app.route('/vep/<chrom>/<pos>/<ref>/<alt>', methods=['GET'])
def vep_lookup(chrom, pos, ref, alt):
    return jsonify(vepconnector.get_vep(chrom=chrom, pos=pos, ref=ref, alt=alt))
    # Placeholder:
    # return jsonify({'chrom': chrom, 'pos': pos, 'ref': ref, 'alt': alt})

if __name__ == '__main__':
    app.run()
