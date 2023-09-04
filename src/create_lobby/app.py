import json
import os
import boto3
import uuid

def create_lobby(table_name, name, max_player_count):
    """
    Parameters
    ----------
    table_name: string, required
        Name of the DynamoDB table used as the data store for lobbies
        
    name: string, required
        Name of the lobby
        
    maxPlayerCount: number, required
        Maximum player capacity of the lobby

    Returns
    -------
    string lobbyID, used to reference the newly created lobby
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    lobby_id = str(uuid.uuid4())
    table.put_item(
        Item={
            'id': lobby_id,
            'name': name,
            'status': 'Waiting for players',
            'playerCount': 0,
            'maxPlayerCount': max_player_count
        }
    )
    return lobby_id


def lambda_handler(event, context):
    """
    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format. Required fields: name, string; maxPlayerCount, number

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
    max_player_count = int(event.get('maxPlayerCount'))
    lobby_name = event.get('name')
    if lobby_name is None:
        raise ValueError("No lobby name specified!")
    
    lobby_id = create_lobby(table_name, lobby_name, max_player_count)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*"
        },
        "body": json.dumps({ 'lobbyID': lobby_id }, default=str),
    }
