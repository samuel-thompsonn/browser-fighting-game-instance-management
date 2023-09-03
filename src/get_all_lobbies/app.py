import json
import os
import boto3
import random


def lambda_handler(event, context):
    """
    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

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
    
    # TODO: Find a better way to assign non-clashing IDs
    item_id = random.randrange(100000000)

    # dynamodb = boto3.resource('dynamodb')
    # table = dynamodb.Table(table_name)
    # table.put_item(
    #     Item={
    #         'ID': f"{item_id}"
    #     }
    # )

    response_data = [
        {
            "id": 3,
            "name": "Placeholder lobby name",
            "status": "Waiting for players",
            "playerCount": 1,
            "maxPlayerCount": 2
        },
        {
            "id": 7,
            "name": "Placeholder lobby name 2",
            "status": "In-Game",
            "playerCount": 2,
            "maxPlayerCount": 2
        }
    ]

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*"
        },
        "body": json.dumps(response_data),
    }
