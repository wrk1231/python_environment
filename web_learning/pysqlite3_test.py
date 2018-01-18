import sqlite3
conn = sqlite3.connect('My1st.db')
cusor = conn.cursor()
cusor.execute("select * from DEPARTMENT")
conn.commit()
value = cusor.fetchall()
print value