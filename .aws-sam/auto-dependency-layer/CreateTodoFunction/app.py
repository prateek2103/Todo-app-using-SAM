import json
import boto3
import uuid
from datetime import datetime

client = boto3.resource('dynamodb')
table = client.Table('Todos')

def lambda_handler(event, context):
    body = json.loads(event.get('body'))

    item_id = str(uuid.uuid1())
    table.put_item(
        Item={
            'item_id': item_id,
            'title': body.get('title'),
            'content': body.get('content'),
            'created_date': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            'updated_date': None,
            'is_archived': False,
            'is_deleted': False,
            'is_done': False
        }
    )

    return {"statusCode":201, "body":f"todo added successfully with id:{item_id}"}