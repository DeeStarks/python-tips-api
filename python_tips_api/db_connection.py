import psycopg2
from psycopg2 import Error
import environ
from django.core.exceptions import ObjectDoesNotExist

env = environ.Env()
environ.Env.read_env()

class Database:
    def __init__(self):
        self.__connection = None
        self.__cursor = None

    def connect_to_db(self):
        # Close the connection if it is already open
        if self.__connection is not None:
            self.close_db_connection()
        try:
            # Connect to an existing database
            connection = psycopg2.connect(
                user=env('DB_USERNAME'),
                password=env('DB_PASSWORD'),
                host="127.0.0.1",
                port="5432",
                database=env('DB_NAME')
            )
            cursor = connection.cursor()
            self.__connection = connection
            self.__cursor = cursor
            # Print PostgreSQL Connection properties
            # print(connection.get_dsn_parameters(), "\n")
            # Print PostgreSQL version
            # cursor.execute("SELECT version();")
            # record = cursor.fetchone()
            # print("You are connected to - ", record, "\n")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def close_db_connection(self):
        self.__connection.close()
        self.__cursor.close()

    def describe_table(self, table_name):
        self.connect_to_db()
        try:
            self.__cursor.execute("SELECT * FROM " + table_name)
            return self.__cursor.description
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            self.close_db_connection()
    
    def execute_query(self, query):
        self.connect_to_db()
        try:
            self.__cursor.execute(query)
            return self.__cursor.fetchall()
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            self.close_db_connection()
        
    def select_table(self, table_name):
        data = []
        table = self.describe_table(table_name)
        table = [col.name for col in table]
        query = "SELECT * FROM " + table_name
        db_data = self.execute_query(query)
        for row in db_data:
            data.append(dict(zip(table, row)))
        # Sorting the data by id - reversed
        data = sorted(data, key=lambda i: i['id'], reverse=True)
        return data

    def select_row(self, table_name, target_column, value):
        data = []
        query = "SELECT * FROM " + table_name + " WHERE " + target_column + " = '" + str(value) + "'"
        table = self.describe_table(table_name)
        table = [col.name for col in table]
        db_data = self.execute_query(query)
        try:
            data.append(dict(zip(table, db_data[0])))
        except IndexError:
            raise ObjectDoesNotExist(f"Tip with '{target_column}' - '{str(value)}' does not exist")
        return data

    def insert_row(self, table_name, data):
        query_ids = "SELECT id FROM " + table_name
        ids = self.execute_query(query_ids)
        last_id = ids[-1][0]
        query = "INSERT INTO " + table_name + " (id, "
        for key, value in data.items():
            query += key + ", "
        query = query[:-2] + ") VALUES ('" + str(last_id+1) + "', "
        for key, value in data.items():
            query += "'" + str(value).replace("'", str('"')) + "', "
        query = query[:-2] + ");"
        self.connect_to_db()
        try:
            self.__cursor.execute(query)
            self.__connection.commit()
            return self.select_row(table_name, 'id', last_id+1)
        except (Exception, psycopg2.Error) as error:
            raise Exception(error)
        finally:
            self.close_db_connection()

    def update_row(self, table_name, target_column, value, column_name, new_value):
        query = "UPDATE " + table_name + " SET " + column_name + " = '" + str(new_value) + "' WHERE " + target_column + " = '" + str(value) + "'"
        self.connect_to_db()
        try:
            self.__cursor.execute(query)
            self.__connection.commit()
        except (Exception, psycopg2.Error) as error:
            raise Exception(error)
        finally:
            self.close_db_connection()

    def delete_row(self, table_name, target_column, value):
        query = "DELETE FROM " + table_name + " WHERE " + target_column + " = '" + str(value) + "'"
        self.connect_to_db()
        try:
            self.__cursor.execute(query)
            self.__connection.commit()
        except (Exception, psycopg2.Error) as error:
            raise Exception(error)
        finally:
            self.close_db_connection()

database = Database()