import psycopg2
from configparser import ConfigParser
import os

def load_config(filename="config/database.ini", section="postgresql"):
    """Loads a database config"""

    # current_dir = os.path.dirname(__file__)
    # filepath = os.path.join(current_dir, filename)

    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {filename} file")

    return config

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        with psycopg2.connect(**config) as conn:
            return conn
    except (pyscopg2.DatabaseError, Exception) as error:
        print(error)

def db_run(sql, data=(), fetch=True, multi=False, returning=False, config="config/database.ini"):
    """
    Run SQL statements against the database.

    Args:
        sql (str): The SQL statement to be run. Use %s as placeholder.
        data (tuple, optional): A tuple to be put into placeholders. Should be same size as number of placeholders in sql. Defaults to ().
        fetch (bool, optional): Whether the statement is expected to fetch values (query). Defaults to True.
        multi (bool, optional): Whether the statement is expected to fetch multiple values (query). No effect without fetch. Defaults to False.
        returning (bool, optional): Whether the statement contains a returning keyword. Defaults to False.
        config (str, optional): The configuration file for the database. Defaults to "config/database.ini".

    Returns:
        Varies: The return type and value depends on the SQL query and the database response.
    """
    config = load_config(filename=config)
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, data)

                if fetch:
                    if multi:
                        return cur.fetchall()
                    else:
                        return cur.fetchone()
                elif returning:
                        row = cur.fetchone()
                        if row:
                            return row[0]
                        else:
                            raise Exception("Could not get return value")

    except (Exception, psycopg2.DatabaseError) as error:
        print("An error has occured (x01): ", error)

def db_run_batch(sql_list, fetch=True, multi=False, config="config/database.ini"):
    conn = None
    config = load_config(filename=config)
    return_values = []

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for statement in sql_list:
                    cur.execute(statement)
                    if fetch:
                        if multi:
                            return_values.append(cur.fetchall())
                        else:
                            return_values.append(cur.fetchone())
                conn.commit()
                return return_values
    except (Exception, psycopg2.DatabaseError) as error:
        if conn:
            conn.rollback()
        print(error)

if __name__ == "__main__":
    sql1 = """
        SELECT * FROM vep;
    """
    sql2 = """
        SELECT * FROM hpo_gene_associations;
    """

    sql_list = [sql1, sql2]

    result = db_run_batch(sql_list)
    print("result:")
    for element in result:
        print(element)
