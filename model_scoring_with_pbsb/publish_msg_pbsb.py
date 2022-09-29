'''This model is use to published scored data from BigQuery to cloud pub/sub topic'''

def publish_msg_pbsb(inputbqpath:str,
                    project_id:str,
                    topic_id:str):
    
    from google.cloud import pubsub_v1
    from google.cloud import bigquery
    inputbqpath = str(inputbqpath[5:])
    query = "SELECT * FROM " + inputbqpath
    print(inputbqpath)
    
    #Load the data from Bigquery based on given query
    client = bigquery.Client(location="us-central1", project=project_id)
    load_job = client.query(query) 
    df = load_job.to_dataframe()
    
    #Convert data from to json string format to create a single message
    message = str(df.T.to_json())
    
    #Publish message to cloud pub/sub topic
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    
    # Data must be a bytestring
    data = message.encode("utf-8")
    future = publisher.publish(
        topic_path, data, origin="python-sample", username="gcp"
    )
    print(future.result())

    
    