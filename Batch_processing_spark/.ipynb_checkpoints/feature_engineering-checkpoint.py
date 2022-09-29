'''This model is use to get input data from different resources'''


def feature_engineering(input_temp_table: str
                        , project_id: str) -> str:

    from google.cloud import bigquery
    import pandas
    import os

    query = "SELECT * FROM " + input_temp_table
    feature_temp_table = "qwiklabs-gcp-01-df00ef1cf655.credit.credit_feature_temp"
    
    #Load the data from Bigquery based on given query
    client = bigquery.Client(location="us-central1", project=project_id)
    load_job = client.query(query) 
    df = load_job.to_dataframe()
    
    '''Perform feature engineering here'''
    df.dropna(inplace=True)
    
    
    #Upload the batch data to a temporary table
    client.load_table_from_dataframe(dataframe= df, destination=feature_temp_table)
    feature_temp_table_uri = "bq://" + feature_temp_table
    return feature_temp_table_uri

