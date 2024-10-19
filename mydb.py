import sqlite3

class Database:
    def __init__(self, db):
        self.db_file = db

    def fetchRecord(self, query):
     conn = sqlite3.connect(self.db_file)
     cur = conn.cursor()
     cur.execute(query)
     rows = cur.fetchall()
     conn.close()
     return rows


    def fetchDistinctCategories(self):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT category FROM expense_record")
        rows = cur.fetchall()
        conn.close()
        return [row[0] for row in rows]

    def insertRecord(self, item_name, item_price, purchase_date, category):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute("INSERT INTO expense_record (item_name, item_price, purchase_date, category) VALUES (?, ?, ?, ?)",
                    (item_name, item_price, purchase_date, category,))
        conn.commit()
        conn.close()

    def removeRecord(self, rowid):
        conn = sqlite3.connect(self.db_file)
        conn.execute("DELETE FROM expense_record WHERE rowid=?", (rowid,))
        conn.commit()
        conn.close()

    def updateRecord(self, item_name, item_price, purchase_date, category, rowid):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute("UPDATE expense_record SET item_name=?, item_price=?, purchase_date=?, category=? WHERE rowid=?",
                    (item_name, item_price, purchase_date, category, rowid))
        conn.commit()
        conn.close()
