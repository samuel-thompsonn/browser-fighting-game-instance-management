import json
import os
import boto3
from boto3.dynamodb.conditions import Attr
import uuid

def allocate_instance(lobby_id, table_name):
    """
    Parameters
    ----------
    lobby_id: string, required
        ID of the lobby to which we must assign an instance
    table_name: string, required
        Name of the DynamoDB table used as the data store for lobbies
        
    Returns
    -------
    instance_ip: IP of the instance, where players will connect in order
    to play a round of the game.
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    scan_response = table.scan(
        FilterExpression=Attr('lobbyId').eq(None)
    )
    if (scan_response['Count'] == 0):
        raise RuntimeError('No available instances')
    selected_instance = scan_response['Items'][0]
    table.update_item(
        Key={ 'id': selected_instance['id'] },
        UpdateExpression="set lobbyId = :lobby",
        ExpressionAttributeValues={ ':lobby': lobby_id },
    )
    return selected_instance['ip']


def lambda_handler(event, context):
    """
    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format. Required fields: lobbyId

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    table_name = os.getenv('TABLE_NAME')
    if table_name is None:
        raise RuntimeError("No target DDB table found!")
    lobby_id = event.get('lobbyId')
    if lobby_id is None:
        raise ValueError("No lobby id specified!")

    ip = allocate_instance(lobby_id, table_name)
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*"
        },
        "body": json.dumps({ 'ip': ip }, default=str),
    }
