import boto3
import json

client = boto3.resource("s3")
bucket = client.Bucket("todo-list-archive-bucket-cb")


def lambda_handler(event, context):
    archives = []

    for archive_item in bucket.objects.all():
        archives.append(archive_item.key)

    return {"statusCode":200, "body":json.dumps(archives)}
