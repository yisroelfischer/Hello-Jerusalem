from flask import Flask, request,  jsonify
from flask_cors import CORS
import sqlite3
from get_tour import main

app = Flask(__name__)
CORS(app)

def connect():
    db = sqlite3.connect('./db.sqlite3')
    db.row_factory = sqlite3.Row
    return db

@app.route('/getSitesList', defaults={'tags': 'all'}, methods=['POST'])
@app.route('/getSitesList/<tags>', methods=['POST'])
def get_sites_list(tags):
    
    db = connect()
    cur = db.cursor()  
    if tags == 'all':
        cur.execute("SELECT * FROM sites")
    else: 
        cur.execute("SELECT * FROM sites WHERE id = ANY(SELECT id FROM tags WHERE tag = ?)", (tags,))
    sites = cur.fetchall()
    db.close()
    
    sites = [dict(site) for site in sites]
    return jsonify(sites)
    

@app.route('/getTour', methods=['POST'])
def get_tour():
    data = request.json
    sites = data.get('sites')
    
    db = connect()
    cur = db.cursor()
    cur.execute('SELECT id, start, end, length FROM paths')
    edges = [{'id': id, 'start': start, 'end': end, 'weight': length} for id, start, end, length in cur.fetchall()]
    db.close()
    
    return jsonify(main(sites, edges))


if __name__ == '__main__':
    app.run(port=3001)