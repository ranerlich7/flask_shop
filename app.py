from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.environ.get('DB_HOST')

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = DB_HOST
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    stock = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50), default="General")
    price = db.Column(db.Numeric(10,2), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    
    

@app.route("/")
def hello_world():
   return "<p>Hello, Server is live now please right click on index.html!</p>"

# this function recieves a json product:
# for example. we can call thunder client http:127.0.0.1:9000/create_product
# with body=
# {
#     "category": "Toys",
#     "name": "Baby Jumper",
#     "price": 199.90,
#     "stock": 55
#   }

@app.route('/create_product', methods=['POST'])
def create_product():
    data = request.get_json()    
    # add new article
    new_product = Product(**data)
    # new_product = Product(
    #     name=data['name'], stock=data['stock'], category=data['category'],price=data['price'],image=data['image'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'})



@app.route('/delete_product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Deleted successfully'})
    else:
        return jsonify({'message': f'Error deleting {id}'})




@app.route("/products")
@app.route("/products/<id>")
def article(id=-1):
    if id == -1:
        products = Product.query.all()
    else:
        products = [Product.query.get(id)]
    return_data = []
    for product in products:
        return_data.append(
            {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'stock': product.stock,
                'category': product.category,
                'image':product.image
            })
    if id != -1:
        return jsonify(return_data[0])

    return jsonify(return_data)
    
    
with app.app_context():
    db.create_all()
if __name__ == '__main__':
   app.run(debug=True, port=9000)