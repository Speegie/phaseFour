from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL, MySQLdb
import yaml
from datetime import date, datetime
import re

app = Flask(__name__)
#app.run()

# Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

#cdemilio@tiktok.com
#Charlie Demilio
name, email, status = 'Addison Ray', 'aray@tiktok.com', None

global currentDate
currentDate = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        if request.form['action'] == 'regUser':
            return redirect('/registerIntermediate')
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

@app.route('/registerIntermediate', methods=['GET', "POST"])
def registerIntermediate():
    if request.method == "POST":
        if request.form['but'] == "customer":
            return redirect('/registerCustomer')
        if request.form['but'] == "owner":
            return redirect('/registerOwner')
    
    return render_template("registerIntermediate.html")

@app.route('/registerOwner', methods=['GET', 'POST'])
def registerOwner():
    cur = mysql.connection.cursor()
    if request.method == "POST":
        if request.form['action'] == 'back':
            return redirect('/')
        if request.form['action'] == 'submit':
            cur = mysql.connection.cursor()
            details = request.form

            fname = details["fname"]
            lname = details['lname']
            email = details['email']
            password = details['password']
            confirm = details['confirm']
            phone = details['phone']

            if (password == confirm):
                cur.execute("call register_owner('{}', '{}', '{}', '{}', '{}');".format(email, fname, lname, password, phone))

    return render_template('registerOwner.html')

