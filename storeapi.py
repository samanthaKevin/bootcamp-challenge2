"""API program for store manager"""

import datetime
from flask import Flask
from flask import request
from flask import jsonify

APP = Flask(__name__)

EMPLOYEES = ['Mutenyo Charity', 'Masembe Steven']
PRODUCTS = [
    {'name':'cake', 'price': 11000, 'qty': 3},
    {'name':'cup', 'price': 25000, 'qty': 10},
    {'name':'exercise book', 'price': 5000, 'qty': 30}
]
SALES = [
    {'product_name':'exercise book', 'employee':'Mutenyo Charity',
     'product_amount':5000, 'date':'22-Sept-2018'},
    {'product_name':'cake', 'employee':'Mutenyo Charity',
     'product_amount':11000, 'date':'22-Sept-2018'},
    {'product_name':'cup', 'employee':'Mutenyo Charity',
     'product_amount':25000, 'date':'23-Sept-2018'},
    {'product_name':'cup', 'employee':'Mutenyo Charity',
     'product_amount':25000, 'date':'23-Sept-2018'},
    {'product_name':'cake', 'employee':'Masembe Steven',
     'product_amount':11000, 'date':'22-Sept-2018'},
    {'product_name':'cake', 'employee':'Masembe Steven',
     'product_amount':11000, 'date':'23-Sept-2018'}
]

def obj_created(obj):
    """Function to handle success messages."""

    resp = jsonify(obj)
    resp.status_code = 201
    return resp

@APP.errorhandler(404)
def not_found():
    """Function to handle not found urls."""

    message = {
        'status':404,
        'message':'Not Found: ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@APP.errorhandler(415)
def not_supported():
    """Function to handle not supported content types."""

    message = {
        'status':415,
        'message':'Not Supported: ' + request.headers['Content-Type']
    }
    resp = jsonify(message)
    resp.status_code = 415
    return resp

@APP.errorhandler(500)
def wrong_parameters():
    """Function to handle unsupported parameters."""

    message = {
        'status':500,
        'message':'Unsupported Parameters'
    }
    resp = jsonify(message)
    resp.status_code = 500
    return resp

@APP.route('/v1/products', methods=['GET'])
def getproducts():
    """This function gets all products."""

    allproducts = jsonify(PRODUCTS)
    allproducts.status_code = 200
    return allproducts

@APP.route('/v1/products/<int:product_id>', methods=['GET'])
def getproduct(product_id):
    """This function gets a specific product by id."""

    product = jsonify(PRODUCTS[product_id])
    product.status_code = 200
    return product

@APP.route('/v1/sales', methods=['GET'])
def getsales():
    """This function all sales."""

    allsales = jsonify(SALES)
    allsales.status_code = 200
    return allsales

@APP.route('/v1/sales/<int:sale_id>', methods=['GET'])
def getsale(sale_id):
    """This function gets a specific sale by id."""

    sale = jsonify(SALES[sale_id])
    sale.status_code = 200
    return sale

@APP.route('/v1/products', methods=['POST'])
def create_product():
    """This function creates a new product."""

    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        if 'name' in data and 'price' in data and 'qty' in data:
            name = data['name']
            price = data['price']
            qty = data['qty']
            PRODUCTS.append({'name':name, 'price':price, 'qty':qty})
            obj = {'name':name, 'price':price, 'qty':qty}
            return obj_created(obj)
        else:
            return wrong_parameters()
    elif request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        data = request.form
        if 'name' in data and 'price' in data and 'qty' in data:
            name = data['name']
            price = data['price']
            qty = data['qty']
            PRODUCTS.append({'name':name, 'price':price, 'qty':qty})
            obj = {'name':name, 'price':price, 'qty':qty}
            return obj_created(obj)
        else:
            return wrong_parameters()
    else:
        return not_supported()

@APP.route('/v1/sales', methods=['POST'])
def create_sale():
    """This function creates a new sale."""

    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        # check if parameters exist
        if 'employee' in data and 'product_name' in data:
            # check if employee exists
            if data['employee'] in EMPLOYEES:
                employee = data['employee']
            else:
                return not_found()

            for item in PRODUCTS:
                # check if product exists
                if data['product_name'] == item['name']:
                    product_name = data['product_name']
                    product_amount = item['price']
                    break

            date = datetime.datetime.now()
            SALES.append({
                'employee':employee, 'product_name':product_name,
                'product_amount':product_amount, 'date':date
                })
            obj = {
                'employee':employee, 'product_name':product_name,
                'product_amount':product_amount, 'date':date
                }
            return obj_created(obj)
        else:
            return wrong_parameters()
    elif request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        data = request.form
        # check if parameters exist
        if 'employee' in data and 'product_name' in data:
            # check if employee exists
            if data['employee'] in EMPLOYEES:
                employee = data['employee']
            else:
                return not_found()

            for item in PRODUCTS:
                # check if product exists
                if data['product_name'] == item['name']:
                    product_name = data['product_name']
                    product_amount = item['price']
                    break

            date = datetime.datetime.now()
            SALES.append({
                'employee':employee, 'product_name':product_name,
                'product_amount':product_amount, 'date':date
                })
            obj = {
                'employee':employee, 'product_name':product_name,
                'product_amount':product_amount, 'date':date
                }
            return obj_created(obj)
        else:
            return wrong_parameters()    
    else:
        return not_supported()

if __name__ == '__main__':
    APP.run(port='5002', debug=True)
