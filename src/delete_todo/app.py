import boto3
from datetime import datetime

ssm = boto3.client('ssm')
sqs = boto3.client('sqs')
dbClient = boto3.resource("dynamodb")
table = dbClient.Table("Todos")

def get_queue_url(parameter_name):
    response = ssm.get_parameter(
        Name=parameter_name,
        WithDecryption=False
    )

    return response['Parameter']['Value']

def updateDb(item_id):
    table.update_item(
        Key = {
            'item_id': item_id
        },
        UpdateExpression = "set isDeleted=:t, updated_date=:d",
        ExpressionAttributeValues={
            ':t': True,
            ':d': datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }
    )
    
def lambda_handler(event, context):

    queue_url = get_queue_url("/todolist/deletequeue/url")

    response = sqs.receive_message(
        QueueUrl=queue_url
    )

    count = 0
    if 'Messages' in response:
        messages = response['Messages']
        count = len(messages)
        for message in messages:
            item_id = message['Body']
            updateDb(item_id)
        
        receipt_handle = message['ReceiptHandle']

        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )

    return f"deletion executed successfully for {count} messages"