import mysql.connector


class connectDB:
    def __init__(self, client_ID):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.DB = "netproject1"
        self.serverID = client_ID

    def connectDB(self):
        db = mysql.connector.connect(
    host= self.host,
    user= self.user,
    password= self.password,
    database= self.DB
    )
        return db
    
    def createTable(self):
        db  = self.connectDB()
        command = db.cursor()
        command.execute("create table if not exists "+self.serverID+" (\
            publisher_id int not null,\
            time timestamp not null,\
            humidity float not null,\
            temperature float not null,\
            thermalarray text not null,\
            primary key(publisher_id,`time`)\
            )")