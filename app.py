from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL, MySQLdb
import yaml
from datetime import date
import re

app = Flask(__name__)
app.run()

# Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

currentDate = date.today()

#cdemilio@tiktok.com
#Charlie Demilio
name, email, status = 'Addison Ray', 'aray@tiktok.com', None

@app.route('/', methods=['GET', 'POST'])
def index():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        if request.form['action'] == 'regUser':
            return redirect('/register')
        # Fetch form data
        userDetails = request.form

        global name, email, status
    
        name = userDetails['name']
        email = userDetails['email']
        status = [0, 0, 0]

        if request.form['action'] == 'loginUser':
            result_value = cur.execute("select * from admins where email=%s", (email,))
            if (result_value > 0):
                status[0] = 1
                print(status)
                return redirect('/intermediate')
            result_value = cur.execute("select * from customer where email=%s", (email,))
            if (result_value > 0):
                status[1] = 1
                print(status)
                return redirect('/intermediate')
            result_value = cur.execute("select * from owners where email=%s", (email,))
            if (result_value > 0):
                status[2] = 1
                print(status)
                return redirect('/intermediate')

        return redirect('/')
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/intermediate', methods=['GET', 'POST'])
def intermediate():
    if request.method == 'POST':
        if request.form['but'] == "admin":
            return redirect('/adminHome')
        if request.form['but'] == 'customer':
            return redirect('/customerHome')
        if request.form['but'] == 'owner':
            return redirect('/ownerHome')
    print(status)
    return render_template('intermediate.html', status = status)

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
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        if request.form['btn_identifier'] == 'sortOne':
            resultValue = cur.execute("SELECT * FROM view_airports order by Airport_Id asc")
            viewAirportDetails = cur.fetchall()
            return render_template('viewAirports.html', viewAirportDetails=viewAirportDetails)
        if request.form['btn_identifier'] == 'sortTwo':
            resultValue = cur.execute("SELECT * FROM view_airports order by Airport_Name asc")
            viewAirportDetails = cur.fetchall()
            return render_template('viewAirports.html', viewAirportDetails=viewAirportDetails)
        if request.form['btn_identifier'] == 'sortThree':
            resultValue = cur.execute("SELECT * FROM view_airports order by Time_Zone asc")
            viewAirportDetails = cur.fetchall()
            return render_template('viewAirports.html', viewAirportDetails=viewAirportDetails)
        if request.form['btn_identifier'] == 'sortFour':
            text = request.form['text']
            resultValue = cur.execute("SELECT * FROM view_airports where Airport_Name like '%" + text + "%'")
            viewAirportDetails = cur.fetchall()
            return render_template('viewAirports.html', viewAirportDetails=viewAirportDetails)
        if request.form['btn_identifier'] == 'sortFive':
            time = request.form.get('time')
            resultValue = cur.execute("SELECT * FROM view_airports where time_zone = '" + time + "'")
            viewAirportDetails = cur.fetchall()
            return render_template('viewAirports.html', viewAirportDetails=viewAirportDetails)
        if request.form['btn_identifier'] == 'back':
            return redirect('/adminHome')
        if request.form['btn_identifier'] == 'sortSix':
            resultValue = cur.execute("SELECT * FROM view_airports order by total_arriving_flights desc")
            viewAirportDetails = cur.fetchall()
            return render_template('viewAirports.html', viewAirportDetails=viewAirportDetails)
        if request.form['btn_identifier'] == 'sortSev':
            resultValue = cur.execute("SELECT * FROM view_airports order by total_departing_flights desc")
            viewAirportDetails = cur.fetchall()
            return render_template('viewAirports.html', viewAirportDetails=viewAirportDetails)
        if request.form['btn_identifier'] == 'sortEight':
            resultValue = cur.execute("SELECT * FROM view_airports order by avg_departing_flight_cost desc")
            viewAirportDetails = cur.fetchall()
            return render_template('viewAirports.html', viewAirportDetails=viewAirportDetails)

    if request.method == 'GET':
        resultValue = cur.execute("SELECT * FROM view_airports")
        viewAirportDetails = cur.fetchall()
        return render_template('viewAirports.html', viewAirportDetails=viewAirportDetails)

