from flask import Flask, render_template

app = Flask(__name__)

@app.route('/login')
def Login():
     pass

""" CRUD do produto"""

@app.route('/')
def ListProducts():
     return render_template("index.html")

@app.route('/delete_products')
def DeleteProducts():
     pass

@app.route('/insert_products')
def InsertProducts():
     pass

@app.route('/update_products')
def UpdateProducts():
     pass


""" CRUD do vendedor """

@app.route('/insert_Seller')
def InsertSeller():
     pass

@app.route('/delete_seller')
def DeleteSeller():
     pass

@app.route('/list_seller')
def ListSeller():
     pass

@app.route('/update_seller')
def UpdateSeller():
     pass


if __name__ == '__main__':
     app.run()