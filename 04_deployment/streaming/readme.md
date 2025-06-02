# aws lambda 
### 1.create a simple lambda funtion with a test event to test
```
import json

def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features
def predict(features):
    return 10.0
def lambda_handler(event, context):
    ride=event['ride']
    ride_id=event['ride_id']
    features=prepare_features(ride)
    prediction=predict(features)
    return {
        'ride_duration': prediction,
        'ride_id': ride_id
    }
````

```
{
  "ride":{
    "PULocationID": 130,
    "DOLocationID": 205,
    "trip_distance": 3.66
  },
  "ride_id":123
}
```

### aws kinesis-

create a simple kinesis stream for test
(ride_events-stream name)
(1-ride id)
`````bash
KINESIS_STREAM_INPUT=ride_events
aws kinesis put-record \
    --stream-name ${KINESIS_STREAM_INPUT} \
    --partition-key 1 \
    --data "Hello,this is a test"
`````
````
{
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49662250773985614793419391233323513470228380249627820034",
                "data": "Hellothisisatest",
                "approximateArrivalTimestamp": 1744319536.253
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49662250773985614793419391233323513470228380249627820034",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::585768144809:role/lambda-kinesis-role",
            "awsRegion": "us-east-1",
            "eventSourceARN": "arn:aws:kinesis:us-east-1:585768144809:stream/ride_events"
        }
    ]
}

```````
### 2.now change the data for kinesis stream to test
````
import json
import base64

def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features
def predict(features):
    return 10.0
def lambda_handler(event, context):
    #ride=event['ride']
    #ride_id=event['ride_id']
    #features=prepare_features(ride)
    #prediction=predict(features)
    print(json.dumps(event))
    for record in event['Records']:
        encoded_data=record['kinesis']['data']
        decoded_data=base64.b64decode(encoded_data).decode('utf-8')
        ride_event=json.loads(decoded_data)
        print(ride_event)
    prediction=10.0
    ride_id=123
    return {
        'ride_duration': prediction,
        'ride_id': ride_id
    }
``````

````bash
KINESIS_STREAM_INPUT=ride_events

# Send the JSON payload, base64-encoded
aws kinesis put-record \
  --stream-name "$KINESIS_STREAM_INPUT" \
  --partition-key 1 \
  --data "$(echo -n '{
    "ride": {
      "PULocationID": 130,
      "DOLocationID": 205,
      "trip_distance": 3.66
    },
    "ride_id": 123
  }' | base64)"

`````
### 3.create another data stream
## lambda.py
``````
import json
import os
import boto3
import base64
kinesis_client = boto3.client('kinesis')

PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME', 'ride_predictions')


def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features

def predict(features):
    return 10.0


def lambda_handler(event, context):
    predictions_events = []
    
    for record in event['Records']:
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        ride_event = json.loads(decoded_data)

        ride = ride_event['ride']
        ride_id = ride_event['ride_id']
    
        features = prepare_features(ride)
        prediction = predict(features)
        

        prediction_event = {
            'model': 'ride_duration_prediction_model',
            'version': '123',
            'prediction': {
                'ride_duration': prediction,
                'ride_id': ride_id
            }
        }
        print(json.dumps(prediction_event))

        kinesis_client.put_record(
                StreamName=PREDICTIONS_STREAM_NAME,
                Data=json.dumps(prediction_event),
                PartitionKey=str(ride_id)
            )
        predictions_events.append(prediction_event)



    return {
        'prediction': predictions_events

    }
`````

### reading from the stream


````bash
KINESIS_STREAM_OUTPUT='ride_predictions'
SHARD='shardId-000000000000'

SHARD_ITERATOR=$(aws kinesis \
    get-shard-iterator \
        --shard-id ${SHARD} \
        --shard-iterator-type TRIM_HORIZON \
        --stream-name ${KINESIS_STREAM_OUTPUT} \
        --query 'ShardIterator' \
)

RESULT=$(aws kinesis get-records --shard-iterator $SHARD_ITERATOR)

