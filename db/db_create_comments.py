import sqlite3

conn = sqlite3.connect('test.db')
print "Opened database successfully";
c = conn.cursor()

c.execute(
    '''
    CREATE TABLE COMMENTS
    (ID INTEGER PRIMARY KEY   AUTOINCREMENT,
     IP     TEXT    NOT NULL,
     COMMENT TEXT   NOT NULL,
     DATE_CREATED datetime default current_timestamp
    );
    ''')

print "Table created successfully";
conn.commit()
conn.close()