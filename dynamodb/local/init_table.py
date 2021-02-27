import boto3

endpoint_url = "http://dynamodb:8000"
table_name_suffix = "-local"

dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint_url)

for table in dynamodb.tables.all():
    table.delete()

dynamodb.create_table(
    TableName="User" + table_name_suffix,
    AttributeDefinitions=[
        {
            "AttributeName": "UserId",
            "AttributeType": "S",
        },
    ],
    KeySchema=[
        {
            "AttributeName": "UserId",
            "KeyType": "HASH",
        },
    ],
    BillingMode="PAY_PER_REQUEST",
)

dynamodb.create_table(
    TableName="Session" + table_name_suffix,
    AttributeDefinitions=[
        {
            "AttributeName": "SessionId",
            "AttributeType": "S",
        },
    ],
    KeySchema=[
        {
            "AttributeName": "SessionId",
            "KeyType": "HASH",
        },
    ],
    BillingMode="PAY_PER_REQUEST",
)

dynamodb.create_table(
    TableName="Item" + table_name_suffix,
    AttributeDefinitions=[
        {
            "AttributeName": "UserId",
            "AttributeType": "S",
        },
        {
            "AttributeName": "CreatedAt",
            "AttributeType": "S",
        },
    ],
    KeySchema=[
        {
            "AttributeName": "UserId",
            "KeyType": "HASH",
        },
        {
            "AttributeName": "CreatedAt",
            "KeyType": "RANGE",
        },
    ],
    BillingMode="PAY_PER_REQUEST",
)
