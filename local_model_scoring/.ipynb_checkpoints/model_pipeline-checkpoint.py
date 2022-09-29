import google.cloud.aiplatform as aip
from kfp import dsl
from kfp.v2 import compiler
from kfp import components
import warnings
import get_input_data,feature_engineering,model_scoring


PROJECT_ID = 'qwiklabs-gcp-01-df00ef1cf655'
REGION = "us-central1"
BUCKET_NAME = "gs://vaibucket"
PIPELINE_ROOT = "{}/pipeline_root".format(BUCKET_NAME)
BASE_IMAGE = "python:3.9"


#Create Pipeline
@dsl.pipeline(
  name='localbatchscoringpipeline',
  description='This pipeline is intend to perform batch scoring.'
)

def pipeline(
    query: str = "SELECT * FROM qwiklabs-gcp-01-df00ef1cf655.credit.credit_data LIMIT 100",
    project_id: str = "qwiklabs-gcp-01-df00ef1cf655" ,
    region: str = "us-central1",
    bucket: str = "gs://vaibucket",
    big_query_op: str = "bq://qwiklabs-gcp-01-df00ef1cf655.credit"
):
    #Generate the component
    get_input_data_op = components.create_component_from_func(get_input_data.get_input_data,
                                                base_image=BASE_IMAGE,
                                                packages_to_install=['google-cloud-bigquery[pandas]==2.34.3','pandas'])
        
    feature_engineering_op = components.create_component_from_func(feature_engineering.feature_engineering,
                                                 base_image = BASE_IMAGE,
                                                 packages_to_install=['google-cloud-bigquery[pandas]==2.34.3','pandas'])
    
    model_scoring_op = components.create_component_from_func(model_scoring.batch_model_scoring,
                                                 base_image=BASE_IMAGE,
                                                 packages_to_install=['google-cloud-bigquery[pandas]==2.34.3','pandas',
                                                                      'google-cloud-aiplatform'])
    
    input_data = get_input_data_op(query = query, project_id = project_id)
    feature_data = feature_engineering_op(input_data.output, project_id)
    model_scoring_op(feature_data.output, big_query_op)
    
    
if __name__ == '__main__':
    
    import google.cloud.aiplatform as aip
    aip.init(project= PROJECT_ID, staging_bucket= BUCKET_NAME)
    
    pipeline_export_filepath = 'test-pipeline.json'
    compiler.Compiler().compile(pipeline_func=pipeline,
                                package_path=pipeline_export_filepath)
    job = aip.PipelineJob(
        display_name="scoring_pipeline_3",
        template_path=pipeline_export_filepath,
        pipeline_root=PIPELINE_ROOT,
        enable_caching = False
    )
    
    job.run()