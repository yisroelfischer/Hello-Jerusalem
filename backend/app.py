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

@app.route('/gemini-api-key', methods=['GET'])
def fetchKey():
    key = os.getenv('GEMINI_API_KEY')
    if not key:
        return(jsonify({'error': 404}))
    return jsonify({'key': key})


if __name__ == '__main__':
    app.run(port=5000, debug=True)