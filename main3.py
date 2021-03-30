from flask import Flask, Response, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import json
from bson.json_util import dumps

app = Flask(__name__)

try:
    # app.config['MONGO_URI'] = "mongodb://localhost:27017/Invoice"
    app.config['MONGO_URI'] = 'mongodb://coworking:admin@117.53.44.15:30001,117.53.44.15:30002,117.53.44.15:30003/coworking?authSource=coworking&replicaSet=my-mongo-set'
    mongo = PyMongo(app)
    collection = mongo.db.invoice
except:
    print('ERORR CANNOT CONNECT TO DB')

        
@app.route('/invoice/insert_invoice', methods=['POST'])
def insert():
    try:
        invoice = request.get_json() or {
            'id_user': request.form['id_user'],
            'status': request.form['status'],
            'token': request.form['token'],
            'tempat': request.form['tempat'],
            'capacity': request.form['capacity'],
            'invoice': request.form['invoice'],
            'is_aktif': request.form['is_aktif']
        }
        dbResponse = collection.insert_one(invoice)
        print(dbResponse.inserted_id)

        return Response(
            response= json.dumps({
                'message':'invoice berhasil dibuat',
                'id': f'{dbResponse.inserted_id}'
            }),
            status=200,
            mimetype='apllication/json'
        )
    except Exception as ex:
        print(ex)
        return jsonify('Cannot insert invoice')    

@app.route('/invoice/get_invoice', methods=['GET'])
def get():
    try:
        data = list(collection.find())
        return Response(
            response= json.dumps(data, default=str),
            status= 500,
            mimetype='application/json'
        )
    except Exception as ex:
        print(ex)
        return jsonify('Cannot read invoice')

@app.route('/invoice/get_invoice/<id>', methods=['GET'])
def get_invoicebyid(id):
    try:
        data = collection.find_one({'_id':ObjectId(id)})
        return Response(
            response= json.dumps(data, default=str),
            status= 500,
            mimetype='application/json'
        )
    except Exception as ex:
        print(ex)
        return jsonify('Cannot read invoice')

@app.route('/invoice/update_invoice/<id>', methods=['POST'])
def update(id):
    try:
        invoice = request.get_json() or {
            'id_user': request.form['id_user'],
            'status': request.form['status'],
            'token': request.form['token'],
            'tempat': request.form['tempat'],
            'capacity': request.form['capacity'],
            'invoice': request.form['invoice'],
            'is_aktif': request.form['is_aktif']
        }

        collection.update_one(
            {'_id':ObjectId(id)},
            {'$set': invoice}
            )
            
        return Response(
            response= json.dumps('Invoice updated'),
            status= 200,
            mimetype='application/json'
            )

    except Exception as ex:
        print(ex)
        return jsonify('Cannot update invoice')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)