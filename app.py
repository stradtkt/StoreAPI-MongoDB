from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource



app = Flask(__name__)
app.config['MONGO_DBNAME'] = "store_mongo_api"
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
        data = request.get_json()
        if not data:
            data = {'message': 'There has been an error'}
            return jsonify(data)
        else:
            _id = data.get('_id')
            if id:
                if mongo.db.products.find_one({"_id": str(_id)}):
                    return {'message': 'Product already exists'}
                else:
                    product = mongo.db.products.insert_one(data)
        return jsonify(product)

    def put(self, product_id):
        product = mongo.db.products
        name = request.json['name']
        price = request.json['price']
        desc = request.json['desc']
        data = {'name': name, 'price': price, 'desc': desc}
        product.update({'_id': ObjectId(product_id)}, {'$set': data})
        new = product.find_one({'_id': str(product_id)})
        output = {'_id': str(new['_id']), 'name': str(new['name']), 'price': int(new['price']), 'desc': str(new['desc'])}
        return jsonify({'product': output})

    def delete(self, product_id):
        mongo.db.products.remove({'_id': str(product_id)})
        return jsonify({'message': 'Item has been deleted.'})



class Employees(Resource):
    def get(self):
        employees = mongo.db.employees
        output = []
        for e in employees.find():
            output.append({'name': str(e['name']),'email': str(e['email']),'phone': str(e['phone']),'dep': str(e['dep'])})
        return jsonify({'employees': output})


    def post(self):
        employee = mongo.db.employees
        name = request.json['name']
        email = request.json['email']
        phone = request.json['phone']
        dep = request.json['dep']
        employee_id = employee.insert({'name': name, 'email': email, 'phone': phone, 'dep': dep})
        new = employee.find_one({'_id': str(employee_id)})
        emp = {'name': str(new['name']), 'email': str(new['email']), 'phone': str(new['phone']), 'dep': str(new['dep'])}
        return jsonify({'employee': emp})

    def put(self, employee_id):
        employee = mongo.db.employees
        name = request.json['name']
        email = request.json['email']
        phone = request.json['phone']
        dep = request.json['dep']
        data = {'name': name, 'email': email, 'phone': phone, 'dep': dep}
        employee.update({'_id': str(employee_id)}, {'$set': data})
        new = employee.find_one({'_id': str(employee_id)})
        output = {'name': str(new['name']), 'email': str(new['email']), 'phone': str(new['phone']), 'dep': str(new['dep'])}
        return jsonify({'employee': output})

    def delete(self, employee_id):
        mongo.db.emplyees.remove({'id': str(employee_id)})
        return jsonify({'message': 'Employee has been deleted.'})




api.add_resource(Product, '/products')
api.add_resource(Employees, '/employees')

if __name__ == '__main__':
    app.run(debug=True)