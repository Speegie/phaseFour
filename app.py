from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml
from datetime import date

app = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

currentDate = date.today()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        #cur = mysql.connection.cursor()
        #cur.execute("INSERT INTO users(name, email) VALUES(%s, %s)",(name, email))
        #mysql.connection.commit()
        #cur.close()
        return redirect('/users')
    return render_template('index.html')


@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM accounts")
    print(resultValue)
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html', userDetails=userDetails)




@app.route('/viewAirlines')
def viewAirlines():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM view_airlines")
    if resultValue > 0:
        viewAirlineDetails = cur.fetchall()
        return render_template('viewAirlines.html', viewAirlineDetails=viewAirlineDetails)

@app.route('/viewOwners')
def viewOwners():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM view_owners")
    if resultValue > 0:
        viewOwnersDetails = cur.fetchall()
        return render_template('viewOwners.html', viewOwnersDetails=viewOwnersDetails)

        





@app.route('/setDate')
def setDate():
    if request.method == 'POST':
        currentDate = request.form
        theCurrentDate = currentDate['totalDate']
    return render_template('setDate.html')

if __name__ == '__main__':
    app.run(debug=True)