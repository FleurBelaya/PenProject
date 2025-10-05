import sqlite3

conn = sqlite3.connect('articles.db')
cur = conn.cursor()

cur.execute('DELETE FROM articles')
conn.commit()
conn.close()
