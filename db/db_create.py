import sqlite3

conn = sqlite3.connect('test.db')
print "Opened database successfully";
c = conn.cursor()
c.execute(
    '''
    CREATE TABLE HOUSE
    (SOURCE           TEXT    NOT NULL,
     URL           TEXT    PRIMARY KEY,
     TITLE           TEXT    NOT NULL,
     USER           TEXT    NOT NULL,
     POST_TIME       DATE    NOT NULL,
     CRAWL_TIME       DATE    NOT NULL
    );
    ''')
print "Table created successfully";
conn.commit()
conn.close()