
import os
from flask import Flask, render_template, request, redirect, session
import pyodbc
import re
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

app.secret_key = 'your_secret_key'

def connection():
    
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=KANCHANA;DATABASE=train;Trusted_Connection=yes')
    #conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+KANCHANA +';DATABASE=' + train +';UID=' +'Trusted_Connection=yes')

 
    return conn
@app.route('/')
def page():
    return render_template('starting.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    try:
        msg = ''
        if request.method=='GET':
            return render_template('login.html', car = {})
        if request.method == 'POST':
            name = request.form["name"]
            password = request.form["password"]
            conn = connection()
            cursor = conn.cursor()        
            cursor.execute('SELECT id FROM accounts WHERE username = ? AND password = ?', (name, password ))
            account = cursor.fetchone()

            if account !=0 and account !='' and account!= None:
                return render_template('home.html')
            
            else:
                msg='Incorrect username / password !'
                return render_template('index.html',msg=msg)

           
    except Exception as e:
            # Handle exceptions here
            print(f"Error: {str(e)}")
            msg = 'An error occurred. Please try again.'
    return render_template('login.html', msg=msg)
                       
    
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''

    if request.method == 'GET':
        return render_template("register.html", car = {})
    if request.method == 'POST':
        name = request.form["name"]
        password = request.form["password"]
        email = request.form["email"]
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dbo.accounts (username,password, email) VALUES ( ?, ?, ?)",name, password, email)
        conn.commit()
        conn.close()
        msg='your registration successfully completed'
        return render_template('index.html',msg=msg)

        #msg = 'You have successfully registered !'

############################################################ Reservation For Train Ticket Details ########################################

@app.route('/reservation_form',methods =['GET', 'POST'])
def chance():
    #try:
        trains=[]
        if request.method == 'GET':
            return render_template('reservation_form.html',train={})
        if request.method == 'POST':
            try:
                First_name = request.form["First_name"]
                Last_name = request.form["Last_name"]
                From_station = request.form["From_station"]
                To_station = request.form["To_station"]
                Phone_Number = request.form["Phone_Number"]
                dateofjourney= request.form["date"]
                conn = connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO reservation.user_reservation_details (First_name,Last_name, From_station,To_station,Phone_Number,dateofjourney,paidamount) VALUES ( ?, ?, ?,?,?,?,?)",First_name, Last_name, From_station,To_station,Phone_Number,dateofjourney,459)
                conn.commit()
                conn.close()
                return redirect('/upi')

            except:
                msg='Please enter all second details'   
                return render_template('index.html', msg=msg)
            
    
#########################################################################################################################################
    
########################################################### Credit card details (payment) ###############################################

@app.route('/upi',methods =['GET', 'POST'])

def upi():
    #try:
        trains=[]
        if request.method == 'GET':
            return render_template('upi.html',train={})
        if request.method == 'POST':
            #try:
                cname = request.form["cname"]
                ccnum = request.form["ccnum"]
                expmonth = request.form["expmonth"]
                expyear = request.form["expyear"]
                cvv = request.form["cvv"]
                conn = connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO reservation.credit_card_details (cname,ccnum, expmonth,expyear,cvv,amount) VALUES ( ?, ?, ?,?,?,?)",cname, ccnum,expmonth ,expyear,cvv,459)
                conn.commit()
                conn.close()
                msg='your registration successfully completed'
                return redirect('/booking_hist')
           # except:
                #msg='Please enter all  second details'   
               # return render_template('index.html',msg=msg )
            
            
    


#########################################################################################################################################

################################################################## booking histroy ######################################################

@app.route('/booking_hist')
def booking_histoty():
   trains=[]
   conn = connection()
   cursor = conn.cursor()
   cursor.execute('select * from reservation.user_reservation_details ')
   for row in cursor.fetchall():
    trains.append({"First_name": row[1]+' '+row[2],  "From_station": row[3], "To_station": row[4],"Phone_Number":row[5], "dateofjourney":row[6] ,"paidamount":row[7]})
   return render_template("booking_hist.html",trains=trains)

#########################################################################################################################################

#########################################################################################################################################

################################################################## cancel ticket ######################################################

@app.route('/cancel')
def cancel():
   msg='Are you sure you want to cancel the ticket'
   return render_template('cancel.html',msg=msg)

@app.route('/check_update',methods =['GET', 'POST'])
def check_update():
    try:
        if request.method == 'GET':
                return render_template('cancel_update.html',train={})
        if request.method == 'POST':
                try:
                    First_name = request.form["First_name"]
                    Phone_Number = request.form["Phone_Number"]
                    conn = connection()
                    cursor = conn.cursor()
                    cursor.execute("update reservation.user_reservation_details set paidamount=0 where Phone_Number= ?",Phone_Number )
                    conn.commit()
                    conn.close()
                    return render_template('home.html')

                except:
                    msg='Please enter all second details'   
                    return render_template('index.html', msg=msg)
        return render_template('home.html')
    except:
        msg='error'
        return render_template('index.html',msg=msg)


#########################################################################################################################################



@app.route('/profile')
def profile():
    return render_template("profile.html")



@app.route('/test')
def logout():
        return render_template("test.html")

@app.route('/displaytrains')
def search():
    cars = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM RESERVATION.TRAIN")
    for row in cursor.fetchall():
        cars.append({"TR_NO": row[0], "TR_NAME": row[1], "FROM_STN": row[2], "TO_STN": row[3]})
    conn.close()


    


@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name

@app.route('/home')
def home():
	return render_template("home.html")


@app.route('/Trains_between_stations')
def Trains_between_stations():
   trains=[]
   conn = connection()
   cursor = conn.cursor()
   cursor.execute('select * from RESERVATION.TRAIN')
   for row in cursor.fetchall():
    trains.append({"TR_NO": row[0], "TR_NAME": row[1], "FROM_STN": row[2], "TO_STN": row[3],"SEATS":row[4]})
   return render_template("Trains_between_stations.html",trains=trains)
   

@app.route('/find_train', methods =['GET', 'POST'])
def find_train():
    trains=[]
    msg = ''
    if request.method=='GET':
         return render_template('find_train.html', train = {})
    if request.method == 'POST':
        trains=[]
        FROM_STN = request.form["FROM_STN"]
        TO_STN = request.form["TO_STN"]
        conn = connection()
        cursor = conn.cursor()        
        cursor.execute('SELECT TR_NO FROM RESERVATION.TRAIN WHERE FROM_STN = ? AND TO_STN = ?', (FROM_STN, TO_STN ))
        account = cursor.fetchone()
        if account !=0 and account !='' and account!= None:
            cursor.execute('select * from RESERVATION.TRAIN WHERE FROM_STN = ? AND TO_STN = ?', (FROM_STN, TO_STN ))
            for row in cursor.fetchall():
              trains.append({"TR_NO": row[0], "TR_NAME": row[1], "FROM_STN": row[2], "TO_STN": row[3],"SEATS":row[4]})
            return render_template("Trains_between_stations.html",trains=trains)
        else:
             msg='something went wrong'
             return render_template('index.html',msg=msg)

        conn.commit()
        conn.close()
    msg='No trains available'   
    return render_template('index.html',msg=msg)


@app.route('/view_trains')
def view_train():
   trains=[]
   conn = connection()
   cursor = conn.cursor()
   cursor.execute('select * from RESERVATION.TRAIN')
   for row in cursor.fetchall():
    trains.append({"TR_NO": row[0], "TR_NAME": row[1], "FROM_STN": row[2], "TO_STN": row[3],"SEATS":row[4]})
   return render_template("Trains_between_stations.html",trains=trains)



################################################################search by train number############################################
@app.route('/search_num', methods =['GET', 'POST'])
def search_num():
    trains=[]
    msg = ''
    if request.method=='GET':
         return render_template('search_num.html', train = {})
    if request.method == 'POST':
        trains=[]
        TR_NO = request.form["TR_NO"]
        conn = connection()
        cursor = conn.cursor()        
        cursor.execute('SELECT TR_NO FROM RESERVATION.TRAIN WHERE TR_NO = ? ', (TR_NO ))
        account = cursor.fetchone()
        if account !=0 and account !='' and account!= None:
            cursor.execute('select * from RESERVATION.TRAIN WHERE TR_NO = ? ', (TR_NO ))
            for row in cursor.fetchall():
              trains.append({"TR_NO": row[0], "TR_NAME": row[1], "FROM_STN": row[2], "TO_STN": row[3],"SEATS":row[4]})
            return render_template("Trains_between_stations.html",trains=trains)
        else:
             msg='something went wrong'
             return render_template('index.html',msg=msg)

        conn.commit()
        conn.close()
    msg='No trains available'   
    return render_template('index.html',msg=msg)






            


# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application 
	# on the local development server.
	app.run(debug=True)
