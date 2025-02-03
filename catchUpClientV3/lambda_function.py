import json
import redis
import boto3

redis_client = redis.Redis(host="scribblev3cache-kblgzn.serverless.use1.cache.amazonaws.com", port=6379, decode_responses=True, ssl=True)
client = boto3.client('apigatewaymanagementapi', endpoint_url="https://lmjcc8llz2.execute-api.us-east-1.amazonaws.com/production/")

def lambda_handler(event, context):
    messages = event["Records"]
    recent_pixels = redis_client.scan_iter(match="*;*")
    for message in messages:
        connectionId = message["body"]
        for coords in recent_pixels:
            x, y = coords.split(";")
            try:
                client.post_to_connection(ConnectionId=connectionId, Data=json.dumps({"x": x, "y": y}).encode('utf-8'))
            except client.exceptions.GoneException:
                redis_client.lrem("connections", 0, connectionId)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
