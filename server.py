from flask import Flask, render_template, request, redirect, session

from flask import Flask
# import the Connector function
from mysqlconnection import MySQLConnector
app = Flask(__name__)
# connect and store the connection in "mysql" note that you pass the database name to the function
mysql = MySQLConnector(app, 'friendsdb')
# an example of running a query

@app.route('/')
def index():
    friends = mysql.query_db("SELECT * FROM friends")
    return render_template('index.html', all_friends=friends )

@app.route('/friends', methods=['POST'])
def create():
    # Write query as a string. Notice how we have multiple values
    # we want to insert into our query.
    query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (:first_name, :last_name, :occupation, NOW(), NOW())"
    # We'll then create a dictionary of data from the POST data received.
    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'occupation': request.form['occupation']
           }
    # Run query, with dictionary values injected into the query.
    mysql.query_db(query, data)
    return redirect('/')


@app.route('/friends/<id>/edit')
def edit(id):

    query = "SELECT * FROM friends Where id = :specific_id"

    data = {'specific_id': id}

    friends = mysql.query_db(query, data)
    return render_template('update.html', all_friends = friends)

@app.route('/friends/<id>', methods=['POST'])
def update(id):

    query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, occupation = :occupation WHERE id = :id"
    # We'll then create a dictionary of data from the POST data received.
    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'occupation': request.form['occupation'],
             'id': id
           }
    # Run query, with dictionary values injected into the query.
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/confirm/friends/<id>/delete', methods=['POST'])
def destroy(id):

    query = "DELETE FROM friends WHERE id = :id"
    data = {'id': id}
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/confirm/<id>', methods=['POST'])
def confirm(id):

    query = "SELECT * FROM friends Where id = :id"
    data = {'id': id}
    friends = mysql.query_db(query, data)
    return render_template("destroy.html", all_friends = friends)







#     query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, occupation = :occupation WHERE id = :id"
# #
# data = {
#          'first_name': request.form['first_name'],
#          'last_name':  request.form['last_name'],
#          'occupation': request.form['occupation'],
#          'id': friend_id
#          }
# mysql.query_db(query, data)
# @app.route('/delete')
# def index():
#     return render_template('/')
#


app.run(debug=True)
