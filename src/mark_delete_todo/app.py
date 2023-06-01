import boto3

sqs = boto3.client('sqs')
ssm = boto3.client('ssm')

def get_queue_url(parameter_name):
    response = ssm.get_parameter(
        Name=parameter_name,
        WithDecryption=False
    )

    return response['Parameter']['Value']

def lambda_handler(event, context):

    # get the queue name
    queue_url = get_queue_url('/todolist/deletequeue/url')

    #get the item id
    params = event.get('pathParameters')
    item_id = params.get('item_id')
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=item_id
    )

    return {"statusCode": 200, "body": f'{item_id} marked as delete successfully'}