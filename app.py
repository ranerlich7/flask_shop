from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'
db = SQLAlchemy(app)



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    stock = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50), default="General")
    price = db.Column(db.Numeric(10,2), nullable=False)

@app.route("/")
def hello_world():
   return "<p>Hello, World!</p>"

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
    new_product = Product(name=data['name'], stock=data['stock'], category=data['category'],price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'})
    
    
with app.app_context():
    db.create_all()

if __name__ == '__main__':
   app.run(debug=True, port=9000)