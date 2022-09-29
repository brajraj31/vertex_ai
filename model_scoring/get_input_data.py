'''This module is use to get input data from different resources'''

def get_input_data(query: str, project_id: str) -> str:

    from google.cloud import bigquery
    import pandas
    import os

    
    temp_table = "qwiklabs-gcp-01-df00ef1cf655.credit.credit_data_temp"
    
    #Load the data from Bigquery based on given query
    client = bigquery.Client(location="us-central1", project=project_id)
    load_job = client.query(query) 
    df = load_job.to_dataframe()
    
    #Upload the batch data to a temporary table
    client.load_table_from_dataframe(dataframe= df, destination=temp_table)
    
    return temp_table