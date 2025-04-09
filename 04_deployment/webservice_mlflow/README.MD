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

 6. generate pipfile and `pipfile.lock:
 pipenv install scikit-learn==1.0.2 flask --python=3.9  gunicorn mlflow boto3





7.Activate the virtual environment

    pipenv shell

8.Creating a script with Flask for prediction and test files. Run the test.py

    python test.py

9.Since WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead., install gunicorn

    gunicorn --bind=0.0.0.0:9696 predict:app

10.Creating a script in gunicorn for prediction and test files. Run the test.py

    python test.py

11.Lauch subshell in virtual environment

    pipenv shell
12. Install dev dependency

    `pipenv install --dev requests`
13.Write down a Dockerfile.

    Build docker image. docker build -t ride-duration-prediction-service:v1 .

14.Run docker image

    docker run -it --rm -p 9696:9696  ride-duration-prediction-service:v1


 