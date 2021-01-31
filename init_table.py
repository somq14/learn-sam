import boto3

dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

dynamodb.create_table(
    TableName="DynamoDBTable",
    AttributeDefinitions=[
        {
            'AttributeName': 'PK',
            'AttributeType': 'S',
        },
        {
            'AttributeName': 'SK',
            'AttributeType': 'S',
        }
    ],
    KeySchema=[
        {
            'AttributeName': 'PK',
            'KeyType': 'HASH',
        },
        {
            'AttributeName': 'SK',
            'KeyType': 'RANGE',
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10,
    },
)
