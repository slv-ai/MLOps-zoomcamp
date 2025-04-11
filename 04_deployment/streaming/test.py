import lambda_function
event ={
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49662255557763068820621213448783501988434282262086811650",
                "data": "ewogICAgInJpZGUiOiB7CiAgICAgICJQVUxvY2F0aW9uSUQiOiAxMzAsCiAgICAgICJET0xvY2F0aW9uSUQiOiAyMDUsCiAgICAgICJ0cmlwX2Rpc3RhbmNlIjogMy42NgogICAgfSwKICAgICJyaWRlX2lkIjogMTIzCiAgfQ==",
                "approximateArrivalTimestamp": 1744331662.366
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49662255557763068820621213448783501988434282262086811650",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::585768144809:role/lambda-kinesis-role",
            "awsRegion": "us-east-1",
            "eventSourceARN": "arn:aws:kinesis:us-east-1:585768144809:stream/ride_events"
        }
    ]
}


result=lambda_function.lambda_handler(event,None)
print(result)
