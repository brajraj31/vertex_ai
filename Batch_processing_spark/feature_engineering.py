'''This model is use to get input data from different resources'''


def feature_engineering(input_temp_table: str
                        , project_id: str) -> str:

    from google.cloud import bigquery
    from google_cloud_pipeline_components.experimental.dataproc import \
        DataprocPySparkBatchOp
    import pandas
    import os

    
    _ = DataprocPySparkBatchOp(
        project=project_id,
        location="us-central1",
        main_python_file_uri=main_python_file_uri,
        args = args
    )


