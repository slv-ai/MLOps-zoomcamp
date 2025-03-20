STEPS:
pip install mlflow
pip install boto3 s3fs
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root s3://mlflow-models-slv/