@app.route('/viewCustomers', methods=['GET', 'POST'])
def viewCustomers():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        if request.form['btn_identifier'] == 'sortOne':
            resultValue = cur.execute("SELECT * FROM view_customers order by customer_name asc")
            viewCustDetails = cur.fetchall()
            return render_template('viewCustomers.html', viewCustDetails=viewCustDetails)
        if request.form['btn_identifier'] == 'sortTwo':
            resultValue = cur.execute("SELECT * FROM view_customers order by avg_rating desc")
            viewCustDetails = cur.fetchall()
            return render_template('viewCustomers.html', viewCustDetails=viewCustDetails)
        if request.form['btn_identifier'] == 'sortThree':
            resultValue = cur.execute("SELECT * FROM view_customers order by location asc")
            viewCustDetails = cur.fetchall()
            return render_template('viewCustomers.html', viewCustDetails=viewCustDetails)
        if request.form['btn_identifier'] == 'sortFour':
            text = request.form['text']
            resultValue = cur.execute("SELECT * FROM view_customers where customer_name like '%" + text + "%'")
            viewCustDetails = cur.fetchall()
            return render_template('viewCustomers.html', viewCustDetails=viewCustDetails)
        if request.form['btn_identifier'] == 'sortSix':
            resultValue = cur.execute("SELECT * FROM view_customers order by is_owner desc")
            viewCustDetails = cur.fetchall()
            return render_template('viewCustomers.html', viewCustDetails=viewCustDetails)
        if request.form['btn_identifier'] == 'sortSev':
            resultValue = cur.execute("SELECT * FROM view_customers order by total_seats_purchased desc")
            viewCustDetails = cur.fetchall()
            return render_template('viewCustomers.html', viewCustDetails=viewCustDetails)
        if request.form['btn_identifier'] == 'back':
            return redirect('/adminHome')

    if request.method == 'GET':
        resultValue = cur.execute("SELECT * FROM view_customers")
        viewCustDetails = cur.fetchall()
        return render_template('viewCustomers.html', viewCustDetails=viewCustDetails)

@app.route('/viewFlights', methods=['GET', 'POST'])
def viewFlights():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        if request.form['btn_identifier'] == 'sortOne':
            resultValue = cur.execute("SELECT * FROM view_flight order by flight_id desc")
            viewFlightDetails = cur.fetchall()
            return render_template('viewFlights.html', viewFlightDetails=viewFlightDetails)
        if request.form['btn_identifier'] == 'sortTwo':
            resultValue = cur.execute("SELECT * FROM view_flight order by airline asc")
            viewFlightDetails = cur.fetchall()
            return render_template('viewFlights.html', viewFlightDetails=viewFlightDetails)
        if request.form['btn_identifier'] == 'sortThree':
            resultValue = cur.execute("SELECT * FROM view_flight order by destination asc")
            viewFlightDetails = cur.fetchall()
            return render_template('viewFlights.html', viewFlightDetails=viewFlightDetails)
        if request.form['btn_identifier'] == 'sortFour':
            text1 = request.form.get('text')
            resultValue = cur.execute("SELECT * FROM view_flight where num_empty_seats < " + text1 )
            viewFlightDetails = cur.fetchall()
            return render_template('viewFlights.html', viewFlightDetails=viewFlightDetails)
        if request.form['btn_identifier'] == 'sortEight':
            resultValue = cur.execute("SELECT * FROM view_flight where num_empty_seats < 100000" )
            viewFlightDetails = cur.fetchall()
            return render_template('viewFlights.html', viewFlightDetails=viewFlightDetails)
        if request.form['btn_identifier'] == 'sortFive':
            resultValue = cur.execute("SELECT * FROM view_flight order by flight_date desc")
            viewFlightDetails = cur.fetchall()
            return render_template('viewFlights.html', viewFlightDetails=viewFlightDetails)
        if request.form['btn_identifier'] == 'sortSix':
            resultValue = cur.execute("SELECT * FROM view_flight order by seat_cost desc")
            viewFlightDetails = cur.fetchall()
            return render_template('viewFlights.html', viewFlightDetails=viewFlightDetails)
        if request.form['btn_identifier'] == 'sortSev':
            resultValue = cur.execute("SELECT * FROM view_flight order by total_spent desc")
            viewFlightDetails = cur.fetchall()
            return render_template('viewFlights.html', viewFlightDetails=viewFlightDetails)
        if request.form['btn_identifier'] == 'back':
            return redirect('/adminHome')

    if request.method == 'GET':
        resultValue = cur.execute("SELECT * FROM view_flight")
        viewFlightDetails = cur.fetchall()
        return render_template('viewFlights.html', viewFlightDetails=viewFlightDetails)



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
            return redirect('/adminHome')

    if request.method == 'GET':
        resultValue = cur.execute("SELECT * FROM view_owners")
        viewOwnersDetails = cur.fetchall()
        return render_template('viewOwners.html', viewOwnersDetails=viewOwnersDetails)

