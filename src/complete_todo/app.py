import boto3
from datetime import datetime

client = boto3.resource("dynamodb")
table = client.Table("Todos")

def lambda_handler(event,context):
    params = event.get("pathParameters")

    item_id = params.get("item_id")

    table.update_item(
        Key = {
            'item_id': item_id
        },
        UpdateExpression = 'set isDone= :r, updated_date= :s',
        ExpressionAttributeValues = {
            ':r':True,
            ':s':datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }
    )


    return {'statusCode':200, 'body':f'todo marked completed for item_id:{item_id}'}
