import sqlite3

#This class contains sql queries to check the data in the database 

class Checkdata:

    # the constructor prints the data present in the database 

    def __init__(self):
        self.conn = sqlite3.connect('students_attendance.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM attendance")
        results=self.c.fetchall()
        print(results)
        self.conn.close()

#check is the object for the Checkdata class 

check=Checkdata()


