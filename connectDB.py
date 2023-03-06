import mysql.connector


class connectDB:
    def __init__(self, client_ID):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.DB = "netproject1"
        self.servername = "server"+client_ID
        self.serverID = int(client_ID)


    def connectDatabase(self):
        db = mysql.connector.connect(
    host= self.host,
    user= self.user,
    password= self.password,
    database= self.DB
    )
        return db
    
    def createTable(self):
        db  = self.connectDatabase()
        command = db.cursor()
        command.execute("create table if not exists "+self.servername+" (publisher_ID int not null, time varchar(256) not null, humidity float not null, temperature float not null, thermalarray varchar(256) not null, primary key(publisher_id, time))")

    def insertInto(self,time,humidity,temperature,thermal):
        db  = self.connectDatabase()
        command = db.cursor(prepared=True)
        #If Not Exists*/(select * from "+self.servername+" where time = '"+time+"') 
        #command.execute("insert into "+self.servername+" (publisher_ID,time,humidity,temperature,thermalarray) values ("+(self.serverID)+", '"+time+"', "+(humidity)+", "+(temperature)+" , '"+thermal+"')")
        query = "INSERT INTO " + self.servername + " VALUES (%s, %s,%s, %s,%s)"
        values = (self.serverID, time, humidity, temperature, thermal)
        command.execute(query, values)
        db.commit()

    def printAllData(self):
        db = self.connectDatabase()
        command = db.cursor(prepared=True)

