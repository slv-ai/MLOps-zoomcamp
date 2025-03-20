## Here, using locally hosted sqlite database for tracking server and s3 bucket for artifact storage

STEPS:
1.Install aws CLI:

  `
  curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
  sudo installer -pkg AWSCLIV2.pkg -target /

2.aws configure
   1). Check configure list if the credential is already set, `aws configure list`
   2). (optional) If it does not, and shows as follows, set the `config` file.
  - AWS Access Key ID [None]: The access key id from IAM 
  - AWS Secret Access Key [None]: The Secret key id from IAM
  - default region name should be the similar format as: `ca-central-1`
 aws s3 ls <target> --recursive shows the history of all uploaded files
pip install mlflow

pip install boto3 s3fs

mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root s3://mlflow-models-slv/
