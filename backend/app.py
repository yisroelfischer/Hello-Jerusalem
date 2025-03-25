import os, sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
from get_tour import main
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

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
    

@app.route('/get-tours', methods=['GET'])
def get_tours():
    raw_sites = request.args.get('sites')
    print(f'raw sites: {raw_sites}')
    if not raw_sites:
        return jsonify({'error': 'no sites provided'}), 400
    split_sites = raw_sites.split(',')
    print(f'split sites: {split_sites}')
    sites = []
    for site in split_sites:
        if not site.isdigit():
            return jsonify({'error': 'invalid sites'}), 400
        sites.append(int(site))
    print(f'sites: {sites}')
    
    
    db = connect()
    cur = db.cursor()
    cur.execute('SELECT id, start, end, length FROM paths')
    edges = [{'id': id, 'start': start, 'end': end, 'weight': length} 
             for id, start, end, length in cur.fetchall()]
    db.close()
    
    result = main(sites, edges)
    print(f'result: {result}')
    if not result:
        return jsonify({'error': 'invalid tour'}), 400
    tours = []
    for tour in result:
        split_tour = []
        for seg in tour:
            if isinstance(seg, tuple):
                split_tour.extend([seg[0], seg, seg[1]])
            else:
                split_tour.append(seg)
        tours.append([dictify(seg) for seg in split_tour])
               
    return jsonify(tours)


def dictify(seg):
    if isinstance(seg, int):
        return {'type': 'site', 'id': seg}
    if isinstance(seg, tuple):
        return {'type': 'path', 'start': seg[0], 'end': seg[1]}
    

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
    cur.execute('SELECT length, video_id, start_time, end_time FROM paths WHERE start = ? AND end = ?', (path[0], path[1]))
    path_info = [
        {'length': length, 
        'videoId': video_id, 
        'startTime': start_time, 
        'endTime': end_time} 
        for length, video_id, start_time, end_time in cur.fetchall()]
    db.close()
    
    if not path_info:
        return {'error': 'no response recieved'}, 400 
    path_info.sort(key=lambda x: int(x['length']))
    return path_info[0]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)