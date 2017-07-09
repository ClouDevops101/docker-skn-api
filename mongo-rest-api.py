from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from pymongo import MongoClient
import os

app = Flask(__name__)

client = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)
db = client.stars
#app.config['MONGO_DBNAME'] = 'restdb'
#app.config['MONGO_URI'] = 'mongodb://db:27017/restdb'


#mongo = PyMongo(app)

@app.route('/star', methods=['GET'])
def get_all_stars():
  star = db.stars
  output = []
  for s in star.find():
    output.append({'name' : s['name'], 'distance' : s['distance']})
  return jsonify({'result' : output})

@app.route('/star/', methods=['GET'])
def get_one_star(name):
  star = db.stars
  s = star.find_one({'name' : name})
  if s:
    output = {'name' : s['name'], 'distance' : s['distance']}
  else:
    output = "No such name"
  return jsonify({'result' : output})

@app.route('/star', methods=['POST'])
def add_star():
  star = db.stars
  name = request.json['name']
  distance = request.json['distance']
  star_id = star.insert({'name': name, 'distance': distance})
  new_star = star.find_one({'_id': star_id })
  output = {'name' : new_star['name'], 'distance' : new_star['distance']}
  return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
