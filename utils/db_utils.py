from sshtunnel import SSHTunnelForwarder
import pymysql
import paramiko
import pandas as pd
from utils.logging_utils import log_to_output
import json

def execute_queries_from_db(credential_json_path, queries):
    """Execute a list of queries on a remote database and return the results as a list of dataframes"""

    with open(credential_json_path, "r") as f:
        json_dict = json.load(f)

    result = []
    log_to_output("Connecting to database")

    # if it runs locally
    if 'ssh_host' in json_dict.keys():
        mypkey = paramiko.RSAKey.from_private_key_file(json_dict['ssh_private_key_path'],password=json_dict['ssh_private_key_password'])

        with SSHTunnelForwarder((json_dict['ssh_host'], json_dict['ssh_port']), ssh_username=json_dict['ssh_username'],ssh_pkey=mypkey, remote_bind_address=(json_dict['sql_hostname'], json_dict['sql_port'])) \
            as tunnel:
            return run_queries(json_dict, queries, tunnel.local_bind_port)
    else:
        return run_queries(json_dict, queries, json_dict['sql_port'])

def run_queries(json_dict, queries, sql_port):
    result = []
    conn = pymysql.connect(host=json_dict['sql_hostname'],
                           user=json_dict['sql_username'],
                           passwd=json_dict['sql_password'],
                           db=json_dict['sql_main_database'],
                           port=sql_port)
    for query in queries:
        log_to_output("Executing query")
        try:
            result.append(pd.read_sql_query(query, conn))
        except ValueError:
            result.append(pd.DataFrame({'ERROR': []}))
    conn.close()
    log_to_output("Executed query")
    return result

def load_sql_file(filename):
    with open(filename, 'r') as sql_file:
        return sql_file.read()
