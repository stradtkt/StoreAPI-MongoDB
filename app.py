from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource
from bson.objectid import ObjectId
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/store_mongo_api"
mongo = PyMongo(app)
api = Api(app)

class Product(Resource):
    def get(self):
        products = mongo.db.products
        products = []
        for p in products.find():
            products.append({"_id": str(p["_id"]), "name": str(p["name"]), "price": int(p["price"]), "desc": str(p["desc"])})
        return jsonify({"products": products})

    def post(self):
        products = mongo.db.products
        name = request.json['name']
        price = request.json['price']
        desc = request.post['desc']
        product_id = products.insert({'name': name, 'price': price, 'desc': desc})
        new_prod = products.find_one({'id': product_id})
        product = {'name': new_prod['name'], 'price': new_prod['price'], 'desc': new_prod['desc']}
        return jsonify({'product': product})

    def put(self, product_id):
        product = mongo.db.products
        name = request.json['name']
        price = request.json['price']
        desc = request.json['desc']
        data = {'name': name, 'price': price, 'desc': desc}
        product.update({'_id': ObjectId(product_id)}, {'$set': data})
        new = product.find_one({'_id': ObjectId(product_id)})
        output = {'_id': str(new['_id']), 'name': str(new['name']), 'price': int(new['price']), 'desc': str(new['desc'])}
        return jsonify({'product': output})








api.add_resource(Product, '/products')

if __name__ == '__main__':
    app.run(debug=True)