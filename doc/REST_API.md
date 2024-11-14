# Documentation for Annotation Service: REST API
To initialize the FastAPI service, execute from the project folder “fastapi dev src/rest/rest_api.py”. This will launch the application. To access the API documentation endpoint, open in a web browser the following link: “ http://127.0.0.1:8000/docs” (which is an interactive interface). Afterwards, the POST method has to be clicked, following “Try it out“, where JSON data can be uploaded. Finally, click execute and it will take a few seconds or minutes. Insomnia (or another API client to test the request) or a terminal can also be used. To execute from a terminal with curl (which can be imported in Insomnia): \
curl -X POST "http://127.0.0.1:8000/vep" -H "Content-Type: application/json" -d '{"chrom": "1", "pos": "12345", "ref": "A", "alt": "T"}'

# Code explained:

## Imports and Setup
- Imports essential libraries and modules.
- Logging is configured to track application events.

## Utility Functions
- **`single_to_double_quotes()`**: Replaces single quotes with double quotes in JSON strings.
- **`convert_to_hgvs()`**: Converts VCF data (variant coordinates) to HGVS notation.

## Asynchronous Processing
- **`process_chunk()`**: Processes a chunk of HGVS notations asynchronously.

## API Endpoint

- **`/vep `**: Handles JSON input for processing VCF data. This endpoint receives a JSON object containing chromosome (chrom), position (pos), reference allele (ref), and alternate allele (alt) information, converts it to HGVS notation, and queries the Ensembl VEP API for annotation. If data is already available in the database, it retrieves the result directly from there.
