import os
import psycopg2 as pg


class Connector:
    def __init__(self, database, port=5432):
        super().__init__()

        self.conn = pg.connect(
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            host=os.environ.get("DB_HOST"),
            port=port,
            database=database,
        )

        self.cur = self.conn.cursor()

    def reset_connection(self):
        self.__init__()

        return None
