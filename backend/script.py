import sqlite3

db = sqlite3.connect('./db/sites.db')
next = sqlite3.connect('./db.sqlite3')
db.row_factory = sqlite3.Row
cur = db.cursor()
ncur = next.cursor()

# Fetching all site IDs
site_list = list(cur.execute('SELECT id FROM sites'))
ncur.execute('CREATE TABLE paths(id NOT NULL AUTOINCREMENT, start, end, length, FOREIGN KEY(start))')
for s, site in enumerate(site_list):
    if s > 0:
        cur.execute('INSERT INTO paths(start, end, length, url) VALUES(?, ?, ?, ?)', (site_list[s-1]['id'], site['id'], site['id'], 'https://www.youtube.com/watch?v=wDchsz8nmbo'))
    else:
        # For the first entry, use s+1 instead of s-1 for the previous site ID
        cur.execute('INSERT INTO paths(start, end, length, url) VALUES(?, ?, ?, ?)', (site['id'], site['id'], site['id'], 'https://www.youtube.com/watch?v=wDchsz8nmbo'))

# Commit changes to the database
db.commit()
db.close()
