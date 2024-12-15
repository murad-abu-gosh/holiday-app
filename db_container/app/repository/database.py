from abc import ABC, abstractmethod
from typing import List, Any
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


class DatabaseInterface(ABC):
    @abstractmethod
    def insert_many(self, collection: str, documents: List[dict]) -> None:
        pass

    @abstractmethod
    def find(self, collection: str, query: dict) -> List[Any]:
        pass

    @abstractmethod
    def exists(self, collection: str, query: dict) -> bool:
        pass


class Database(DatabaseInterface):
    def __init__(self, region: str):
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        self.table_name = 'holidays'
        self._ensure_table_exists()
        print(f"Connected to DynamoDB in region: {region}")

    def _ensure_table_exists(self) -> None:
        try:
            # Try to get the table
            table = self.dynamodb.Table(self.table_name)
            table.table_status
            print(f"Table {self.table_name} exists")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                self._create_table()
            else:
                raise e

    def _create_table(self) -> None:
        try:
            table = self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {
                        'AttributeName': 'country',
                        'KeyType': 'HASH'  # Partition key
                    },
                    {
                        'AttributeName': 'date',
                        'KeyType': 'RANGE'  # Sort key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'country',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'date',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            # Wait until the table exists
            table.meta.client.get_waiter('table_exists').wait(TableName=self.table_name)
            print(f"Created table {self.table_name}")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print(f"Table {self.table_name} already exists")
            else:
                raise e

    def _get_table(self, collection: str):
        return self.dynamodb.Table(collection)

    def insert_many(self, collection: str, documents: List[dict]) -> None:
        if not documents:
            return

        table = self._get_table(collection)
        with table.batch_writer() as batch:
            for document in documents:
                batch.put_item(Item=document)
        print(f"Inserted {len(documents)} documents into {collection}")

    def find(self, collection: str, query: dict) -> List[dict]:
        table = self._get_table(collection)
        filter_expression = None
        key_condition_expression = None

        # Handle different query conditions
        for key, value in query.items():
            if key == 'country':
                key_condition_expression = Key('country').eq(value)
            elif key == 'month':
                if filter_expression:
                    filter_expression = filter_expression & Attr('month').eq(value)
                else:
                    filter_expression = Attr('month').eq(value)

        kwargs = {}
        if key_condition_expression:
            kwargs['KeyConditionExpression'] = key_condition_expression
        if filter_expression:
            kwargs['FilterExpression'] = filter_expression

        response = table.query(**kwargs) if key_condition_expression else table.scan(**kwargs)
        return response.get('Items', [])

    def exists(self, collection: str, query: dict) -> bool:
        results = self.find(collection, query)
        return len(results) > 0