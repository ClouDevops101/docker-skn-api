import os
from flask import Flask, redirect, url_for, request, render_template
from flask import jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)
db = client.star

@app.route('/star', methods=['GET'])
def get_all_stars():
  star = db.star
  output = []
  for s in star.find():
    output.append({'name' : s['name'], 'age' : s['age']})
  return jsonify({'result' : output})

@app.route('/star/name/<string:name>', methods=['GET'])
def get_one_star_by_name(name):
  star = db.star
  s = star.find_one({'name' : name})
  if s:
    output = {'name' : s['name'], 'age' : s['age']}
  else:
    output = "No such name"
  return jsonify({'result' : output})

@app.route('/star/age', methods=['DELETE'])
def remove_one_star_by_age():
  star = db.star
  age = request.json['age']
 # for obj in star.find({"age": age}):
#    id = obj["_id"]
 # star.remove("_id": ObjectId(id))
  output = star.delete_many({"age": age})
  #new_star = star.find_one({'_id': star_id })
  #output = {'name' : new_star['name'], 'age' : new_star['age']}
  return jsonify({'deleted' : output.deleted_count})

@app.route('/star/name', methods=['DELETE'])
def remove_one_star_by_name():
  star = db.star
  name = request.json['name']
 # for obj in star.find({"age": age}):
#    id = obj["_id"]
 # star.remove("_id": ObjectId(id))
  output = star.delete_many({"name": name})
  #new_star = star.find_one({'_id': star_id })
  #output = {'name' : new_star['name'], 'age' : new_star['age']}
  return jsonify({'deleted' : output.deleted_count})

#@app.route('/star/name/v2', methods=['DELETE'])
#def delete_one_star_by_name():
#  star = db.star
#  name = request.json['name']
#  for obj in star.find({"name": name}):
#    id = obj["_id"]
#  output = star.remove("_id" : ObjectId(id))
  #output = star.delete_many({"name": age})
  #new_star = star.find_one({'_id': star_id })
  #output = {'name' : new_star['name'], 'age' : new_star['age']}
#  return jsonify({'Removed' : output})


@app.route('/star/age/<int:age>', methods=['GET'])
def get_one_star_by_age(age):
  star = db.star
  s = star.find_one({'age' : age})
  if s:
    output = {'name' : s['name'], 'age' : s['age']}
  else:
    output = "No such age"
  return jsonify({'result' : output})

#@app.route('/star/<int:star_id>', methods=['GET'])
#def get_id_star(name):
#  star = db.star
#  s = star.find_one({'_id' : start_id})
#  if s:
#    output = {'name' : s['name'], 'age' : s['age']}
#  else:
#    output = "No such name"
#  return jsonify({'result' : output})

@app.route('/star', methods=['POST'])
def add_star():
  star = db.star
  name = request.json['name']
  age = request.json['age']
  star_id = star.insert({'name': name, 'age': age})
  new_star = star.find_one({'_id': star_id })
  output = {'name' : new_star['name'], 'age' : new_star['age']}
  return jsonify({'result' : output})

@app.route('/view')
def todo():
  star = db.star
  _items = star.find()
  items = [item for item in _items]
  return render_template('todo.html', items=items)


@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'name': request.form['name'],
        'age': request.form['age']
    }
    db.star.insert_one(item_doc)

    return redirect(url_for('todo'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
