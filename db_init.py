import sqlite3

con = sqlite3.connect("vpn.db")

cur = con.cursor()

cur.execute("""
    CREATE TABLE Configs
        (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            isDelete INTEGER DEFAULT 0,
            isActive INTEGER DEFAULT 1,
            fileName TEXT DEFAULT "",
            fileId TEXT DEFAULT "",
            nameClient TEXT
        );
""")

con.commit()

cur.close()
con.close()