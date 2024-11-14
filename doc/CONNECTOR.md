# Connector module

## Basic usage

This modules aim is to provide a way from outside to connect to the database and to be able to poll the api for missing entries.  

The API is realized in the `api.py` file and can be started, simply by running `python -m src.connector.fastapi`.  
While it is running the webapi can be accessed on port 8000 of the machine running the api code.  

### Available Calls:
- HPOs: `127.0.0.1:8000/hpo_gs/<gene_symbol>`  
- HPOs: `127.0.0.1:8000/hpo_id/<hpo_id>`  
- VEPs: `127.0.0.1:8000/vep/<chrom>/<pos>/<ref>/<alt>`  

Returns a json containing all entries from the database that match the given fields.  

## Retrieving data

Using the `apifetch` function from the `connector`-module one can retrieve data from the api (or any api actually) rather comfortably by providing the function a url and getting a list of dictionaries (one for each json object in return).  
Example:  
```python
apifetch("127.0.0.1:8000/hpo_gs/baz")
```  

```python
apifetch("127.0.0.1:8000/vep/1/1/A/T")
```

## Missing

- A way to connect to the VEP-API to check for missing entries
- ~~A way to poll for VEP entries in the database~~
- ~~A way to access the data automagically on the client device by parsing the webapi~~


## Technical

### API

The main module api is used to start the api webserver and to provide the neccessary functions to access data.  
These can be written in the following format:  
```python
@app.get("/<name>/{input}")
def some_function(input):
    data_to_be_returned = [{"data": data}, {"also_data": data}]
    return JSONResponse(content=data_to_be_returned)

```
this causes `127.0.0.1:8000/name/<input>` to be accessable and to return the output of `data_to_be_returned` as json. Note that `some_data` can be a function call.

### apifetch

These are just two very simple functions and a third one to wrap the other two.  
- `fetch_data_from_api(str)` takes a url as string and returns a json string.  
- `json_to_dict(str)` takes a json string containing json objects and parses them into multiple dictionaries which it returns as a list.  
- `apifetch(str)` simply does both: take a url and return a list of dictionaries



### hpoconnector

Kind of like the counterpart of the `hpocontroller`-routine from the `database`-module. It connects the `fetch_hpo(str)` method from the controller to the api by turning the output into a list of dictionaries.
