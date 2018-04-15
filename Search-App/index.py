from flask import Flask, render_template, request, jsonify
import os
import pymongo as py

app = Flask(__name__,
        static_url_path="/static")

client = py.MongoClient(os.environ['MONGO_URI'])
db = client.ch


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/data", methods=['GET', 'POST'])
def data():
    search = request.get_json()['a'].split(' ')
    res = db.docs.find({
                    'filetype': 'pdf',
                    'doctype': 'annual-returns',
                    'extracted_hand': {'$exists': True},
                    'extracted_hand': {'$in': search}
                })
    out = []

    for i, x in enumerate(res):
        if i == 10:
            break
        out.append(" ".join(x['extracted_hand'][:30]))
    return(jsonify(out))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
