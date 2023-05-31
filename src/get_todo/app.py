import boto3
import json

client = boto3.resource("dynamodb")
table = client.Table("Todos")

def lambda_handler(event, context):
    path_param = event.get('pathParameters')
    item_id = path_param.get('item_id')

    result = table.get_item(Key = {"item_id": item_id })

    return {"statusCode": 200, "body": json.dumps(result['Item'])}