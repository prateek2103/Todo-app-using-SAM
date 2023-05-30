import json

import boto3
from datetime import datetime

client = boto3.resource("dynamodb")
table = client.Table("Todos")

def lambda_handler(event, context):
    body = json.loads(event.get('body'))
    item_id = body.get('item_id')

    table.update_item(
        Key ={
            'item_id': item_id
        },
        UpdateExpression = "set title=:t , content=:c, updated_date=:d",
        ExpressionAttributeValues={
            ':t': body.get("title"),
            ':c': body.get("content"),
            ':d': datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        },  
    )

    return {"statusCode":200, 'body':f"todo successfully updated for item_id : {item_id}"}   