@app.route('/ownerAddProperty', methods = ['GET', 'POST'])
def ownerAddProperty():
    if request.method == 'POST':
        if request.form['btn_identifier'] == 'cancel':
            return redirect('/')
            #Change this when we have owner
        if request.form['btn_identifier'] == 'add':            
            ownerInput = request.form

            name = ownerInput['name']
            email = ownerInput['email']
            description = ownerInput['description']
            street = ownerInput['street']
            city = ownerInput['city']
            state = ownerInput['state']
            zip = ownerInput['zip']
            nearestAirport = ownerInput['nearestAirport']
            distToAirport = ownerInput['distToAirport']
            capacity = ownerInput['capacity']
            cost = ownerInput['cost']

            cur = mysql.connection.cursor()
            cur.execute("call add_property('{}', '{}', '{}', {}, {}, '{}', '{}', '{}', '{}', '{}', {});".format
            (name, email, description, capacity, cost, street, city, state, zip, nearestAirport, distToAirport))
            mysql.connection.commit()

    return render_template('ownerAddProperty.html')


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

@app.route('/bookFlight', methods=['GET', 'POST'])
def bookFlight():
    cur = mysql.connection.cursor()
    # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # conn = MySQLdb.connect(cursorclass=MySQLdb.cursors.DictCursor)
    # cur = conn.cursor()
    if request.method == 'POST':
        

        
        if request.form['btn_identifier'] == 'sortByAirline':
            resultValue = cur.execute('SELECT Airline, flight_id, num_empty_seats FROM view_flight order by airline')
            bookFlightDetails = cur.fetchall()
            return render_template('bookFlight.html', bookFlightDetails=bookFlightDetails)
        
        if request.form['btn_identifier'] == 'sortByFlightNum':
            resultValue = cur.execute('SELECT Airline, flight_id, num_empty_seats FROM view_flight order by CAST(flight_id as UNSIGNED) asc')
            bookFlightDetails = cur.fetchall()
            return render_template('bookFlight.html', bookFlightDetails=bookFlightDetails)

        if request.form['btn_identifier'] == 'submitFlight':
            selectedRow = request.form.get('radio_identifier')
            selectedRow = selectedRow.split(", ")
            numSeatsArr = request.form.getlist('txt_identifier')
            #print(selectedRow)
            airline = selectedRow[0][2:-2]
            flight_id = selectedRow[1][1:-1]
            numSeats = 0

            for ns in numSeatsArr:
                if ns != '0':
                    numSeats = int(ns)

            cur.execute("call book_flight('{}','{}','{}','{}','{}');".format(email, flight_id, airline, numSeats, currentDate))
            resultValue = cur.execute('SELECT Airline, flight_id, num_empty_seats FROM view_flight order by airline')
            bookFlightDetails = cur.fetchall()
            return render_template('bookFlight.html', bookFlightDetails=bookFlightDetails)

    if request.method == 'GET':
        resultValue = cur.execute('SELECT Airline, flight_id, num_empty_seats FROM view_flight')
        bookFlightDetails = cur.fetchall()
        return render_template('bookFlight.html', bookFlightDetails=bookFlightDetails)

    # resultValue = cur.execute('SELECT Airline, flight_id, num_empty_seats FROM view_flight')
    # bookFlightDetails = cur.fetchall()
    # return render_template('bookFlight.html', bookFlightDetails=bookFlightDetails)
    #cur = mysql.connection.cursor()
    #resultValue = cur.execute("SELECT * FROM view_airlines")
    #if resultValue > 0:
        #viewAirlineDetails = cur.fetchall()
        #return render_template('viewAirlines.html', viewAirlineDetails=viewAirlineDetails)

