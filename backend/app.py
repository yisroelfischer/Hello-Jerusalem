import os, sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
from get_tour import main
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

def connect():
    db = sqlite3.connect('./db.sqlite3')
    db.row_factory = sqlite3.Row
    return db

@app.route('/get-site-lists', methods=['GET'])
def get_site_lists():
    print('getting site lists')
    db = connect()
    cur = db.cursor() 

    cur.execute('SELECT tag FROM tags')
    tags = cur.fetchall()
    tags = [tag[0] for tag in tags]
        
    site_lists = []
    for tag in tags:
        cur.execute('SELECT id FROM tags WHERE tag = ?', (tag,))
        tag_id = cur.fetchone()[0]
        cur.execute(('''SELECT id, name 
                        FROM sites 
                        WHERE id IN (SELECT site_id 
                                FROM site_tags 
                                WHERE tag_id = ?)'''), (tag_id,))
        sites = [{'id': id, 'name': name} for id, name in cur.fetchall()]
        site_lists.append({'tag': tag, 'list': [site for site in sites]})
    db.close()

    return jsonify(site_lists)
    

@app.route('/get-tour', methods=['GET'])
def get_tour():
    sites = request.args.get('sites')
    if not sites:
        return jsonify({'error': 'no sites provided'}), 400
    sites = [int(site) for site in sites.split(',')]
    
    db = connect()
    cur = db.cursor()
    cur.execute('SELECT id, start, end, length FROM paths')
    edges = [{'id': id, 'start': start, 'end': end, 'weight': length} 
             for id, start, end, length in cur.fetchall()]
    db.close()
    
    result = main(sites, edges)
    if not result:
        return jsonify({'error': 'invalid tour'}), 400
    tour = []
    for i in result:
        if isinstance(i, int):
            tour.append({'type': 'site', 'id': i})
        else:
            tour.extend([
                {'type': 'site', 'id': i[0]}, 
                {'type': 'path', 'start': i[0], 'end': i[1]}, 
                {'type': 'site', 'id': i[1]}
                ])
    return jsonify(result)

@app.route('/gemini-api-key', methods=['GET'])
def fetchKey():
    key = os.getenv('GEMINI_API_KEY')
    if not key:
        return(jsonify({'error': 404}))
    return jsonify({'key': key})

@app.route('/get-site')
def get_site():
    site = request.args.get('site')
    if not site.isdigit():
        return jsonify({'error': 'invalid format'}), 400
    return get_site_info(site)

@app.route('/get-path')
def get_path():
    path = request.args.get('path')
    path = path.split(',')
    
    if len(path) == 2 and all(p.isdigit() for p in path):
        start = int(path[0])
        end = int(path[1])
        start_info = get_site_info(start)
        path_info = get_path_info((start, end))
        end_info = get_site_info(end)
        return jsonify({'start': start_info, 'path': path_info, 'end': end_info})
    return jsonify({'error': 'invalid format'}), 400
    
def get_site_info(site):
    db = connect()
    cur = db.cursor()
    cur.execute('SELECT id, name, image_url FROM sites WHERE id = ?', (site,))
    info = cur.fetchone()
    if not info:
        return jsonify({'error': 'no response recieved'}), 400
    db.close()
    id, name, image = info
    return {'id': id, 'name': name, 'image': image}

 
def get_path_info(path):
    db = connect()
    cur = db.cursor()
    cur.execute('SELECT url FROM paths WHERE start = ? AND end = ?', (path[0], path[1]))
    url = cur.fetchone()
    db.close()
    if not url:
        return {'error': 'no response recieved'}, 400
    return {'url': url[0]}

if __name__ == '__main__':
    app.run(port=5000, debug=True)