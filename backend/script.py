import sqlite3
import sys

def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == 'fix':
            fix_urls()
        else:
            add_site(sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[1] == 'tag':
        add_tag(sys.argv[2])
    elif len(sys.argv) == 3:
        add_path(sys.argv[1], sys.argv[2])

def connect():
    db = sqlite3.connect('./db.sqlite3')
    db.row_factory = sqlite3.Row
    return db

def add_path(start, end):
    video_id = input('video id: ')
    start_time = int(input('Start time: '))
    end_time = int(input('End time: '))
    
    db = connect()
    cur = db.cursor()
    
    # Get start id
    cur.execute("""SELECT id FROM sites WHERE name = ?""", (start,))
    start_id = cur.fetchone()
    if start_id:
        start_id = start_id[0]
   
    if not start_id:
        add_site(start)
        cur.execute("""SELECT id FROM sites WHERE name = ?""", (start,))
        start_id = cur.fetchone()
        if start_id:
            start_id = start_id[0]
   
   # Get end id     
    cur.execute("""SELECT id FROM sites WHERE name = ?""", (end,))
    end_id = cur.fetchone()
    if end_id:
        end_id = end_id[0]
    if not end_id:
        add_site(end)
        cur.execute("""SELECT id FROM sites WHERE name = ?""", (end,))
        end_id = cur.fetchone()
        if end_id:
            end_id = end_id[0]
    
    length = end_time - start_time
    
    url = f'youtube.com/embed/{video_id}?start={start_time}&end={end_time}'
    
    cur.execute('INSERT INTO paths(start, end, length, url) VALUES(?, ?, ?, ?)', 
                (start_id, end_id, length, url))
    db.commit()
    db.close()
    
def add_site(site):
    print(f'Entering {site} into database')
    db = connect()
    cur = db.cursor()
    
    image = input('Enter image url: ')
    tag_list = []
    cur.execute('SELECT id, tag FROM tags')
    tags = [{'id': id, 'tag': tag} for id, tag in cur.fetchall()]
    for tag in tags:
        is_tag = input(f"{tag['tag']}? y/n ")
        if is_tag == 'y':
            tag_list.append(tag['id'])
            
    cur.execute('INSERT INTO sites(name, image_url) VALUES(?, ?)',(site, image))
    cur.execute('SELECT id FROM sites WHERE name = ?', (site,))
    site_id = cur.fetchone()
    if site_id:
        site_id = site_id[0]
    for tag in tag_list:
        cur.execute('INSERT INTO site_tags(site_id, tag_id) VALUES(?, ?)', (site_id, tag))
    db.commit()
    db.close()
    
def add_tag(tag):
    db = connect()
    cur = db.cursor()
    
    cur.execute('INSERT INTO tags(tag) VALUES(?)', (tag,))
    cur.execute('SELECT id FROM tags WHERE tag = ?', (tag,))
    tag_id = cur.fetchone()[0]
    cur.execute('SELECT id, name FROM sites')
    sites = [{'id': id, 'name': name} for id, name in cur.fetchall()]
    for site in sites:
        is_tag = input(f"{site['name']}? y/n ")
        if is_tag == 'y':
            cur.execute('INSERT INTO site_tags(site_id, tag_id) VALUES(?, ?)', (site['id'], tag_id))
    db.commit()
    db.close()
    
def fix_urls():
    db= connect()
    cur = db.cursor()
    
    cur.execute('SELECT id, url FROM paths')
    urls = [{'id': id, 'url': url} for id, url in cur.fetchall()]
    for url in urls:
        print(url)
        video_id = input('id: ')
        start = input('start: ')
        end = input('end: ')
        new_url = f'youtube.com/embed/{video_id}?start={start}&end={end}'
        cur.execute('UPDATE paths SET url = ? WHERE id = ?', (new_url, url['id']))
    db.commit()
    db.close()
    
if __name__ == '__main__':
    main()     