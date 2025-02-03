import redis

redis_client = redis.Redis(host="scribblev3cache-kblgzn.serverless.use1.cache.amazonaws.com", port=6379, decode_responses=True, ssl=True)

def lambda_handler(event, context):
    connectionId = event["requestContext"]["connectionId"]
    redis_client.lrem("connections", 0, connectionId)
    return { "statusCode" : 200 }
