import sqlite3

conn = sqlite3.connect('test.db')
print "Opened database successfully";
c = conn.cursor()

c.execute(
    '''
    CREATE TABLE XIAOQUGPS
    (XQ     TEXT PRIMARY KEY,
     LAT    TEXT    NOT NULL,
     LON    TEXT   NOT NULL,
     NMB    INTEGER NOT NULL
    );
    ''')

print "Table created successfully";
conn.commit()
conn.close()