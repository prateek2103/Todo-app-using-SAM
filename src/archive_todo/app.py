import boto3
from datetime import datetime
from botocore.exceptions import ClientError
import json

# intialize resources
s3_client = boto3.client('s3')
dynamodb_client = boto3.resource('dynamodb')
dynamodb_table = dynamodb_client.Table('Todos')

# method to prepare the archive object for s3
def prep_archive_content(item_id, response):
    with open(f'/tmp/{item_id}.csv', 'w') as archive:

        # write csv header
        archive.write("Item Id,Title,Content,Created,Updated,Archived,Deleted,Complete,Archived Date\n")

        item = response['Item']
        entry = f"{item_id},{item['title']},{item['content']},{item['created_date']},{item['updated_date']},{'True'},{item['is_deleted']},{item['is_done']},{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
        archive.write(entry)

# mark the item archived in DB
def mark_item_archived(item_id, dynamodb_table):
    response = dynamodb_table.update_item(
        Key={
            'item_id': item_id
        },
        UpdateExpression="set is_archived=:a, updated_date=:u",
        ExpressionAttributeValues={
            ':a': True,
            ':u': datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        },
        ReturnValues="UPDATED_NEW"
    )
    return response

# main function
def lambda_handler(event, context):
    path_param = event.get('pathParameters')
    item_id = path_param.get('item_id') 

    try:
        # fetching todo item from dynamodb table first
        response = dynamodb_table.get_item(Key={'item_id': item_id})

        prep_archive_content(item_id, response)

        # upload file to S3
        try:
            s3_client.upload_file(f'/tmp/{item_id}.csv', "todo-list-archive-bucket", f"{item_id}.csv")
        except ClientError as ex:
            return {'statusCode': 502, 'body': f'Error archiving todo: {ex}'}

        # mark the item archived in db
        try:
            mark_item_archived(item_id, dynamodb_table)
        except ClientError as ex:
            return {'statusCode': 502, 'body': f"Error archiving todo: {ex}"}

        return {
            'statusCode': 200,
            'body': f"successfully archived item: {item_id}"
        }
    
    except ClientError as e:
        return { 'statusCode': 502, 'body': f"Error: {e}"}