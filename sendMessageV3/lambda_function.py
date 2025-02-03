import json
import boto3
import redis

client = boto3.client('apigatewaymanagementapi', endpoint_url="https://1eo8hw4vk6.execute-api.us-east-1.amazonaws.com/production/")
redis_client = redis.Redis(host="v4valkey-kblgzn.serverless.use1.cache.amazonaws.com", port=6379, decode_responses=True, ssl=True)
sqs = boto3.client("sqs")

def lambda_handler(event, context):
    body = json.loads(event["body"])
    responseMessage = body["message"]
    x = responseMessage["x"]
    y = responseMessage["y"]
    x = int(x) if int(x) <= 999 else 999
    y = int(y) if int(y) <= 999 else 999
    thisconnect = event["requestContext"]["connectionId"]
    client.post_to_connection(ConnectionId=thisconnect, Data=json.dumps({"x": x, "y": y}).encode('utf-8'))
    idx = y*1000+x
    redis_client.setbit("map", idx, 1)
    redis_client.setnx(str(x)+";"+str(y), 1)
    redis_client.expire(str(x)+";"+str(y), 120)
    sqs.send_message(QueueUrl="https://sqs.us-east-1.amazonaws.com/248189920963/scribbleV4Queue", MessageBody=str(x)+";"+str(y))

    return { "statusCode": 200  }