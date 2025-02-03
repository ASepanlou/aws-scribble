import boto3
from redis.cluster import RedisCluster
import io
from PIL import Image

s3 = boto3.client("s3")
redis_client = RedisCluster(host="scribblev3cache-kblgzn.serverless.use1.cache.amazonaws.com", port=6379, decode_responses=False, ssl=True)

def lambda_handler(event, context):
    image = Image.new("1", (1000,1000))
    output = io.BytesIO()
    image_str = redis_client.get("map")
    bin_rep = [format(i, '#010b')[2:] for i in image_str]
    flattened = list(''.join(bin_rep))
    flattened = [(int(i) + 1) % 2 for i in flattened]
    flattened = flattened + ([1] * (1000*1000 - len(flattened)))
    image.putdata(flattened)
    image.save(output, format="PNG")
    s3.put_object(Body=output.getvalue(), Bucket="scribblev3", Key="image.png", ACL="public-read")

    return { "statusCode": 200  }