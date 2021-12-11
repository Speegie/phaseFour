from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml
from datetime import date

app = Flask(__name__)
#app.run()

# Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

currentDate = date.today()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['reg'] == 'regUser':
            return redirect('/register')
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/adminHome', methods=['GET', 'POST'])
def adminHome():
    if request.method == 'POST':
        if request.form['but'] == 'sched':
            return redirect('/scheduleFlight')
        if request.form['but'] == 'removeF':
            return redirect('/removeFlight')
        if request.form['but'] == 'processD':
            return redirect('/processDate')
        if request.form['but'] == 'viewAirports':
            return redirect('/viewAirports')
        if request.form['but'] == 'viewAirlines':
            return redirect('/viewAirlines')
        if request.form['but'] == 'viewC':
            return redirect('/viewCustomers')
        if request.form['but'] == 'viewO':
            return redirect('/viewOwners')
        if request.form['but'] == 'logout':
            return redirect('/')
    return render_template('adminHome.html') 

@app.route('/scheduleFlight', methods=['GET', 'POST'])
def scheduleFlight():
    if request.method == 'POST':
        if request.form['but'] == 'back':
            return redirect('/adminHome')
    return render_template('scheduleFlight.html')

@app.route('/removeFlight', methods=['GET', 'POST'])
def removeFlight():
    if request.method == 'POST':
        if request.form['but'] == 'back':
            return redirect('/adminHome')
    return render_template('removeFlight.html')

@app.route('/processDate', methods=['GET', 'POST'])
def processDate():
    if request.method == 'POST':
        if request.form['but'] == 'back':
            return redirect('/adminHome')
    return render_template('processDate.html')

@app.route('/viewAirports', methods=['GET', 'POST'])
def viewAirports():
    if request.method == 'POST':
        if request.form['but'] == 'back':
            return redirect('/adminHome')
    return render_template('viewAirports.html')

@app.route('/viewCustomers', methods=['GET', 'POST'])
def viewCustomers():
    if request.method == 'POST':
        if request.form['but'] == 'back':
            return redirect('/adminHome')
    return render_template('viewCustomers.html')

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM accounts")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html', userDetails=userDetails)



@app.route('/viewOwners', methods=['GET', 'POST'])
def viewOwners():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        if request.form['btn_identifier'] == 'sortOne':
            resultValue = cur.execute("SELECT * FROM view_owners order by avg_rating desc")
            viewOwnersDetails = cur.fetchall()
            return render_template('viewOwners.html', viewOwnersDetails=viewOwnersDetails)
        if request.form['btn_identifier'] == 'sortTwo':
            resultValue = cur.execute("SELECT * FROM view_owners order by num_properties_owned desc")
            viewOwnersDetails = cur.fetchall()
            return render_template('viewOwners.html', viewOwnersDetails=viewOwnersDetails)
        if request.form['btn_identifier'] == 'sortThree':
            resultValue = cur.execute("SELECT * FROM view_owners order by avg_property_rating desc")
            viewOwnersDetails = cur.fetchall()
            return render_template('viewOwners.html', viewOwnersDetails=viewOwnersDetails)
        if request.form['btn_identifier'] == 'sortFour':
            text = request.form['text']
            resultValue = cur.execute("SELECT * FROM view_owners where owner_name like '%" + text + "%'")
            viewOwnersDetails = cur.fetchall()
            return render_template('viewOwners.html', viewOwnersDetails=viewOwnersDetails)
        if request.form['btn_identifier'] == 'back':
            #return render_template('index.html')
            return redirect('/adminHome')

    if request.method == 'GET':
        resultValue = cur.execute("SELECT * FROM view_owners")
        viewOwnersDetails = cur.fetchall()
        return render_template('viewOwners.html', viewOwnersDetails=viewOwnersDetails)


@app.route('/viewAirlines', methods=['GET', 'POST'])
def viewAirlines():
    
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        if request.form['btn_identifier'] == 'sortOne':
            resultValue = cur.execute("SELECT * FROM view_airlines order by rating desc")
            viewAirlinesDetails = cur.fetchall()
            return render_template('viewAirlines.html', viewAirlinesDetails=viewAirlinesDetails)
        if request.form['btn_identifier'] == 'sortTwo':
            resultValue = cur.execute("SELECT * FROM view_airlines order by total_flights desc")
            viewAirlinesDetails = cur.fetchall()
            return render_template('viewAirlines.html', viewAirlinesDetails=viewAirlinesDetails)
        if request.form['btn_identifier'] == 'sortThree':
            resultValue = cur.execute("SELECT * FROM view_airlines order by min_flight_cost desc")
            viewAirlinesDetails = cur.fetchall()
            return render_template('viewAirlines.html', viewAirlinesDetails=viewAirlinesDetails)
        if request.form['btn_identifier'] == 'sortFour':
            text = request.form['text']
            resultValue = cur.execute("SELECT * FROM view_airlines   where airline_name like '%" + text + "%'")
            viewAirlinesDetails = cur.fetchall()
            return render_template('viewAirlines.html', viewAirlinesDetails=viewAirlinesDetails)
        if request.form['btn_identifier'] == 'back':
            #return render_template('index.html')
            return redirect('/adminHome')

    if request.method == 'GET':
        resultValue = cur.execute("SELECT * FROM view_airlines")
        viewAirlinesDetails = cur.fetchall()
        return render_template('viewAirlines.html', viewAirlinesDetails=viewAirlinesDetails)
    
    
    
    #cur = mysql.connection.cursor()
    #resultValue = cur.execute("SELECT * FROM view_airlines")
    #if resultValue > 0:
        #viewAirlineDetails = cur.fetchall()
        #return render_template('viewAirlines.html', viewAirlineDetails=viewAirlineDetails)



@app.route('/setDate')
def setDate():
    if request.method == 'POST':
        currentDate = request.form
        theCurrentDate = currentDate['totalDate']
    return render_template('setDate.html')

if __name__ == '__main__':
    app.run(debug=True)