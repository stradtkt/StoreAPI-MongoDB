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
        output = []
        for p in products.find():
            output.append({"_id": str(p["_id"]), "name": str(p["name"]), "price": int(p["price"]), "desc": str(p["desc"])})
        return jsonify({"products": output})

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

    def delete(self, product_id):
        mongo.db.products.remove({'id': ObjectId(product_id)})
        return jsonify({'message': 'Item has been deleted.'})



class Employees(Resource):
    def get(self):
       employees = mongo.db.employees
       output = []
       for e in employees.find():
           output.append({
               'name': str(e['name']),
               'email': str(e['email']),
               'phone': str(e['phone']),
               'dep': str(e['dep'])
           })
        return jsonify({'employees': output})


    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass




api.add_resource(Product, '/products')
api.add_resource(Employees, '/employees')

if __name__ == '__main__':
    app.run(debug=True)