import google.cloud.aiplatform as aip
import warnings
import get_input_data,feature_engineering,model_scoring



PROJECT_ID = 'qwiklabs-gcp-01-df00ef1cf655'
REGION = "us-central1"
BUCKET_NAME = "gs://vaibucket"
PIPELINE_ROOT = "{}/pipeline_root".format(BUCKET_NAME)
BIG_QUERY_OP = ""

def scoring():
    
    input_table = get_input_data(query='', project_id = PROJECT_ID)
    feature_table = feature_engineering(input_temp_table=input_table, project_id = PROJECT_ID)
    batch_model_scoring(inputpath=feature_table, outputpath=BIG_QUERY_OP)


if __name__ == '__main__':
    scoring()