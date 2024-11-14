import subprocess
import sys
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from src.connector import hpoconnector, vepconnector

app = FastAPI()

# Define available paths:

@app.post("/get-variants")
async def upload_vcf(file: UploadFile = File(...)):
    contents = await file.read()
    contents_str = contents.decode("utf-8")
    data = vepconnector.lookup_vcf(contents_str)
    return JSONResponse(content=data)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/hpo_gs/{gene_symbol}")
def hpo_gs_lookup(gene_symbol):
    list_of_dicts = hpoconnector.get_hpo(gene_symbol, searchfield="symbol")
    return JSONResponse(content=list_of_dicts)

@app.get("/hpo_id/{hpo_id}")
def hpo_id_lookup(hpo_id):
    list_of_dicts = hpoconnector.get_hpo(hpo_id, searchfield="id")
    return JSONResponse(content=list_of_dicts)

@app.get("/vep/{chrom}/{pos}/{ref}/{alt}")
def vep_lookup(chrom, pos, ref, alt):
    list_of_dicts = vepconnector.get_vep(chrom=chrom, pos=pos, ref=ref, alt=alt)
    return JSONResponse(content=list_of_dicts)

if __name__ == "__main__":
    import uvicorn
    if "reload" in sys.argv:
        subprocess.run(["uvicorn", "src.connector.fastapi:app", "--reload"])
    else:
        uvicorn.run(app, host="127.0.0.1", port=5000)
