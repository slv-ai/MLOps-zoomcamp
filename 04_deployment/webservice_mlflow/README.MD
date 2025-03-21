## Here, using locally hosted sqlite database for tracking server and s3 bucket for artifact storage

STEPS:
1.Install aws CLI:
  ```
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip awscliv2.zip
  sudo ./aws/install
  aws --version
2.aws configure --profile
  AWS Access Key ID [None]:
  AWS Secret Access Key [None]: 
  Default region name [None]:
  Default output format [None]
3.list s3 bucket:
  ```
   aws s3 ls --profile
4. Run the following to start mlflow tracking server
```
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root s3://mlflow-models-slv/

5.To verify the port
```
sudo lsof -i :5000
#to remove port
```
 sudo kill -9
 