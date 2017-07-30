#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import request

app = Flask(__name__)

entries = [
    {
        'id': 1,
        'title': u'Weather',
        'description': u'The weather in Charleston is hot in July. Also it storms a lot.',
    },
    {
        'id': 2,
        'title': u'Pink carpet',
        'description': u'Does anybody know if carpet can be dyed? I bleached the carpet in my office and now it is pink. Help!',
    },
    {
        'id': 3,
        'title': u'Travel',
        'description': u'Travel is fun but flying is boring. Always stuck in a middle seat with a big sweaty guy in front of you and a screaming baby behind you',
    },
    {
        'id': 4,
        'title': u'Costco',
        'description': u'Costco is great!! I just bought a futon, a bookcase, and beats headphones for $700!!',
    },
    {
        'id': 5,
        'title': u'Edmunds Oast',
        'description': u'Just checked out Edmunds Oast last weekend with a friend of mine. The menu was pretty limited but the drinks were phenomenal! I had some kind of red wine vermouth that was amazing!!',
    },
    {
        'id': 6,
        'title': u'Petco',
        'description': u'Petco does a great job with nail trimming for dogs. Their prices are good and I never have to wait more than a few minutes.',
    }
]

@app.route('/blog/entries', methods=['GET'])
def get_entries():
    return jsonify({'entries':entries})

@app.route('/blog/entries/<int:entry_id>', methods=['GET'])
def get_entry(entry_id):
        entry = [entry for entry in entries if entry['id']==entry_id]
        if len(entry) ==0:
                abort(404)
        return jsonify({'entry':entry[0]})

@app.route('/blog/entries', methods=['POST'])
def create_entry():
    if not request.json or not 'title' in request.json:
        abort(400)
    entry = {
        'id': entries[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
    }
    entries.append(entry)
    return jsonify({'entry': entry}), 201

@app.route('/blog/entries/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    entry = [entry for entry in entries if entry['id'] == entry_id]
    if len(entry) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    entry[0]['title'] = request.json.get('title', entry[0]['title'])
    entry[0]['description'] = request.json.get('description', entry[0]['description'])
    return jsonify({'entry': entry[0]})

@app.route('/blog/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    entry = [entry for entry in entries if entry['id'] == entry_id]
    if len(entry) == 0:
        abort(404)
    entries.remove(entry[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)

