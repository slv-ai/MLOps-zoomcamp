## Here, using locally hosted sqlite database for tracking server and s3 bucket for artifact storage

STEPS:
pip install mlflow

pip install boto3 s3fs

mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root s3://mlflow-models-slv/
