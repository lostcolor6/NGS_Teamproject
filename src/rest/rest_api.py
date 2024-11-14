import json
import subprocess
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
import requests
import logging
import os
import sys
from typing import List, Tuple
import asyncio
from src.database import vepcontroller
import uvicorn
from src.util import output_parser


# here the FastAPI application is initialized
app = FastAPI()

# creating logging to be able to see what is happening at specific times in an "app.log" file
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# constants for the Ensembl REST API are defined below
ENSEMBL_REST_API_URL = "https://rest.ensembl.org"
MAX_ELEMENTS_PER_REQUEST = 1  # process no more than 200 variants per request/chunks


# important for HGVS JSON file that is generated
def single_to_double_quotes(json_str: str) -> str:
    """Replaces single quotes with double quotes in a string."""
    return json_str.replace("'", '"')


# function that converts VCF data (variant data) to HGVS notation
def convert_to_hgvs(chrom, pos, ref, alt):
    # removes 'chr' prefix from chromosome names if present
    if chrom.startswith("chr"):
        chrom = chrom[3:]

    pos = int(pos)

    try:
        if len(ref) == 1 and len(alt) == 1:  # substitution
            return f"{chrom}:g.{pos}{ref}>{alt}"
        elif len(ref) > len(alt) == 1:  # deletion
            end_pos = pos + len(ref) - 1
            return f"{chrom}:g.{pos}_{end_pos}del{ref[1:]}"
        elif len(ref) == 1 and len(ref) < len(alt):  # insertion
            end_pos = pos + 1
            return f"{chrom}:g.{pos}_{end_pos}ins{alt[1:]}"

    except Exception as e:
        # logging of the error and raises an HTTPException if conversion fails
        logger.error(f"Failed to convert to HGVS notation: {e}")
        raise HTTPException(status_code=400, detail="Failed to convert to HGVS notation")


# asynchronous function to process a chunk of HGVS notations (avoids overwhelming the API) and make a request to the Ensembl VEP API
async def process_chunk(
    hgvs_chunk,
    species = "homo_sapiens",
    alphamissense = True,
    cadd = "1",
    spliceai = 1,
    gencode_basic = True,
    hgvs_parameter = True,
    mane = True,
    chunk_number = 1,
    total_chunks = 1
):

    json_data = json.dumps(hgvs_chunk)
    corrected_json_data = single_to_double_quotes(json_data)
    # logging the chunk being processed
    logger.info(f"Processing {chunk_number} of {total_chunks} elements: {corrected_json_data}")

    # defining the API endpoint and request parameters
    endpoint_url = f"{ENSEMBL_REST_API_URL}/vep/{species}/hgvs"
    headers = {"Content-Type": "application/json"}
    params = {
        "AlphaMissense": alphamissense,
        "CADD": cadd,
        "SpliceAI": spliceai,
        "gencode_basic": gencode_basic,
        "hgvs": hgvs_parameter,
        "mane": mane
    }

    logger.info(f"Request URL: {endpoint_url}")
    logger.info(f"Request Headers: {headers}")
    logger.info(f"Request Params: {params}")
    logger.info(f"Request Body: {json.loads(corrected_json_data)}")

    try:
        # sends a POST request to the Ensembl VEP API with the HGVS notations that has been converted above
        response = requests.post(
            endpoint_url,
            headers=headers,
            json={"hgvs_notations": [json.loads(corrected_json_data)]},
            params=params
        )
        response.raise_for_status()
        logger.info(f"POST request successful for chunk {chunk_number} of {total_chunks} with {len(hgvs_chunk)} elements")
        logger.info(str(response.json())) # includes logging for every JSON produced by each chunk (large data set)
        return response.json() # API's response in JSON from one chunk

    except requests.RequestException as e:
        logger.error(f"Request to Ensembl VEP API failed for chunk {chunk_number}: {e.response.text if e.response else e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# POST route at "/vep"
@app.post("/vep")
async def get_vep(request: Request):
    # extract + parse JSON data from incoming request
    data = await request.json()
    # retrieve VEP data from DB using chrom, pos.
    database_result = vepcontroller.get_vep(chrom=data["chrom"], pos=data["pos"], alt=data["alt"], ref=data["ref"])
    # checks if DB returned results
    if bool(database_result):
        # when results are found, return JSON response
        return JSONResponse(content=database_result, status_code=200)
    else:
        print("no entry in DB for: " + data["chrom"] + str(data["pos"]) + data["alt"] + data["ref"])
        hgvs = convert_to_hgvs(chrom=data["chrom"], pos=data["pos"], alt=data["alt"], ref=data["ref"])
        # process the HGVS string asynchronously to retrieve data from Ensembl API
        api_result = await process_chunk(hgvs)
        parsed = output_parser.json_parser(str(api_result))
        # insert the parsed data into the DB for later usage
        vepcontroller.insert_vep(json.loads(parsed), chrom=data["chrom"], pos=data["pos"], alt=data["alt"], ref=data["ref"])
        # access the DB again to retrieve the newly inserted data
        database_result = vepcontroller.get_vep(chrom=data["chrom"], pos=data["pos"], alt=data["alt"], ref=data["ref"])
        # return DB result as JSON response
        return JSONResponse(content=database_result, status_code=200)

if __name__ == "__main__":
    if "reload" in sys.argv:
        subprocess.run(["uvicorn", "src.connector.fastapi:app", "--reload"])
    else:
        uvicorn.run(app, host="127.0.0.1", port=8000)
