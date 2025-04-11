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