echo ${RESULT} | jq -r '.Records[0].Data' | base64 --decode
``````
### Try the recall of the responses
```
echo $SHARD_ITERATOR
echo $RESULT
````


### 4.load model to lambda
edit lambda_function.py and run
```
export PREDICTIONS_STREAM_NAME="ride_predictions"
export RUN_ID="6bf96782bee64c8cadefd3497b0712a1"
export TEST_RUN="True"

python test.py
```
(create a new conda env and install pip install numpy==2.0.2 pandas==2.2.3 scikit-learn==1.6.1 scipy==1.13.1 psutil==5.9.0 boto3 mlflow)run python test.py

## 5.create a docker file
```
pipenv install boto3 mlflow scikit-learn==1.6.1 --python=3.9
```
#use python 3.9 image from aws ecr,Use the standard AWS Lambda Invoke path for the emulator:url = 'http://localhost:8080/2015-03-31/functions/function/invocations'


```
docker build -t stream-model-duration:v1 .

````
```
export AWS_ACCESS_KEY_ID=YOUR_KEY_ID 
export AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION=YOUR_REGION
```
```
docker run -it --rm \
-p 8080:8080 \
-e PREDICTIONS_STREAM_NAME="ride_predictions" \
-e RUN_ID="6bf96782bee64c8cadefd3497b0712a1" \
-e TEST_RUN="True" \
-e AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
-e AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
-e AWS_DEFAULT_REGION="us-east-1" \
stream-model-duration:v1

````
and run python test_docker.py


### 6.push image to AWS-ECR

1.Create a new AWS repo -copy repository uri and paste in REMOTE URI

```
aws ecr create-repository --repository-name duration-model


```
2.Login to ECR

```
aws ecr get-login-password --region <your-region> --profile ml_user | \
docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.<your-region>.amazonaws.com

```
3.Push the docker image to ECR.
````
REMOTE_URI="<paste repository uri here>"
REMOTE_TAG="v1"
REMOTE_IMAGE=${REMOTE_URI}:${REMOTE_TAG}

LOCAL_IMAGE="stream-model-duration:v1"
docker tag ${LOCAL_IMAGE} ${REMOTE_IMAGE}
docker push ${REMOTE_IMAGE}

````
4.Sucessfully uploaded. And check the image
```
 echo $REMOTE_IMAGE
```

### 7.model from docker image
1.Create a new Lambda function, which is from the container image , the container name is ride-duration-predition, and Container image URI is REMOTE_URI
2.Then go to Lambda > Configuration > Environment variables, create Key - value for PREDICTIONS_STREAM_NAME and RUN_ID

Add Kinesis stream created before as trigger for new lambda function. Also delete the previous Lambda function which also used this Kinesis stream.

Creat policy to IAM-rule for s3.
3.test:
run a test event on lambda 

or
send a new record to trigger kinesis stream:
````
KINESIS_STREAM_INPUT=ride-events \ 
aws kinesis put-record \
    --stream-name ${KINESIS_STREAM_INPUT} \
    --partition-key 1 \
   --cli-binary-format raw-in-base64-out \
    --data '{
        "ride": {
            "PULocationID": 130,
            "DOLocationID": 205,
            "trip_distance": 3.66
        }, 
        "ride_id": 156
    }'
````
Ask for the output stream.
````
KINESIS_STREAM_OUTPUT='ride_predictions'
SHARD='shardId-000000000000'

SHARD_ITERATOR=$(aws kinesis \
    get-shard-iterator \
        --shard-id ${SHARD} \
        --shard-iterator-type TRIM_HORIZON \
        --stream-name ${KINESIS_STREAM_OUTPUT} \
        --query 'ShardIterator' \
)

RESULT=$(aws kinesis get-records --shard-iterator $SHARD_ITERATOR)
echo ${RESULT} | jq -r '.Records[0].Data' | base64 --decode
````
result:{"model": "ride_duration_prediction_model", "version": "123", "prediction": {"ride_duration": 10.0, "ride_id": 123}}(base) ubuntu@ip-172-31-38-225:~$

refer:https://github.com/Muhongfan/MLops/blob/main/04-deployment/streaming/README.md
