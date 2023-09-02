import json

# import requests
import os
import boto3
import random


def lambda_handler(event, context):
    """Sample pure Lambda function

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
    
    item_id = random.randrange(100000000)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    table.put_item(
        Item={
            'ID': f"{item_id}"
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"New element in table: {item_id}",
            # "location": ip.text.replace("\n", "")
        }),
    }
