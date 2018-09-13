import sqlite3

conn = sqlite3.connect('test.db')
print "Opened database successfully";
c = conn.cursor()
c.execute(
    '''
    CREATE TABLE HOUSE
    (SOURCE           TEXT    NOT NULL,
     URL           TEXT    NOT NULL,
     TITLE           TEXT    PRIMARY KEY,
     USER           TEXT    NOT NULL,
     POST_TIME       TIME    NOT NULL,
     CRAWL_TIME       TIME    NOT NULL
    );
    ''')

c.execute(
    '''
    CREATE TABLE VISIT
    (ID INTEGER PRIMARY KEY   AUTOINCREMENT,
     IP     TEXT    NOT NULL,
     VISIT_TIME DATE    NOT NULL
    );
    ''')

print "Table created successfully";
conn.commit()
conn.close()