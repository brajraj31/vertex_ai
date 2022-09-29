

"""A PySpark program that perform fetaure engineering using spark."""

import argparse
import sys
from pyspark.sql import SparkSession

def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',
                        dest='input',
                        default='qwiklabs-gcp-01-df00ef1cf655.credit.credit_data',
                        help='Input BigQuery table to process.')
    parser.add_argument('--output',
                        dest='output',
                        default='qwiklabs-gcp-01-df00ef1cf655.credit.credit_spark_feature_temp',
                        help='Output BigQuery Table to write results to.')
    
    known_args, _ = parser.parse_known_args(argv)
    
    spark = SparkSession\
            .builder\
            .appName("featureengineering")\
            .getOrCreate()
    
    sc = spark.sparkContext

    # Load data from BigQuery.
    df = spark.read.format('bigquery').option('table', known_args.input).load()
  
    #perform feature engineering here
    df.dropna().show(truncate=False)  

    df.write.format('bigquery').option('table', known_args.output).save()
    
    sc.stop()
    
if __name__ == '__main__':
    run(sys.argv)