# General Guide:

- Make sure postgresql service is running
    (Use services on Windows or systemctl on UNIX)
- (only once) Create a database in the psql console (or use the default one, called "postgres")
- (only once) Insert the correct db name and credentials in the database.ini file
- Make sure the venv is properly running using the steps detailed below (to prevent polluting your own python installation)
- (only once) Install the necessary packages using the requirements.txt (see below)
- import and use the `db_run` function from the `sqlcontroller` module in your code like this:

```python
from database import sqlcontroller
sqlcontroller.db_run(sql, data=(), fetch=True, multi=False, returning=False)
```  
Parameters:  
- `sql`: A single String containing the sql statement to be run. You can use `%s` as placeholder for values supplied by the data tuple.  
- `data`: A tuple containing the data to be filled in the placeholders in the statement. Defaults to empty. Results in an error if there are more placeholders than tuple elements.  
- `fetch`: A boolean stating whether you expect the statement to return something. Defaults to true. The Return value will be a tuple containig the returned row.  
- `multi`: A boolean stating whether you expect the statement to return multiple rows. Defaults to false. The return value will be a List of tuples. Works only if `fetch` is `True`.
- `returning`: A boolean made for sql statements returning a single field (usually the ID of a created object). Defaults to false and works only if `fetch` and `multi` are set to `False`

Examples:  
- `sqlcontroller.db_run("SELECT * FROM table WHERE id=1;")` Returns the row where id is 1 (assuming there is only one)  
- `sqlcontroller.db_run("SELECT * FROM table;", mutli=True)` Returns all rows in `table` as a list of tuples.  
- `sqlcontroller.db_run("INSERT INTO table VALUES(%s%s%s);", (1, 2, 3), fetch=False)` Insert 1,2,3 into `table`.  
- `sqlcontroller.db_run("INSERT INTO table VALUES(1) RETURNING id;", returning=True)` Inserts 1 into `table` and returns the id of the inserted row.  

# Currently created tables:
(Written as actual tables to make it easier to understand. Remember to scroll sideways if necessary.  
Italic is the primary key.  
Serial means a new value gets created for this column whenever a new row is created.
Values behind String types are the maximum length of the string to be put there.)  

hpo_gene_associations:  
| *id*    | hpo_id      | hpo_name    | ncbi_gene_id | gene_symbol | disease_id |
| ------- | ----------- | ----------- | ------------ | ----------- | ---------- |
| Integer | String(255) | String(255) | Integer      | String(255) | Integer    |
| Serial  |             |             |              |             |            |

patients:  
| *id*    | firstname   | lastname    | age     |
| ------- | ----------- | ----------- | ------- |
| Integer | String(255) | String(255) | Integer |
| Serial  |             |             |         |

phenotype_associations:  
| *id*    | patientid         | hpoid                          |
| ------- | ----------------- | ------------------------------ |
| Integer | Integer           | Integer                        |
| Serial  | Ref: patients(id) | Ref: hpo_gene_associations(id) |

vep:  
| *id*    | alphamissense | cadd    | spliceaAI | gencode_basic | hgvs    | mane      | gene_id    | gene_symbol | gene_symbol_source | hgnc_id     | clin_sig    | clin_sig_allele | phenotype_or_disease |
| ------- | ------------- | ------- | --------- | ------------- | ------- | --------- | ---------- | ----------- | ------------------ | ----------- | ----------- | --------------- | -------------------- |
| Integer | Integer       | Integer | Integer   | Integer       | Integer | Integer   | String(15) | String(255) | String(255)        | String(255) | String(255) | String(255)     | Integer              |
| Serial  |               |         |           |               |         |           |            |             |                    |             |             |                 |                      |

vep_transcript_ids:  
| *id*    | transcript_id | vep_id      |
| ------- | ------------- | ----------- |
| Integer | String(255)   | Integer     |
| Serial  |               | Ref:vep(id) |

vep_consequence_terms:  
| *id*    | term        | vep_id      |
| ------- | ----------- | ----------- |
| Integer | String(255) | Integer     |
| Serial  |             | Ref:vep(id) |

# Available Functions:

(obvously there is more to come...)

