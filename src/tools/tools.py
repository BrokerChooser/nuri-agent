import pandas as pd
from langchain_core.tools import tool
from langgraph.graph import MessagesState
from src.tools.nuclia_client import Nuclia_model,nuclia_prompt
from src.tools.oanda_client import Oanda_client
from utils.db_utils import execute_queries_from_db, load_sql_file


# Define the tools for the agent to use
@tool
def nuclia_search(state: MessagesState):
    """Call this functions when you get searches about brokers.
    You can get questions about fees, account opening, etc. E.g: ibkr fees.
    This is a RAG system, always call this tool as baseline. """
    query = state['messages']

    # Create Nuclia client and call query
    nuclia_client=Nuclia_model()
    response=nuclia_client.search(query=query[0]['content'],prompt=nuclia_prompt)

    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


@tool
def broker_scam_check(broker_name: str):
    """Use to check whether a broker is legitimate and trustworthy. Use this function to check if a broker is regulated"""

    # Query not_reviewed_broker table and brokers table
    query_non_reviewed=load_sql_file('src/tools/sqls/non_reviewed_broker_regulation.sql').format(broker_name=broker_name,broker_slug=broker_name.lower())
    query_reviewed=load_sql_file('src/tools/sqls/reviewed_broker_regulation.sql').format(broker_name=broker_name,broker_slug=broker_name.lower())

    scam_df_list = execute_queries_from_db("db_credential.json", [query_reviewed,query_non_reviewed])
    scam_df=pd.concat(scam_df_list) # merge two dataframes

    if scam_df.empty:
        print("The DataFrame is empty.")
        return f"We don't have info about {broker_name}."

    valid_category=scam_df['category'].values[0]
    regulator=scam_df['regulation'].values[0]

    if valid_category in (2,3):
        return f"Broker {broker_name} is legitimate and trustworthy! {regulator}"
    elif valid_category == 1 :
        return f"Beware of potential scams from {broker_name}! {regulator}"


@tool
def get_forex_price(instrument: str):
    """With this function, a forex's price can be requested from OANDA API.
    Always call this with two currencies with their three-digit numeric codes, separated with '_'.
    I give you couple of examples for three-digit numeric values:
    USD - United States Dollar,
    EUR - Euro,
    GBP - British Pound Sterling,
    AUD - Australian Dollar,
    CAD - Canadian Dollar

    I give you couple of examples how to pass the instrument parameter:
    USD_EUR,
    GBP_AUD,
    GBP_EUR,
    CAD_AUD,
    EUR_USD
    """
    oanda_client=Oanda_client()

    response=oanda_client.get_price(instrument)

    if response['status_code']==200:
        return f"{response['message']}, the {response['data']['instrument']} instrument's bid price is {response['data']['bid_price']} and ask price is {response['data']['ask_price']}"
    else:
        return f"Currently, I can't fetch the request. The reason: {response['message']}. Please try again"

