import boto3
import json

client = boto3.resource("dynamodb")
table = client.Table("Todos")

def lambda_handler(event, context):
    result = table.scan()


    return {"statusCode":200, "body" : json.dumps(result['Items'])}