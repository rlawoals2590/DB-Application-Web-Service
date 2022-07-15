from unittest import result
from flask import Flask, render_template, request, jsonify
from flask_mysql_connector import MySQL


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rlawoals2590'
app.config['MYSQL_DATABASE'] = 'storage'
mysql = MySQL(app)

SELECT_SQL = 'SELECT product_id, product_name, product_price, product_mart FROM storage.storags1s'

@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/select/', methods=['POST'])
def SELECT():
    if request.method == 'POST':
        mycursor = mysql.new_cursor(dictionary=True)
        mycursor.execute(SELECT_SQL)
        myresult = mycursor.fetchall()
        return str(myresult)

@app.route('/insert/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        content = '''
            <form action="http://127.0.0.1:5000/insert/" method="POST">
            <p><input type="number" name="product_id" placeholder="product_id"></p>
            <p><input type="text" name="product_name" placeholder="product_name"></p>
            <p><input type="number" name="product_price" placeholder="product_price"></p>
            <p><input type="text" name="product_mart" placeholder="product_mart"></p>
            <p><input type="submit" value="INSERT"></p>
        '''
        return content
    elif request.method == 'POST':
        id = request.form['product_id']
        name = request.form['product_name']
        price = request.form['product_price']
        mart = request.form['product_mart']
        INSERT_SQL = 'INSERT INTO storage.storags1s (product_id, product_name, product_price ,product_mart)  VALUES("{0}", "{1}", "{2}", "{3}")'.format(id, name, price, mart)
        mycursor = mysql.new_cursor(dictionary=True)
        mycursor.execute(INSERT_SQL)
        conn = mysql.connection
        conn.commit()
        return "was inserted."

if __name__ == '__main__':
    app.run(debug=True)