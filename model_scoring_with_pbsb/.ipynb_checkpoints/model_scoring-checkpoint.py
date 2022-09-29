

def batch_model_scoring(inputpath:str, outputpath:str) -> str:
    '''Import model and perorm batch scoring'''
    import google.cloud.aiplatform as aip

    model_id = '75325342595678208'
    model = aip.Model(model_name=model_id, project='qwiklabs-gcp-01-df00ef1cf655', location='us-central1')
    response = model.batch_predict(
        job_display_name="batch_scoring_poc",
        #gcs_source=inputpath,
        instances_format='bigquery',
        bigquery_source = inputpath,
        #instances_format="csv",
        bigquery_destination_prefix=outputpath
    )
    
    scored_table = response.output_info.bigquery_output_table
    scored_table_path = str(outputpath) + '.' + str(scored_table)
    
    return scored_table_path
