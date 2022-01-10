import pymysql
import pymongo

class initDatabase:
    def __init__(self):
        self.dbSQL = '127.0.0.1'
        self.usernameSQL = 'root'
        self.passwdSQL = 'root'
        self.dbMongo = '127.0.0.1'
        self.portMongo = '27017'

    def initSQL(self):
        self.conn = pymysql.connect(host=self.dbSQL, user=self.usernameSQL, password=self.passwdSQL)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE DATABASE IF NOT EXISTS facebook; """)
        self.cur.execute("""USE facebook;""")
        table_users1 = """
                            CREATE TABLE IF NOT EXISTS
                                User(
                                    User_id BIGINT PRIMARY KEY,
                                    Username text,
                                    Page text,
                                    Personality text,
                                    FGroup text
                                );
                            """
        self.cur.execute(table_users1)

        return self.cur

    def initMongoDB(self):
        self.conn = pymongo.MongoClient(f"mongodb://{self.dbMongo}:{self.portMongo}/")
        return self.conn

    def writeMongoDB(self,x):
        assert len(x)>0
        if len(x) > 1:
            pass
        else:
            pass