- `hpocontroller`: `insert_hpo(dataset)` insert a tuple:
    | field        | type   |
    | ------------ | ----   |
    | hpo_id       | string |
    | hpo_name     | string |
    | ncbi_gene_id | int    |
    | gene_symbol  | string |
    | disease_id   | int    |

    into the hpo table.
- `hpocontroller`: `fetch_hpo(gene_symbol)` retrieve a list of hpo entries by their gene_symbol. 

- `vepcontroller`: `insert_vep(vep)` insert a vep entry as dictionary  
    Example:  
    ```python
    vep = {
        "AlphaMissense": 42,
        "cadd": 42,
        "spliceaAI": 42,
        "gencode_basic": 42,
        "hgvs": 42,
        "mane": 42,
        "gene_id": "foobar",
        "gene_symbol": "foobar",
        "gene_symbol_source": "foobar",
        "hgnc_id": "foobar",
        "clin_sig": "foobar",
        "clin_sig_allele": "foobar",
        "phenotype_or_disease": 42,
        "transcript_id": ["foo","bar","baz"],
        "consequence_terms": ["foo", "bar", "baz"]
    }
    ```  
    None of the fields are optional and the fields should be called exactly like that.  

- `vepcontroller`:
    ```python
    get_vep(
        AlphaMissense = None,
        cadd = None,
        spliceaAI = None,
        gencode_basic = None,
        hgvs = None,
        mane = None,
        gene_id = None,
        gene_symbol = None,
        gene_symbol_source = None,
        hgnc_id = None,
        clin_sig = None,
        clin_sig_allele = None,
        phenotype_or_disease = None
    )
    ```  
    All of these fields are optional, so it is possible to filter out exactly the entries one wants to retrieve. If none are set, it prints an error.  

# (Very) Quick SQL overview:
(I included this for testing purposes or the inclined reader. It is not expected for you to know or use this. It is my job to turn these into ready to use functions like the ones listed above.)

(obviously `table`, `column##` and `value##` need to be changed for proper values)

Inserting stuff:  
```SQL
    INSERT INTO table(column01, column02, ...)
    VALUES(value01, value02, ...);
```

Updating stuff:  
```SQL
    UPDATE table
    SET column01=value01, column02=value02, ...
    WHERE condition;
```

Retrieving Stuff:  
```SQL
    SELECT column01, column02, ...
    FROM table
    WHERE condition;
```

# Batch SQL

If speed is important and one wants to run a big number of statements, there is a dedicated batch version of `db_run`:  

```python
from database import sqlcontroller
sqlcontroller.db_run_batch(sql_list, fetch=True, multi=False)
```

It does not support datasets, so it needs to be provided with a list of finished sql statements (use variable strings if necessary).  
If fetch is set to True, it returns a list of responses. However, this behaviour has not been tested (yet).


# Virtual Environment

## Introduction

A virtual environment allows you to create an independent python instance not using any of your installed packages, so you can keep things separated and clean.  
This functionality is provided by the `venv` package for python.
We can run packages as standalone programs using `python -m <package name>`.

## Creating a venv

You can create a venv by calling `python -m venv <venv-name>`
It then gets created as a subfolder in the current directory. After activating it using the steps detailed below we can check that there is indeed only pip installed by running `pip list` or `python -m pip list`.  
If we now install packages using `pip` they will be installed in our venv, not our system instance.

## Importing requirements

It is very easy to install necessary packages with pip by pulling them as a list from a file.  
This can simply be done by running `pip install -r <filename>` or `python -m pip install -r <filename>`

## Activating/Deactivating the virtual environment

You can see that a venv is active by checking your prompt. There should be the venvs name in front of it as long as it is active (I'd provide screenshots, but my prompt is customized, so they wouldnt be much use.)

### Linux/MacOS

`source database-venv/bin/activate`

### Powershell

`./database-venv/bin/Activate.ps1`

### Deactivation

`deactivate`

# Clearing and setting up the database

Clearing all relations (tables)

`python clear.py`

Creating all relations (not filling them)

`python create.py`

# pgadmin 4 (not used anymore)

## Starting pgadmin4

- Enter venv and run `pgadmin4`
- Open `http://127.0.0.1:5050` in browser
- Login: admin@admin.com // admin@123
- If database sever needs to be added:
    postgres@localhost // postgres
