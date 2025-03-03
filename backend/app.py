from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from get_tour import main

app = Flask(__name__)
CORS(app)

def connect():
    db = sqlite3.connect('./db.sqlite3')
    db.row_factory = sqlite3.Row
    return db

@app.route('/get-site-lists', defaults={'tags': 'all'}, methods=['GET'])
@app.route('/get-site-lists/<tags>', methods=['GET'])
def get_site_lists(tags):
    print('getting site lists')
    db = connect()
    cur = db.cursor() 
    
    if tags == 'all':
        cur.execute('SELECT tag FROM tags')
        tags = cur.fetchall()
        tags = [tag[0] for tag in tags] 
    else:
        tags = tags.split(',')
        
    site_lists = []
    for tag in tags:
        cur.execute('SELECT id FROM tags WHERE tag = ?', (tag,))
        tag_id = cur.fetchone()[0]
        cur.execute('SELECT id, name FROM sites WHERE id IN (SELECT site_id FROM site_tags WHERE tag_id = ?)', (tag_id,))
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
    edges = [{'id': id, 'start': start, 'end': end, 'weight': length} for id, start, end, length in cur.fetchall()]
    db.close()
    
    result = main(sites, edges)
    if not result:
        return jsonify({'error': 'invalid tour'}), 400
    print(result)
    return jsonify(result)


if __name__ == '__main__':
    app.run(port=3001, debug=True)