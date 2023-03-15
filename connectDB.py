import mysql.connector


class connectDB:
    def __init__(self, client_ID):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.DB = "netproject1"
        self.servername = "server"+client_ID
        self.serverID = int(client_ID)

    #Connect to database
    def connectDatabase(self):
        db = mysql.connector.connect(
    host= self.host,
    user= self.user,
    password= self.password,
    database= self.DB
    )
        return db
    
    #use to create ui and recive input from user
    def ui(self):
        print("This is "+self.servername)
        print("1) print all data")
        print("2) print only humidity")
        print("3) print only temperature")
        print("4) print only thermalarray")
        print("5) print menu again")
        print("6) clsoe server")

    #use to create a table to database if it doesnt exist
    def createTable(self):
        db  = self.connectDatabase()
        command = db.cursor()
        command.execute("create table if not exists "+self.servername+" (publisher_ID int not null, time varchar(256), humidity float, temperature float, thermalarray text, primary key(publisher_id, time))")

    #insert a new data to table (have every elemnts)
    def insertIntoAll(self,time,humidity,temperature,thermal,pubID):
        db  = self.connectDatabase()
        command = db.cursor(prepared=True)
        #If Not Exists(select * from "+self.servername+" where time = '"+time+"') 
        #command.execute("insert into "+self.servername+" (publisher_ID,time,humidity,temperature,thermalarray) values ("+(self.serverID)+", '"+time+"', "+(humidity)+", "+(temperature)+" , '"+thermal+"')")
        query = "INSERT INTO " + self.servername + " VALUES (%s, %s, %s, %s, %s)"
        values = (pubID, time, humidity, temperature, thermal)
        command.execute(query, values)
        db.commit()

    #insert a new data to table (missing some elements)
    def insertIntoNotAll(self,time,thermal,pubID):
        db  = self.connectDatabase()
        command = db.cursor(prepared=True)
        #If Not Exists(select * from "+self.servername+" where time = '"+time+"') 
        #command.execute("insert into "+self.servername+" (publisher_ID,time,humidity,temperature,thermalarray) values ("+(self.serverID)+", '"+time+"', "+(humidity)+", "+(temperature)+" , '"+thermal+"')")
        query = "INSERT INTO " + self.servername + " (publisher_ID,time,thermalarray) VALUES (%s,%s,%s)"
        values = (pubID, time, thermal)
        command.execute(query, values)
        db.commit()


    #print add data
    def printAllData(self):
        db = self.connectDatabase()
        command = db.cursor(prepared=True)
        command.execute("select * from "+self.servername)
        result = command.fetchall()
        for x in result:
            print("Publisher ID :"+str(x[0]))
            print("Time :"+str(x[1]))
            print("Humidity :"+str(x[2]))
            print("Temperature :"+str(x[3]))
            print("Thermalarray :"+str(x[4]))
            print("---------------------------------------------------------------------------")

        self.ui()
    
    #print only humidity
    def printOnlyHum(self):
        db = self.connectDatabase()
        command = db.cursor(prepared=True)
        command.execute("select time, humidity, publisher_ID from "+self.servername)
        result = command.fetchall()
        for x in result:
            print("Publisher ID : " + str(x[2]))
            print("Time :"+str(x[0]))
            print("Humidity :"+str(x[1]))
            print("---------------------------------------------------------------------------")
        self.ui()

    #print only temperature
    def printOnlyTemp(self):
        db = self.connectDatabase()
        command = db.cursor(prepared=True)
        command.execute("select time, temperature, publisher_ID from "+self.servername)
        result = command.fetchall()
        for x in result:
            print("Publisher ID : " + str(x[2]))
            print("Time :"+str(x[0]))
            print("Temperature :"+str(x[1]))
            print("---------------------------------------------------------------------------")
        self.ui()

    #print thermalarray
    def printOnlyThe(self):
        db = self.connectDatabase()
        command = db.cursor(prepared=True)
        command.execute("select time, thermalarray, publisher_ID from "+self.servername)
        result = command.fetchall()
        for x in result:
            print("Publisher ID : " + str(x[2]))
            print("Time :"+str(x[0]))
            print("Thermalarray :"+str(x[1]))
            print("---------------------------------------------------------------------------")
        self.ui()

