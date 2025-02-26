from flask import Flask, jsonify
import sqlite3
import get_tour

app = Flask(__name__)

def connect():
    db = sqlite3.connect('./db')
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
    

@app.route('/getTour<sites>', methods=['POST'])
def get_tour(sites):
    return get_tour.main(sites)