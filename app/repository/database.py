from abc import ABC, abstractmethod
from typing import List, Any


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
    def __init__(self, uri: str, db_name: str):
        from pymongo import MongoClient
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        print(f"Connected to database: {db_name}")

    def insert_many(self, collection: str, documents: List[dict]) -> None:
        if documents:
            self.db[collection].insert_many(documents)
            print(f"Inserted {len(documents)} documents into {collection}")

    def find(self, collection: str, query: dict) -> List[dict]:
        return list(self.db[collection].find(query, {'_id': 0}))

    def exists(self, collection: str, query: dict) -> bool:
        return self.db[collection].count_documents(query) > 0