@app.route('/registerCustomer', methods=['GET', 'POST'])
def registerCustomer():
    cur = mysql.connection.cursor()
    if request.method == "POST":
        if request.form['action'] == 'back':
            return redirect('/')
        if request.form['action'] == 'submit':
            cur = mysql.connection.cursor()
            details = request.form

            fname = details["fname"]
            lname = details['lname']
            email = details['email']
            password = details['password']
            confirm = details['confirm']
            phone = details['phone']
            card = details['card']
            cvv = details['cvv']
            exp = details['exp']

            if (password == confirm):
                cur.execute("call register_owner('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(email, fname, lname, password, phone, card, cvv, exp))

    return render_template('registerCustomer.html')

@app.route('/intermediate', methods=['GET', 'POST'])
def intermediate():
    if request.method == 'POST':
        if request.form['but'] == "admin":
            return redirect('/adminHome')
        if request.form['but'] == 'customer':
            return redirect('/custHome')
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
            name = ""
            email = ""
            status = [0, 0, 0]
            return redirect('/')
    return render_template('adminHome.html') 

@app.route('/ownerHome', methods=['GET', 'POST'])
def ownerHome():
    if request.method == 'POST':
        if request.form['but'] == 'add':
            return redirect('/ownerAddProperty')
        if request.form['but'] == 'remove':
            return redirect('/ownerRemoveProperty')
        if request.form['but'] == 'rate':
            return redirect('/ownerRateCustomer')
        if request.form['but'] == 'delete':
            return redirect('/deleteOwnerAccount')
       
        if request.form['but'] == 'logout':
            name = ""
            email = ""
            status = [0, 0, 0]
            return redirect('/')
    return render_template('ownerHome.html') 

@app.route('/custHome', methods=['GET', 'POST'])
def custHome():
    if request.method == 'POST':
        if request.form['but'] == '1':
            return redirect('/bookFlight')
        if request.form['but'] == '2':
            return redirect('/cancelFlight')
        if request.form['but'] == '3':
            return redirect('/viewProperties')
        if request.form['but'] == '4':
            return redirect('/reserveProperty')
        if request.form['but'] == '5':
            return redirect('/cancelProperty')
        if request.form['but'] == '6':
            return redirect('/reviewProperty')
        if request.form['but'] == '7':
            return redirect('/viewIndividualProperties')
        if request.form['but'] == '8':
            return redirect('/customerRateOwner')
        
       
        if request.form['but'] == 'logout':
            name = ""
            email = ""
            status = [0, 0, 0]
            return redirect('/')
    return render_template('custHome.html') 

@app.route('/scheduleFlight', methods=['GET', 'POST'])
def scheduleFlight():
    cur = mysql.connection.cursor()

    currDate = date.today()


    if request.method == 'POST':
        if request.form['btn_identifier'] == 'sortOne':
            num = request.form.get('num')
            dateStr = request.form.get('date')
            date1 = datetime.strptime(dateStr, '%Y-%m-%d').date()

            airline = request.form.get('line')
            cost = request.form.get('cost')
            fromA = request.form.get('from')
            toA = request.form.get('to')
            capacity = request.form.get('capacity')
            depTime = request.form.get('deptime')
            arrTime = request.form.get('arrtime')
       
            if (currDate > date1):
                return redirect('/error')
            
            resultVal = cur.execute("call schedule_flight('{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, '{}');".format
                (num,
                airline,
                fromA,
                toA,
                depTime,
                arrTime,
                date1,
                cost,
                capacity,
                currDate))
            
            mysql.connection.commit()
            
            # viewAirportDetails = cur.fetchall()
            
            return render_template('scheduleFlight.html', num=num, dateStr=dateStr, airline=airline, cost=cost, fromA=fromA, toA=toA, capacity=capacity
                ,depTime=depTime, arrTime=arrTime, currDate=currDate)


        if request.form['btn_identifier'] == 'back':
            return redirect('/adminHome')
        if request.form['btn_identifier'] == 'viewAll':
            return redirect('/viewAllFlights')
    return render_template('scheduleFlight.html', currDate = currDate)

@app.route('/viewAllFlights', methods=['GET', 'POST'])
def viewAllFlights():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        if request.form['btn_identifier'] == 'back':
            return redirect('/scheduleFlight')

    if request.method == 'GET':
        resultValue = cur.execute("SELECT * FROM Flight")
        viewFlightDetails = cur.fetchall()
        return render_template('viewAllFlights.html', viewFlightDetails=viewFlightDetails)
    return render_template('viewAllFlights.html')

@app.route('/error', methods=['GET', 'POST'])
def error():
    if request.method == 'POST':
        if request.form['btn_identifier'] == 'back':
            return redirect('/scheduleFlight')
    return render_template('error.html')



@app.route('/removeFlight', methods=['GET', 'POST'])
def removeFlight():
    cur = mysql.connection.cursor()

    currDate = date.today()


    if request.method == 'POST':
        if request.form['btn_identifier'] == 'sortOne':
            resultValue = cur.execute("SELECT * FROM Flight order by Airline_Name asc")
            viewFDetails = cur.fetchall()
            return render_template('removeFlight.html', viewFDetails=viewFDetails, currDate=currDate)
        if request.form['btn_identifier'] == 'sortTwo':
            resultValue = cur.execute("SELECT * FROM Flight order by cast(Flight_Num as SIGNED) desc")
            viewFDetails = cur.fetchall()
            return render_template('removeFlight.html', viewFDetails=viewFDetails, currDate=currDate)
        if request.form['btn_identifier'] == 'sortThree':
            resultValue = cur.execute("SELECT * FROM Flight order by cast(Flight_Date as DATE) asc")
            viewFDetails = cur.fetchall()
            return render_template('removeFlight.html', viewFDetails=viewFDetails, currDate=currDate)
        if request.form['btn_identifier'] == 'sortFour':
            resultValue = cur.execute("SELECT * FROM Flight order by cost desc")
            viewFDetails = cur.fetchall()
            return render_template('removeFlight.html', viewFDetails=viewFDetails, currDate=currDate)
        if request.form['btn_identifier'] == 'sortFive':
            resultValue = cur.execute("SELECT * FROM Flight order by capacity desc")
            viewFDetails = cur.fetchall()
            return render_template('removeFlight.html', viewFDetails=viewFDetails, currDate=currDate)

        if (request.form['btn_identifier'] == 'sortDate'):
            datee = request.form.get('date')
            datee2 = request.form.get('date2')
            
            resultValue = cur.execute("SELECT * FROM Flight where Flight_Date between '" + (datee) + "' and '" + datee2 + "'")

            viewFDetails = cur.fetchall()            
            return render_template('removeFlight.html', viewFDetails=viewFDetails, datee=datee, datee2 = datee2, currDate = currDate)
        
        if (request.form['btn_identifier'] == 'sortLine'):
            aline = request.form.get('line')
            print(aline)
            
            resultValue = cur.execute("SELECT * FROM Flight where Airline_Name = '" + (aline) + "'")

            viewFDetails = cur.fetchall()            
            return render_template('removeFlight.html', viewFDetails=viewFDetails, currDate = currDate)
        
        if (request.form['btn_identifier'] == 'sortEight'):
           
            resultValue = cur.execute("SELECT * FROM Flight")

            viewFDetails = cur.fetchall()            
            return render_template('removeFlight.html', viewFDetails=viewFDetails, currDate = currDate)
        
        if (request.form['btn_identifier'] == 'sortNum'):
            numm = request.form.get('num')
            
            resultValue = cur.execute("SELECT * FROM Flight where Flight_Num = " + (numm))

            viewFDetails = cur.fetchall()            
            return render_template('removeFlight.html', viewFDetails=viewFDetails, currDate = currDate)
        

        if request.form['btn_identifier'] == 'remItems':
            index = request.form.get('rem')
            indexInt = int(index)
            # name = request.form.get('date')
            resultVal = cur.execute("SELECT * FROM Flight")

            viewFDetails = cur.fetchall()

            num1 = viewFDetails[indexInt][0]
            name1 = viewFDetails[indexInt][1]

          
            
            resultVal = cur.execute("call remove_flight('{}', '{}', '{}');".format
                (num1,
                name1,
                currDate))
            
            mysql.connection.commit()
            resultVal = cur.execute("SELECT * FROM Flight")

            viewFDetails = cur.fetchall()
            
            return render_template('removeFlight.html', currDate=currDate, viewFDetails=viewFDetails)


        if request.form['btn_identifier'] == 'back':
            return redirect('/adminHome')
        if request.form['btn_identifier'] == 'viewAll':
            return redirect('/viewAllFlights')
    if request.method == 'GET':
        resultValue = cur.execute("SELECT * FROM Flight")
        viewFDetails = cur.fetchall()
        print(viewFDetails)
        return render_template('removeFlight.html', viewFDetails=viewFDetails, currDate=currDate)
    return render_template('removeFlight.html', currDate = currDate)


@app.route('/adminProcessDate', methods=['GET', 'POST'])
def processDate():
    if request.method == 'POST':
        if request.form['btn_identifier'] == 'back':
            return redirect('/adminHome')
        if request.form['btn_identifier'] == 'setDate':
            userDetails = request.form
            setCurrentDate(userDetails['date'])
            return render_template('adminProcessDate.html')
    return render_template('adminProcessDate.html')

def setCurrentDate(dateInput):
    global currentDate
    currentDate = dateInput

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


@app.route('/viewProperties', methods=['GET', 'POST'])
def viewProperties():
    cur = mysql.connection.cursor()
   
    if request.method == 'POST':
        if request.form['btn_identifier'] == 'sortOne':
            resultValue = cur.execute("SELECT * FROM view_properties order by property_name asc")
            viewPropDetails = cur.fetchall()
            return render_template('viewProperties.html', viewPropDetails=viewPropDetails)
        if request.form['btn_identifier'] == 'sortTwo':
            resultValue = cur.execute("SELECT * FROM view_properties order by address asc")
            viewPropDetails = cur.fetchall()
            return render_template('viewProperties.html', viewPropDetails=viewPropDetails)
        if (request.form['btn_identifier'] == 'sortFour'):
            text1 = request.form.get('text')
            text2 = request.form.get('text2')
            
            if (text1 > text2):
                dummy = text2
                text2 = text1
                text1 = dummy
            
            resultValue = cur.execute("SELECT * FROM view_properties where capacity > " + (text1) + " and capacity < " + text2 )

            viewPropDetails = cur.fetchall()            
            return render_template('viewProperties.html', viewPropDetails=viewPropDetails, text1=text1, text2=text2)
       
        if request.form['btn_identifier'] == 'sortEight':
            text1 = 0
            text2 = "infinity"
            resultValue = cur.execute("SELECT * FROM view_properties where capacity < 100000" )
            viewPropDetails = cur.fetchall()
            return render_template('viewProperties.html', viewPropDetails=viewPropDetails, text1=text1, text2=text2)
        if request.form['btn_identifier'] == 'sortFive':
            resultValue = cur.execute("SELECT * FROM view_properties order by average_rating_score desc")
            viewPropDetails = cur.fetchall()
            return render_template('viewProperties.html', viewPropDetails=viewPropDetails)
        if request.form['btn_identifier'] == 'sortSix':
            resultValue = cur.execute("SELECT * FROM view_properties order by capacity desc")
            viewPropDetails = cur.fetchall()
            return render_template('viewProperties.html', viewPropDetails=viewPropDetails)
        if request.form['btn_identifier'] == 'sortSev':
            resultValue = cur.execute("SELECT * FROM view_properties order by cost_per_night desc")
            viewPropDetails = cur.fetchall()
            return render_template('viewProperties.html', viewPropDetails=viewPropDetails)
        if request.form['btn_identifier'] == 'back':
            return redirect('/custHome')

    if request.method == 'GET':
        resultValue = cur.execute("SELECT * FROM view_properties")
        viewPropDetails = cur.fetchall()
        return render_template('viewProperties.html', viewPropDetails=viewPropDetails)

@app.route('/viewIndividualProperties', methods=['GET', 'POST'])
def viewIProperties():
    cur = mysql.connection.cursor()
   
    if request.method == 'POST':
       
        if (request.form['btn_identifier'] == 'ownEmail'):
            text1 = request.form.get('text')
            text2 = request.form.get('text2')
            
           
            cur.execute("call view_individual_property_reservations('{}', '{}');".format(str(text2), str(text1)))
            mysql.connection.commit()

            resultVal = cur.execute("SELECT * from view_individual_property_reservations;")

            viewPropDetails = cur.fetchall()
            return render_template('viewIProp.html', viewPropDetails=viewPropDetails, text1=text1, text2=text2)
       
       
        if request.form['btn_identifier'] == 'back':
            return redirect('/custHome')

    if request.method == 'GET':
        resultValue = cur.execute("call view_individual_property_reservations('{}', '{}');".format("*", "*"))
        mysql.connection.commit()
        viewPropDetails = cur.fetchall()
        return render_template('viewIProp.html', viewPropDetails=viewPropDetails)

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
            return redirect('/ownerHome')
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

#Needs to be fixed a lot with email and current date
@app.route('/ownerRemoveProperty', methods = ['GET', 'POST'])
def ownerRemoveProperty():
    if request.method == 'POST':
        if request.form['btn_identifier'] == 'back':
            return redirect('/ownerHome')
            #Change this when we have owner
        if request.form['btn_identifier'] == 'removeProperty':            
            selectedRow = request.form.get('radio_identifier')
            
            selectedRow = selectedRow.split(", ")
            name = selectedRow[0][2:-1]
            email = "arthurread@gmail.com"
            currentDate = "2021-10-15"
            cur = mysql.connection.cursor()
            cur.execute("call remove_property('{}', '{}', '{}');".format(name, email, currentDate))
            mysql.connection.commit()

            ownerEmail = "arthurread@gmail.com"
            cur = mysql.connection.cursor()
            cur.execute("SELECT Property_Name, Descr, Capacity, Cost, (SELECT CONCAT(Street, ', ', City, ', ', State, ' ', Zip)) as Address FROM property where Owner_Email like '%" + ownerEmail + "%'")
            viewPropertyDetails = cur.fetchall()
            return render_template('ownerRemoveProperty.html', viewPropertyDetails = viewPropertyDetails)

    if request.method == 'GET':
        ownerEmail = "arthurread@gmail.com"
        cur = mysql.connection.cursor()
        cur.execute("SELECT Property_Name, Descr, Capacity, Cost, (SELECT CONCAT(Street, ', ', City, ', ', State, ' ', Zip)) as Address FROM property where Owner_Email like '%" + ownerEmail + "%'")
        viewPropertyDetails = cur.fetchall()
        return render_template('ownerRemoveProperty.html', viewPropertyDetails = viewPropertyDetails)


@app.route('/ownerRateCustomer', methods = ['GET', 'POST'])
def ownerRateCustomer():
    if request.method == 'POST':
        if request.form['btn_identifier'] == 'back':
            return redirect('/ownerHome')
            #Change this when we have owner
        if request.form['btn_identifier'] == 'submit':
            cur = mysql.connection.cursor()
            ownerEmail = "cbing10@gmail.com"
            cur.execute("select Start_Date, cEmail, pName, Address, Score from owners_rate_customers right join (select pName, oEmail, cEmail, Start_Date, (SELECT CONCAT(Street, ', ', City, ', ', State, ' ', Zip)) as Address from property right join (select Property_Name as pName, Owner_Email as oEmail, Customer as cEmail, Start_Date, End_Date from reserve where Owner_Email = '" + ownerEmail + "') as outerOne on Owner_Email = oEmail and Property_Name = pName where oEmail = '" + ownerEmail + "') as outerTwo on Customer = cEmail;")
            ratingDetails = cur.fetchall()

            newInput = request.form.getlist('txt_identifier')
            for i in range(len(newInput)):
                if newInput[i] != 'None' and int(newInput[i]) != ratingDetails[i][4]:
                    newInput[i] = int(newInput[i])
                    cur.execute("call owner_rates_customer('{}', '{}', {}, '{}');".format(ownerEmail, ratingDetails[i][1], newInput[i], currentDate))
                    mysql.connection.commit()

            cur.execute("select Start_Date, cEmail, pName, Address, Score from owners_rate_customers right join (select pName, oEmail, cEmail, Start_Date, (SELECT CONCAT(Street, ', ', City, ', ', State, ' ', Zip)) as Address from property right join (select Property_Name as pName, Owner_Email as oEmail, Customer as cEmail, Start_Date, End_Date from reserve where Owner_Email = '" + ownerEmail + "') as outerOne on Owner_Email = oEmail and Property_Name = pName where oEmail = '" + ownerEmail + "') as outerTwo on Customer = cEmail;")
            ratingDetails = cur.fetchall()
            return render_template('ownerRateCustomer.html', ratingDetails = ratingDetails)

    if request.method == 'GET':
        ownerEmail = "cbing10@gmail.com"
        cur = mysql.connection.cursor()
        cur.execute("select Start_Date, cEmail, pName, Address, Score from owners_rate_customers right join (select pName, oEmail, cEmail, Start_Date, (SELECT CONCAT(Street, ', ', City, ', ', State, ' ', Zip)) as Address from property right join (select Property_Name as pName, Owner_Email as oEmail, Customer as cEmail, Start_Date, End_Date from reserve where Owner_Email = '" + ownerEmail + "') as outerOne on Owner_Email = oEmail and Property_Name = pName where oEmail = '" + ownerEmail + "') as outerTwo on Customer = cEmail;")
        ratingDetails = cur.fetchall()
        return render_template('ownerRateCustomer.html', ratingDetails = ratingDetails)



@app.route('/deleteOwnerAccount', methods = ['GET', 'POST'])
def deleteOwnerAccount():
    if request.method == 'POST':
        ownerEmail = "jwayne@gmail.com"
        if request.form['btn_identifier'] == 'back':
            return redirect('/ownerHome')
            #Change when have owner home
        if request.form['btn_identifier'] == 'deleteAccount':
            cur = mysql.connection.cursor()
            cur.execute("call remove_owner('" + ownerEmail + "');")#.format(ownerEmail))
            print("Done")
            mysql.connection.commit()
            return render_template('deleteOwnerAccount.html')
        #Test if this works!!!!
    if request.method == 'GET':
        return render_template('deleteOwnerAccount.html')
    




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
            return redirect('/adminHome')

    if request.method == 'GET':
        resultValue = cur.execute("SELECT * FROM view_airlines")
        viewAirlinesDetails = cur.fetchall()
        return render_template('viewAirlines.html', viewAirlinesDetails=viewAirlinesDetails)

@app.route('/bookFlight', methods=['GET', 'POST'])
def bookFlight():
    cur = mysql.connection.cursor()
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
            airline = selectedRow[0][2:-2]
            flight_id = selectedRow[1][1:-1]
            numSeats = 0

            for ns in numSeatsArr:
                if ns != '0':
                    numSeats = int(ns)

            cur.execute("call book_flight('{}','{}','{}','{}','{}');".format(email, flight_id, airline, numSeats, currentDate))
            mysql.connection.commit()
            resultValue = cur.execute('SELECT Airline, flight_id, num_empty_seats FROM view_flight order by airline')
            bookFlightDetails = cur.fetchall()
            return render_template('bookFlight.html', bookFlightDetails=bookFlightDetails)

        if request.form['but'] == 'back':
            return redirect('/custHome')

    if request.method == 'GET':
        resultValue = cur.execute('SELECT Airline, flight_id, num_empty_seats FROM view_flight')
        bookFlightDetails = cur.fetchall()
        return render_template('bookFlight.html', bookFlightDetails=bookFlightDetails)

@app.route('/cancelFlight', methods=['GET', 'POST'])
def cancelFlight():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        if request.form['btn_identifier'] == 'sortByAirline':
            resultValue = cur.execute("SELECT Airline_Name, Flight_Num FROM book where Customer = '{}' order by Airline_name".format(email) )
            cancelFlightDetails = cur.fetchall()
            return render_template('cancelFlight.html', cancelFlightDetails=cancelFlightDetails)
        
        if request.form['btn_identifier'] == 'sortByFlightNum':
            resultValue = cur.execute("SELECT Airline_Name, Flight_Num FROM book where Customer = '{}' order by CAST(flight_num as UNSIGNED) asc".format(email) )
            cancelFlightDetails = cur.fetchall()
            return render_template('cancelFlight.html', cancelFlightDetails=cancelFlightDetails)

        if request.form['btn_identifier'] == 'searchFlight':
            airline = request.form.get('txt_airline')
            flight_num = request.form.get('txt_flightNumber')
            if (airline) != "":
                resultValue = cur.execute("SELECT Airline_Name, Flight_Num FROM book where Customer='{}' AND Airline_Name like '%{}%'".format(email, airline))
                cancelFlightDetails = cur.fetchall()
                return render_template('cancelFlight.html', cancelFlightDetails=cancelFlightDetails)
            elif flight_num != "":
                resultValue = cur.execute("SELECT Airline_Name, Flight_Num FROM book where Customer='{}' AND Flight_Num ='{}'".format(email, flight_num))
                cancelFlightDetails = cur.fetchall()
                return render_template('cancelFlight.html', cancelFlightDetails=cancelFlightDetails)
            else:
                resultValue = cur.execute('SELECT Airline_Name, Flight_Num FROM book where Customer = ' + "'" + email + "'")
                cancelFlightDetails = cur.fetchall()
                return render_template('cancelFlight.html', cancelFlightDetails=cancelFlightDetails)

        if request.form['btn_identifier'] =="submitCancelFlight":
            selectedRow = request.form.get('radio_identifier')
            selectedRow = selectedRow.split(", ")
            airline = selectedRow[0][2:-1]
            flight_num = selectedRow[1][1:-2]
            resultValue = cur.execute("call cancel_flight_booking('{}','{}','{}','{}');".format(email, flight_num, airline, currentDate))
            mysql.connection.commit()
            resultValue = cur.execute('SELECT Airline_Name, Flight_Num FROM book where Customer = "{}" and Was_Cancelled=0'.format(email))
            cancelFlightDetails = cur.fetchall()
            return render_template('cancelFlight.html', cancelFlightDetails=cancelFlightDetails)

        if request.form['but'] == 'back':
            return redirect('/custHome')

    if request.method == 'GET':
        resultValue = cur.execute('SELECT Airline_Name, Flight_Num FROM book where Customer = "{}" and Was_Cancelled=0'.format(email))
        cancelFlightDetails = cur.fetchall()
        return render_template('cancelFlight.html', cancelFlightDetails=cancelFlightDetails)

@app.route('/reserveProperty', methods=['GET', 'POST'])
def reserveProperty():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        if request.form['btn_identifier'] == 'sortByName':
            resultValue = cur.execute('SELECT (reserve.Property_Name), (reserve.Owner_Email), Capacity from reserve natural join property order by reserve.Property_Name')
            reservePropertyDetails = cur.fetchall()
            return render_template('reserveProperty.html', reservePropertyDetails=reservePropertyDetails)
        
        if request.form['btn_identifier'] == 'sortByEmail':
            resultValue = cur.execute('SELECT (reserve.Property_Name), (reserve.Owner_Email), Capacity from reserve natural join property order by reserve.Owner_Email')
            reservePropertyDetails = cur.fetchall()
            return render_template('reserveProperty.html', reservePropertyDetails=reservePropertyDetails)

        if request.form['btn_identifier'] == 'sortByCapacity':
            resultValue = cur.execute('SELECT (reserve.Property_Name), (reserve.Owner_Email), Capacity from reserve natural join property order by Capacity')
            reservePropertyDetails = cur.fetchall()
            return render_template('reserveProperty.html', reservePropertyDetails=reservePropertyDetails)
        
        if request.form['btn_identifier'] == 'searchProperty':
            sDate = request.form.get('txt_sDate')
            eDate = request.form.get('txt_eDate')
            resultValue = cur.execute("SELECT (reserve.Property_Name), (reserve.Owner_Email), Capacity from reserve natural join property \
                where ('{}' < Start_Date and '{}' < Start_Date) or  ('{}' > End_Date and '{}' < Start_Date)".format(sDate, eDate, sDate, eDate))
            reservePropertyDetails = cur.fetchall()
            return render_template('reserveProperty.html', reservePropertyDetails=reservePropertyDetails)

        if request.form['btn_identifier'] == 'submitReserve':
            selectedRow = request.form.get('radio_identifier')
            selectedRow = selectedRow.split(", ")
            numGuestArr = request.form.getlist('txt_identifier')
            propertyName = selectedRow[0][2:-1]
            ownerEmail = selectedRow[1][1:-1]
            numGuest = 0

            for ng in numGuestArr:
                if ng != '0':
                    numGuest = int(ng)

            cur.execute("call reserve_property('{}','{}','{}','{}','{}','{}','{}');"\
                .format(propertyName, ownerEmail, email, sDate, eDate, numGuest, currentDate))
            mysql.connection.commit()
           
            resultValue = cur.execute('SELECT (reserve.Property_Name), (reserve.Owner_Email), Capacity from reserve natural join property\
                where reserve.Start_Date > "{}"'.format(currentDate))
            reservePropertyDetails = cur.fetchall()
            return render_template('reserveProperty.html', reservePropertyDetails=reservePropertyDetails)
        
        if request.form['but'] == 'back':
            return redirect('/custHome')

    if request.method == 'GET':
        resultValue = cur.execute('SELECT (reserve.Property_Name), (reserve.Owner_Email), Capacity from reserve natural join property\
            where reserve.Start_Date > "{}"'.format(currentDate))
        reservePropertyDetails = cur.fetchall()
        return render_template('reserveProperty.html', reservePropertyDetails=reservePropertyDetails)

@app.route('/cancelProperty',  methods=['GET', 'POST'])
def cancelProperty():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        
        if request.form['btn_identifier'] == 'cancelProperty':
            selectedRow = request.form.get('radio_identifier')
            selectedRow = selectedRow.split(", ")
            propertyName = selectedRow[3][1:-1]
            ownerEmail = selectedRow[4][1:-1]
            cur.execute("call cancel_property_reservation('{}','{}','{}','{}');"
                .format(propertyName, ownerEmail, email, currentDate))
            mysql.connection.commit()
            resultValue = cur.execute("SELECT reserve.Start_Date, reserve.Property_Name, reserve.Owner_Email, concat(Street, City, State, Zip)\
            from reserve natural join property where Customer='{}' and Was_Cancelled=0;".format(email))
            cancelPropertyDetails = cur.fetchall()
            return render_template('cancelProperty.html', cancelPropertyDetails=cancelPropertyDetails)
        
        if request.form['but'] == 'back':
            return redirect('/custHome')

    if request.method == 'GET':
        resultValue = cur.execute("SELECT reserve.Start_Date, reserve.Property_Name, reserve.Owner_Email, concat(Street, City, State, Zip)\
         from reserve natural join property where Customer='{}' and Was_Cancelled=0;".format(email))
        cancelPropertyDetails = cur.fetchall()
        return render_template('cancelProperty.html', cancelPropertyDetails=cancelPropertyDetails)

@app.route('/reviewProperty', methods=['GET', 'POST'])
def reviewProperty():
    if request.method == 'POST':
        if request.form['btn_identifier'] == 'back':
            return redirect('/custHome')
            #Change this when we have owner
        if request.form['btn_identifier'] == 'submit':
            cur = mysql.connection.cursor()
            customerEmail = "aray@tiktok.com"
            cur.execute("SELECT start_date, reserve.property_name, reserve.owner_email, CONCAT(street, ', ', city, ', ', state, ' ', zip) as address FROM reserve LEFT JOIN property ON reserve.property_name = property.property_name where customer = '" + customerEmail + "'")
            reviewDetails = cur.fetchall()

            details = request.form

            description = details['content']
            score = details['score']

            newInput = request.form.getlist('radio_identifier')
            for i in range(len(newInput)):
                if newInput[i] != 'None':
                    cur.execute("call customer_review_property('{}', '{}', '{}', '{}', '{}', '{}');".format(reviewDetails[i][1], reviewDetails[i][2], customerEmail, description, score, currentDate))
                    mysql.connection.commit()

            cur.execute("SELECT start_date, reserve.property_name, reserve.owner_email, CONCAT(street, ', ', city, ', ', state, ' ', zip) as address FROM reserve LEFT JOIN property ON reserve.property_name = property.property_name where customer = '" + customerEmail + "'")
            ratingDetails = cur.fetchall()
            return render_template('reviewProperty.html', reviewDetails = reviewDetails)

    if request.method == 'GET':
        customerEmail = "aray@tiktok.com"
        cur = mysql.connection.cursor()
        cur.execute("SELECT start_date, reserve.property_name, reserve.owner_email, CONCAT(street, ', ', city, ', ', state, ' ', zip) as address FROM reserve LEFT JOIN property ON reserve.property_name = property.property_name where customer = '" + customerEmail + "'")
        reviewDetails = cur.fetchall()
        return render_template('reviewProperty.html', reviewDetails = reviewDetails)

@app.route('/customerRateOwner', methods = ['GET', 'POST'])
def customerRateOwner():
    if request.method == 'POST':
        if request.form['btn_identifier'] == 'back':
            return redirect('/custHome')
            #Change this when we have owner
        if request.form['btn_identifier'] == 'submit':
            cur = mysql.connection.cursor()
            customerEmail = "cbing10@gmail.com"
            cur.execute("SELECT start_date as 'Reservation Date', property.owner_email, property.property_name, CONCAT(street, ', ', city, ', ', state, ' ', zip) as address from property LEFT JOIN reserve on reserve.property_name = property.property_name where customer = '" + customerEmail + "'")
            ratingDetails = cur.fetchall()

            newInput = request.form.getlist('txt_identifier')
            for i in range(len(newInput)):
                if newInput[i] != 'None':
                    newInput[i] = int(newInput[i])
                    cur.execute("call customer_rates_owner('{}', '{}', {}, '{}');".format(customerEmail, ratingDetails[i][1], newInput[i], currentDate))
                    mysql.connection.commit()

            cur.execute("SELECT start_date as 'Reservation Date', property.owner_email, property.property_name, CONCAT(street, ', ', city, ', ', state, ' ', zip) as address from property LEFT JOIN reserve on reserve.property_name = property.property_name where customer = '" + customerEmail + "'")
            ratingDetails = cur.fetchall()
            return render_template('customerRateOwner.html', ratingDetails = ratingDetails)

    if request.method == 'GET':
        customerEmail = "cbing10@gmail.com"
        cur = mysql.connection.cursor()
        cur.execute("SELECT start_date as 'Reservation Date', property.owner_email, property.property_name, CONCAT(street, ', ', city, ', ', state, ' ', zip) as address from property LEFT JOIN reserve on reserve.property_name = property.property_name where customer = '" + customerEmail + "'")
        ratingDetails = cur.fetchall()
        return render_template('customerRateOwner.html', ratingDetails = ratingDetails)

if __name__ == '__main__':
    app.run(debug=True)