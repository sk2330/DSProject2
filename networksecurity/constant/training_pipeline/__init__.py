import os
import numpy as np
import pandas as pd


### some common constants that we use in this project are defined here

TARGET_COLUMN= "Result"
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACT_DIR:str = "Artifact"
FILE_NAME:str = "phisingData.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"
SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

'''
Data Ingestion related configuration start with a DATA_INGESTION VAR name
'''

DATA_INGESTION_COLLECTION_NAME :str = "NetworkData"
DATA_INGESTION_DATABASE_NAME :str ="MongoDbTest"
DATA_INGESTION_DIR_NAME: str ="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

'''
Data Validation related configuration start with a DATA_VALIDATION VAR name
'''

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"


