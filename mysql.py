import os
import mysql.connector as mconn


class Connector:
    def __init__(self, database):
        super().__init__()
        self.database = database

        self.conn = mconn.connect(
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            host=os.environ.get("DB_HOST"),
            database=self.database,
        )
        self.cursor = self.conn.cursor()

    def reset_connection(self):
        self.__init__(self.database)
