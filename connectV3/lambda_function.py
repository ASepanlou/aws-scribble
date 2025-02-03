import redis
import boto3

redis_client = redis.Redis(host="scribblev3cache-kblgzn.serverless.use1.cache.amazonaws.com", port=6379, decode_responses=True, ssl=True)
sqs = boto3.client("sqs")

def lambda_handler(event, context):
    connectionId = event["requestContext"]["connectionId"]
    redis_client.lpush("connections", connectionId)
    sqs.send_message(QueueUrl="https://sqs.us-east-1.amazonaws.com/248189920963/catchUpQueueV3", MessageBody=connectionId)
    return { "statusCode" : 200 }
