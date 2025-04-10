# aws lambda 
1.create a simple lambda funtion with a test event to test
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
2.create a simple kinesis stream for test
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
````
import json

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
        print(encoded_data)
    prediction=10.0
    ride_id=123
    return {
        'ride_duration': prediction,
        'ride_id': ride_id
    }
```
3.now change the data for kinesis stream to test
````bash
KINESIS_STREAM_INPUT=ride_events
aws kinesis put-record \
    --stream-name ${KINESIS_STREAM_INPUT} \
    --partition-key 1 \
    --data '{
        "ride":{
            "PULocationID": 130,
            "DOLocationID": 205,
            "trip_distance": 3.66
        },
        "ride_id":123
    }'
`````

## lambda.py
``````
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
    # TODO implement
    print(json.dumps(event))

    for record in event['Records']:
        print(record['kinesis']['data'])
        data=base64.b64decode(record['kinesis']['data']).decode('utf-8')
        print(data)
    prediction=10.0
    ride_id=123
    return {
        'ride_duration': prediction,
        'ride_id': ride_id
    }