@app.route('/cancelFlight', methods=['GET', 'POST'])
def cancelFlight():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        if request.form['btn_identifier'] == 'sortByAirline':
            resultValue = cur.execute("SELECT Airline_Name, Flight_Num FROM book where Customer = '{}' order by Airline_name".format(email) )
            cancelFlightDetails = cur.fetchall()
            return render_template('cancelFlight.html', cancelFlightDetails=cancelFlightDetails)
        
        if request.form['btn_identifier'] == 'sortByFlightNum':
            resultValue = cur.executecur.execute("SELECT Airline_Name, Flight_Num FROM book where Customer = '{}' order by CAST(flight_num as UNSIGNED) asc".format(email) )
            cancelFlightDetails = cur.fetchall()
            return render_template('cancelFlight.html', cancelFlightDetails=cancelFlightDetails)

        if request.form['btn_identifier'] == 'searchFlight':
            # print(request.form.get('txt_airline'))
            # print(request.form.get('txt_flightNumber'))
            airline = request.form.get('txt_airline')
            flight_num = request.form.get('txt_flightNumber')
            if (airline and flight_num) is not None:
                resultValue = cur.execute("SELECT Airline_Name, Flight_Num FROM book where Customer='{}' AND Airline_Name='{}' AND Flight_Num='{}'".format(email, airline, flight_num))
                cancelFlightDetails = cur.fetchall()
                return render_template('cancelFlight.html', cancelFlightDetails=cancelFlightDetails)
            else:
                resultValue = cur.execute('SELECT Airline_Name, Flight_Num FROM book where Customer = ' + "'" + email + "'")
                cancelFlightDetails = cur.fetchall()
            return render_template('cancelFlight.html', cancelFlightDetails=cancelFlightDetails)

        if request.form['btn_identifier'] =="submitCancelFlight":
            # print(request.form.get('radio_identifier'))
            selectedRow = request.form.get('radio_identifier')
            selectedRow = selectedRow.split(", ")
            airline = selectedRow[0][2:-1]
            flight_num = selectedRow[1][1:-2]
            # print(airline, flight_num)
            # print(("call cancel_flight_booking('{}','{}','{}','{}');".format(email, flight_num, airline, currentDate)))
            resultValue = cur.execute("call cancel_flight_booking('{}','{}','{}','{}');".format(email, flight_num, airline, currentDate))

            resultValue = cur.execute('SELECT Airline_Name, Flight_Num FROM book where Customer = ' + "'" + email + "'")
            cancelFlightDetails = cur.fetchall()
            return render_template('cancelFlight.html', cancelFlightDetails=cancelFlightDetails)
    if request.method == 'GET':
        print(email)
        resultValue = cur.execute('SELECT Airline_Name, Flight_Num FROM book where Customer = ' + "'" + email + "'")
        cancelFlightDetails = cur.fetchall()
        return render_template('cancelFlight.html', cancelFlightDetails=cancelFlightDetails)


@app.route('/setDate')
def setDate():
    if request.method == 'POST':
        currentDate = request.form
        theCurrentDate = currentDate['totalDate']
    return render_template('setDate.html')

if __name__ == '__main__':
    app.run(debug=True)