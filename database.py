from PyQt5 import QtCore, QtSql
from pathlib import Path

class Database(object):
    def __init__(self):
        super(Database, self).__init__()
        self.db = None

    def open(self, pathName):
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        p = Path(pathName)
        dbExists = p.is_file()

        self.db.setDatabaseName(pathName)

        if self.db.open():
            if dbExists:
                print("Database open")
            else:
                # TODO: Create the database, and all tables
                print("Database {} does not exist.".format(pathName))
        else:
            print("Error: could not open database.")

    def close(self):
        self.db.close()