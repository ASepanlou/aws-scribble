import json
import boto3
import redis

dynamo_client = boto3.client("dynamodb")
client = boto3.client('apigatewaymanagementapi', endpoint_url="https://lmjcc8llz2.execute-api.us-east-1.amazonaws.com/production/")
redis_client = redis.Redis(host="scribblev3cache-kblgzn.serverless.use1.cache.amazonaws.com", port=6379, decode_responses=True, ssl=True)

def lambda_handler(event, context):
    messages = event["Records"]
    for message in messages:
        x, y = message["body"].split(";")
        idx = int(y)*1000+int(x)
        dynamo_client.put_item(TableName="scribbleV3DB", Item={"idx": {"N": str(idx)}, "x": {"N": str(x)}, "y": {"N": str(y)}})
        connections = redis_client.lrange("connections", 0, -1)
        for connectionId in connections:
            try:
                client.post_to_connection(ConnectionId=connectionId, Data=json.dumps({"x": x, "y": y}).encode('utf-8'))
            except client.exceptions.GoneException:
                redis_client.lrem("connections", 0, connectionId)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
