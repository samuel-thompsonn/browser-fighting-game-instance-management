import json
import pytest
import moto
import os
import boto3

from src.instance_allocation.game_start import app

@pytest.fixture()
def mocked_dynamo_db():
    """Generates mock DynamoDB instance"""
    table_name = os.getenv("TABLE_NAME")
    with moto.mock_dynamodb():
        dynamodb = boto3.client("dynamodb")
        dynamodb.create_table(
            TableName = table_name,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode='PAY_PER_REQUEST'
        )
        table = dynamodb.Table(table_name)
        table.put_item(
            Item={
                'id': 'example_id',
            }
        )

@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "lobbyId": "lobbyId",
        "body": '{ "lobbyId": "lobbyId"}',
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": "",
            },
            "stage": "prod",
        },
        "queryStringParameters": {"foo": "bar"},
        "headers": {
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country": "US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Port": "443",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "Accept-Encoding": "gzip, deflate, sdch",
        },
        "pathParameters": {"proxy": "/examplepath"},
        "httpMethod": "POST",
        "stageVariables": {"baz": "qux"},
        "path": "/examplepath",
    }

@moto.mock_aws
def test_lambda_handler(apigw_event):
    mock_ip = 'example ip address'
    table_name = os.getenv("TABLE_NAME")
    dynamodb = boto3.resource("dynamodb")
    dynamodb.create_table(
        TableName = table_name,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode='PAY_PER_REQUEST'
    )
    table = dynamodb.Table(table_name)
    table.put_item(
        Item={
            'id': 'id',
            'lobbyId': None,
            'ip': mock_ip
        }
    )

    ret = app.lambda_handler(apigw_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "ip" in ret["body"]
    assert data["ip"] == mock_ip
