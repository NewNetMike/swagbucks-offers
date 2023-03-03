class Database:
    def __init__(self, connection):
        self.connection = connection
        self.init()

    def init(self):
        cursor = self.connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Swagbucks(
        SBID TEXT
        )''')
        self.connection.commit()

    def getSB(self, SBID):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Swagbucks WHERE SBID=%s", (SBID,))
        rows = cursor.fetchall()
        if len(rows) > 0:
            return rows[0]
        else:
            return []

    def saveSB(self, SBID):
        cursor = self.connection.cursor()
        sql = ''' INSERT INTO Swagbucks(SBID)
          VALUES(%s) '''
        cursor.execute(sql, (SBID,))
        self.connection.commit()