import os
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv

load_dotenv()


class DBConnection:
    _instance= None
    def __new__(cls):
        if cls._instance is None:
            cls._instance=super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def __init__(self):
        if self._connection is None:
            try:
                self._connection=psycopg2.connect(
                    database=os.getenv("DB_NAME"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    port=os.getenv("DB_PORT"),
                    host=os.getenv("DB_HOST"),
                    )
                self._connection.autocommit = True

            except Exception as e:
                print(e)
                self._connection=None

    def get_connection(self):
        return self._connection

    def execute_query(self, query, params=None):
        try:
            with self._connection.cursor() as cursor:
                results= cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            print(e)

        finally:
            cursor.close()

    def close_connection(self):
        self._connection.close()
        self._connection=None