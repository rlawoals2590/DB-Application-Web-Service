from flask import Flask, render_template, request, jsonify
from flask_mysql_connector import MySQL


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rlawoals2590'
app.config['MYSQL_DATABASE'] = 'competition'
mysql = MySQL(app)

@app.route('/')
def Index():
    return render_template('./index.html')

# SELECT
@app.route('/select/', methods=['GET', 'POST'])
def SELECT():
    if request.method == 'GET':
        content = '''
            <form action="http://127.0.0.1:5000/select/" method="POST">
            <p><input type="text" name="product_name" placeholder="product_name"></p>
            <p><input type="submit" value="SELECT"></p>
            '''
        return content
    elif request.method == 'POST':
        name = request.form['product_name']
        SELECT_SQL = 'SELECT * FROM competition.storage WHERE product_name LIKE "%{0}%"'.format(name)
        mycursor = mysql.new_cursor(dictionary=True)
        mycursor.execute(SELECT_SQL)
        myresult = mycursor.fetchall()
        return render_template('./success.html', data=myresult) 

# INSERT
@app.route('/insert/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        content = '''
            <form action="http://127.0.0.1:5000/insert/" method="POST">
            <p><input type="text" name="product_name" placeholder="product_name"></p>
            <p><input type="number" name="product_price" placeholder="product_price"></p>
            <p><input type="text" name="storebrand" placeholder="storebrand"></p>
            <p>1 = 음료, 2 = 과자, 3 = 레토르트 식품<p>
            <p><input type="number" name="category" placeholder="category"></p>
            <p><input type="text" name="event" placeholder="event"></p>
            <p><input type="submit" value="INSERT"></p>
            </form>
            <a href="http://127.0.0.1:5000"><input type="submit" value="Cancel"></a>
        '''
        return content
    elif request.method == 'POST':
        name = request.form['product_name']
        price = request.form['product_price']
        store = request.form['storebrand']
        category = request.form['category']
        event = request.form['event']
        INSERT_SQL = 'INSERT INTO competition.storage (product_name, product_price ,storebrand, category, event)  VALUES("{0}", "{1}", "{2}", "{3}", "{4}")'.format(name, price, store, category, event)
        mycursor = mysql.new_cursor(dictionary=True)
        mycursor.execute(INSERT_SQL)
        conn = mysql.connection
        conn.commit()
        return render_template('./success.html')

# DELETE
@app.route('/delete/', methods=['GET', 'POST'])
def delete():
    if request.method == 'GET':
        SELECT_SQL = 'SELECT * FROM competition.storage'
        mycursor = mysql.new_cursor(dictionary=True)
        mycursor.execute(SELECT_SQL)
        myresult = mycursor.fetchall()
        return render_template('./delete.html', data=myresult) 
    elif request.method == 'POST':
        name = request.form['product_name']
        store = request.form['storebrand']
        DELETE_SQL = 'DELETE FROM competition.storage WHERE product_name = "{0}" AND storebrand = "{1}"'.format(name, store)
        mycursor = mysql.new_cursor(dictionary=True)
        mycursor.execute(DELETE_SQL)
        mycursor.execute('ALTER TABLE storage AUTO_INCREMENT=1;')
        mycursor.execute('SET @COUNT = 0;')
        mycursor.execute('UPDATE storage SET product_id = @COUNT:=@COUNT+1;')
        conn = mysql.connection
        conn.commit()
        return render_template('./success.html')

if __name__ == '__main__':
    app.run(debug=True)