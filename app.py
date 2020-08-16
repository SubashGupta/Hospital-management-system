
                                                        # HOSPITAL MANAGEMENT SYSTEM BY K. SUBASH GUPTA

from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import join
from sqlalchemy.sql import select
from datetime import date
import sqlite3

app=Flask(__name__)                                                                     # HOSPITAL MANAGEMENT SYSTEM BY K. SUBASH GUPTA
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hosp.sqlite3'
app.config['SECRET_KEY'] = "secret key"

con = sqlite3.connect("hosp.sqlite3")
db = SQLAlchemy(app)                #initializing the SQLAlchemy database.

class userstore(db.Model):      #database fields Creation with constraints for login
    login = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255))
    timestamp = db.Column(db.String(50))

    def __init__(self,name,password,timestamp):
        self.login=login
        self.password=password
        self.timestamp=timestamp

class newpatient(db.Model):             #database fields Creation with constraints for new patient
   patient_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
   patient_SSN_id = db.Column(db.Integer)
   patient_name = db.Column(db.String(100))
   patient_age = db.Column(db.Integer)
   date_of_admission=db.Column(db.String(20))
   type_of_bed=db.Column(db.String(20))
   state = db.Column(db.String(20))
   address=db.Column(db.String(200))
   city=db.Column(db.String(20))
   patient_status=db.Column(db.String(20))

   def __init__(self, id, name, age,date, type, address, state, city):
      self.patient_SSN_id = id
      self.patient_name = name
      self.patient_age = age
      self.date_of_admission =date
      self.type_of_bed=type
      self.address=address
      self.state=state
      self.city=city
      self.patient_status="Active"

#-------------------------------------------------------------------------------------# HOSPITAL MANAGEMENT SYSTEM BY K. SUBASH GUPTA
# basic root page for login

@app.route('/',methods=['GET','POST'])
def beforelogin():
    if request.method == 'POST':    #check the form method is post or not
        session.pop('user',None)            #making sure the seesion user is poped out and made None
        name=request.form['username']
        password=request.form['password']
        #if the name and password are not present in the db then it will show an error
        x =userstore.query.filter_by(login=name , password=password).first()    #checking whether they are in db userstore table or not
        if x is not None :
            session['user']=name                #Making the username as a session for the login  purpose
            with sqlite3.connect("hosp.sqlite3") as con:    #connecting to the hosp.sqlite3 database
                cur = con.cursor()              #creating a cursor object
                from datetime import datetime
                x=datetime.now()
                e="UPDATE userstore SET timestamp = ? WHERE login = ? and password =? ; "
                cur.execute(e,[x,name,password])            #updating the timestamp of the user everytime he/she logs in
                con.commit()                                #saving the changes in the db using commit function
                return redirect(url_for("home"))
        else:                   #Else displaying the credentials are wrong
            flash("Please Re enter the credentials correctly ",'error')
            return redirect(url_for('beforelogin'))         #redirect to the beforelogin page
    return render_template('log.html')
#-------------------------------------------------------------------------------------# HOSPITAL MANAGEMENT SYSTEM BY K. SUBASH GUPTA
# page for logout

@app.route("/logout",methods=["GET","POST"])
def logout():
    session.pop('user',None)            #popping out the created session which was created during login
    flash("logout initiation successful",'error')   #flashing an error message
    return redirect(url_for("beforelogin"))

#-------------------------------------------------------------------------------------# HOSPITAL MANAGEMENT SYSTEM BY K. SUBASH GUPTA
# global user check

@app.before_request
def before_request():
    g.user=None         #setting up global user as None
    if 'user' in session:           #checking if there an user in the session
        g.user=session["user"]          #if user is there then making the user as a global session

#-------------------------------------------------------------------------------------# HOSPITAL MANAGEMENT SYSTEM BY K. SUBASH GUPTA
# home page

@app.route("/home",methods=["GET","POST"])
def home():
    if g.user:                      #checking if global user is there?
        return render_template("ho.html")
    return redirect(url_for("beforelogin"))     #if global user not there then redirecting to beforelogin page.

#-------------------------------------------------------------------------------------# HOSPITAL MANAGEMENT SYSTEM BY K. SUBASH GUPTA
# route page for newpatient entry

@app.route("/newpatient",methods=["GET","POST"])
def new():
    if g.user:              #checking if global user is there?
        return render_template("newpatient.html",newpatient = newpatient.query.all())
    return redirect(url_for("beforelogin"))      #if global user not there then redirecting to beforelogin page.

#-------------------------------------------------------------------------------------# HOSPITAL MANAGEMENT SYSTEM BY K. SUBASH GUPTA
# route for adding the newpatient to the db.

@app.route('/add', methods = ['GET', 'POST'])       #check the form method is post or not
def add():
    if g.user:             #checking if global user is there?
        if request.method == 'POST':            #check the form method is post or not
            if not request.form['patient SSN id'] or not request.form['patient name'] or not request.form['patient age'] or not request.form['date of admission'] or not request.form['type of bed'] or not request.form['address']or not request.form['state']or not request.form['city']:
                flash('Please enter all the fields', 'error')   #if anyone of the condition is not satisfied the flash the message
                return redirect(url_for("new"))     #and redirect to the new function page
            else:
                id=request.form['patient SSN id']       #fetching the patient ssn id into id variable
                ag=request.form['patient age']
                bed=request.form['type of bed']
                if len(id)==9 and len(ag)<4:
                    if bed!="select":
                        patient = newpatient(request.form['patient SSN id'], request.form['patient name'],
                            request.form['patient age'], request.form['date of admission'], request.form['type of bed'], request.form['address'],
                            request.form['state'], request.form['city'])        #sending the data to the class newpatient
                        try:
                            db.session.add(patient)                 #adding the data into the database
                            db.session.commit()                     #saving the added data in the database
                            flash('Patient creation initiated successfully')
                            return redirect(url_for('new'))
                        except:
                            x=1
                    else:
                        flash("Please enter type of Bed" ,'error')          #flashing the message if bed type is not selected
                        return redirect(url_for("new"))
                else:
                    flash("Please type 9 digit Patient SSN id  or a valid age" ,'error')    #flashing the message if 9 digit SSN id is not given as input
                    return redirect(url_for("new"))
        return render_template('newpatient.html')
    return redirect(url_for("beforelogin"))      #if global user not there then redirecting to beforelogin page.

#-------------------------------------------------------------------------------------# HOSPITAL MANAGEMENT SYSTEM BY K. SUBASH GUPTA
# updating an existing patient page with patient id as input

@app.route("/updat",methods=["GET","POST"])
def enterid():
    if g.user:                  #checking if global user is there?
        return render_template("update1.html")
    return redirect(url_for("beforelogin"))          #if global user not there then redirecting to beforelogin page.

@app.route("/updat2",methods=["GET","POST"])
def updat():
    if g.user:
        if request.method == 'POST':            #check the form method is post or not
            if not request.form['patient id']:         #checking if the input patient id message is given or not
                flash('Please enter the Patient id', 'error')
                return redirect(url_for("enterid"))
            else:
                x=''
                id=request.form['patient id']       #fetching the given patient id into the id variable
                x =newpatient.query.filter_by(patient_id = id).all()       #fetching all the patient details into the list x with given id
                if len(x)>0 :       #checking if id is correct
                    return render_template("upd.html",x=x)      #passing the details into the upd.html page
                else:         #if id is wrong
                    flash("Re enter the correct patient id, There is no patient with the given id ", 'error')
                    return redirect(url_for("enterid"))
        return redirect(url_for("enterid"))
    return redirect(url_for("beforelogin"))

@app.route("/updatepatient",methods=["GET","POST"])
def updatepatient():
    if g.user:
        if request.method=="POST":
            id=request.form["patient id"]
            up=newpatient.query.get_or_404(id)
            try:                                        #updating the made changes into the already present fields.
                up.patient_name=request.form['patient name']
                up.patient_age=request.form['patient age']
                up.date_of_admission=request.form['date of admission']
                up.type_of_bed=request.form['type of bed']
                up.address=request.form['address']
                up.state=request.form['state']
                up.city=request.form['city']
                db.session.commit()                     #saving the details into the db.
                flash("Patient update initiated successfully")
                return redirect(url_for("enterid"))
            except:
                x=1
                return render_template('update1.html')
        return render_template('update1.html')
    return redirect(url_for("beforelogin")) #if global user not there then redirecting to beforelogin page.

#-------------------------------------------------------------------------------------# HOSPITAL MANAGEMENT SYSTEM BY K. SUBASH GUPTA
#deleting a patient page with patient id as input

@app.route("/deletepatient",methods=["GET","POST"])
def deletepatient():
    if g.user:
        return render_template("deletepatient.html")
    return redirect(url_for("beforelogin"))

@app.route("/del",methods=["GET","POST"])
def dele():
    if g.user:
        if request.method == 'POST':
            if not request.form['patient id']:              #checking if the input patient id message is given or not
                flash('Please enter all the fields', 'error')
                return redirect(url_for("deletepatient"))
            else:
                x=None
                id=request.form['patient id']            #fetching the given patient id into the id variable
                x =newpatient.query.filter_by(patient_id = id).all()
                if len(x) > 0 :
                    return render_template("del.html",x=x)
                else:
                    flash("Re enter the correct patient id, There are no patients with the given id ", 'error')
                    return redirect(url_for("deletepatient"))
    return redirect(url_for("deletepatient"))

@app.route("/del2",methods=["GET","POST"])
def del2():
    if g.user:
        if request.method=="POST":
            id=request.form["patient id"]
            try:
                newpatient.query.filter_by(patient_id = id).delete()
                db.session.commit()
                flash("Patient deletion initiated successfully")
                return redirect(url_for("deletepatient"))
            except:
                flash('There was an issue updating your task')
                return render_template('deletepatient.html')
        else:
            return render_template('deletepatient.html')
    return redirect(url_for("beforelogin"))
#-------------------------------------------------------------------------------------# HOSPITAL MANAGEMENT SYSTEM BY K. SUBASH GUPTA
# searching for a patient page with patient id as input

@app.route("/searchpatient",methods=["GET","POST"])
def searchpatient():
    if g.user:
        return render_template("search1.html")
    return redirect(url_for("beforelogin"))

@app.route("/search1",methods=["GET","POST"])
def search1():
    if g.user:
        if request.method == 'POST':
            if not request.form['patient id']:                  #checking if the input patient id message is given or not
                flash('Please enter all the fields', 'error')
                return redirect(url_for("searchpatient"))
            else:
                X=''
                id=request.form['patient id']
                x =newpatient.query.filter_by(patient_id = id).all()
                if len(x) > 0 :
                    flash("Patient found")
                    return render_template("sear.html",x=x)
                else:
                    flash("Re enter the correct patient id, There are no patients with the given id ", 'error')
                    return redirect(url_for("searchpatient"))
        return redirect(url_for("searchpatient"))
    return redirect(url_for("beforelogin"))
#-------------------------------------------------------------------------------------# HOSPITAL MANAGEMENT SYSTEM BY K. SUBASH GUPTA
# view all "Active" patients page

@app.route('/viewpatient', methods = ['GET', 'POST'])
def viewallpatients():
    if g.user:
        return render_template('viewpatients.html', newpatient = newpatient.query.filter_by(patient_status = "Active").all())
    return redirect(url_for("beforelogin"))
#-------------------------------------------------------------------------------------
# pharmacy tables creation

class medicinesinput(db.Model):             #database fields Creation with constraints for medicines input from user.
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer)
    medicine_id=db.Column(db.Integer)
    medicine = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    rate=db.Column(db.Integer)
    amount=db.Column(db.Integer)

    def __init__(self, id , patient_id , medicine_id, medicine, quantity,rate,amount):
        self.id=id
        self.patient_id = patient_id
        self.medicine_id=medicine_id
        self.medicine = medicine
        self.quantity = quantity
        self.rate = rate
        self.amount = amount

class pharmacy(db.Model):                   #database fields Creation with constraints for Available medicines
    medicine_id = db.Column(db.Integer, autoincrement=True)
    medicine_name = db.Column(db.Text, primary_key=True)
    quantity_available = db.Column(db.Integer)
    medicine_cost = db.Column(db.Integer)

    def __init__(self,test_id,test_name,test_cost):
        self.medicine_id=medicine_id
        self.medicine_name=medicine_name
        self.quantity_available=quantity_available
        self.medicine_cost=medicine_cost
#-------------------------------------------------------------------------------------# HOSPITAL MANAGEMENT SYSTEM BY K. SUBASH GUPTA
#pharmacy operations pages

#patient details and previous pharmacy history details display and add medicines button
@app.route('/pharmafetch', methods = ['GET', 'POST'])
def pharmafetch():
    if g.user:
        if request.method == 'POST':
            if not request.form['patient id']:
                flash('Please enter the patient id field', 'error')
                return redirect(url_for("pharmafetch"))
            else:
                id=request.form['patient id']
                x =newpatient.query.filter_by(patient_id = id).all()
                y =medicinesinput.query.filter_by(patient_id = id).all()
                if len(x)>0 or len(y)>0 :
                    return render_template("pharmapatientdisplay.html",x=x,y=y,id=id)
                else:
                    flash("Re enter the correct patient id. There are no patients with the given id ", 'error')
                    return redirect(url_for("pharmafetch"))
        return render_template('pharmafetch.html')
    return redirect(url_for("beforelogin"))

#add medicines page
@app.route('/pharmaadd', methods = ['GET', 'POST'])
def pharmaadd():
    if g.user:
        return render_template("pharmaadd.html",pharmacy = pharmacy.query.all())
    return redirect(url_for("beforelogin"))

@app.route("/pharmauserin", methods=["GET","POST"])
def pharmauserin():
    if g.user:
        if request.method=="POST":
            if not request.form["patient id"] or not request.form["medicine"] or not request.form["quantity"]:
                flash('Please enter all the fields', 'error')
                return redirect(url_for("pharmaadd"))
            else:
                patient_id=request.form['patient id']
                medicine=request.form['medicine']
                quantity=request.form['quantity']
                x =newpatient.query.filter_by(patient_id = patient_id).all()
                y=pharmacy.query.filter_by(medicine_name=medicine).all()
                if len(x)>0:
                    if len(y)>0:
                        with sqlite3.connect("hosp.sqlite3") as con:
                            cur = con.cursor()
                                            #query Statement for selecting fields from the pharmacy table
                            s="select medicine_id,medicine_cost,quantity_available from pharmacy where medicine_name=? ; "
                            for row in cur.execute(s,[medicine]):
                                id=row[0]
                                rate=row[1]
                                dup=row[2]
                            cost= int(rate) * int(quantity)
                            b=dup=dup-int(quantity)
                            if b>0 :
                                                    #query Statement for saving given input to the medicinesinput table
                                cur.execute(" INSERT INTO medicinesinput(patient_id,medicine_id,medicine,quantity,rate,amount) values (?,?,?,?,?,?)",(patient_id,id,medicine,quantity,rate,cost,))
                                                    #query Statement for updating the remaining medicines qty in the pharmacy table
                                e="UPDATE pharmacy SET quantity_available = ? WHERE medicine_id = ? ; "
                                cur.execute(e,[dup,id])
                                con.commit()
                                x =newpatient.query.filter_by(patient_id = patient_id).all()
                                p =medicinesinput.query.filter_by(patient_id = patient_id).all()
                                if len(x)>0 and len(y)>0 :
                                    flash('Medicines issued successfully','error')
                                    return render_template("pharmafinaldisp.html",x=x, y=p)
                                else:
                                    flash("Re enter the correct patient id. There are no patients with the given id ", 'error')
                                    return redirect(url_for("pharmaadd"))
                            else:
                                flash("We dont have required amount of medicines for which you requested. Please look at the table and give input",'error')
                                return redirect(url_for("pharmaadd"))

                    else:
                        flash('Please enter the medicine field', 'error')
                        return redirect(url_for("pharmaadd"))
                else:
                    flash("Please enter the correct patient id and all Enter the fields",'error')
                    return redirect(url_for("pharmaadd"))
        return redirect(url_for("pharmaadd"))
    return redirect(url_for("beforelogin"))
#-------------------------------------------------------------------------------------# HOSPITAL MANAGEMENT SYSTEM BY K. SUBASH GUPTA
#diagnostics tables creation

class diaginput(db.Model):              #database fields Creation with constraints for diagnostics input from user
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id=db.Column(db.Integer)
    test_id=db.Column(db.Integer)
    test_name = db.Column(db.Text)
    test_cost= db.Column(db.Integer)

    def __init__(self,id,patient_id,test_id,test_name,test_cost):
        self.id=id
        self.patient_id=patient_id
        self.test_id=test_id
        self.test_name=test_name
        self.test_cost=test_cost

class diagnostics(db.Model):                #database fields Creation with constraints for Available diagnostics
    test_id = db.Column(db.Integer, autoincrement=True)
    test_name = db.Column(db.Text, primary_key=True)
    test_cost = db.Column(db.Integer)

    def __init__(self,test_id,test_name,test_cost):
        self.test_id=test_id
        self.test_name=test_name
        self.test_cost=test_cost
#-------------------------------------------------------------------------------------# HOSPITAL MANAGEMENT SYSTEM BY K. SUBASH GUPTA
#diagnostics operations pages

#patient details and previous diagnostics history details display and add diagnostics button
@app.route('/diagfetch', methods = ['GET', 'POST'])
def diagpatientsearch():
    if g.user:
        if request.method == 'POST':
            if not request.form['patient id']:
                flash('Please enter all the fields', 'error')
                return redirect(url_for("diagpatientsearch"))
            else:
                id=request.form['patient id']
                x =newpatient.query.filter_by(patient_id = id).all()
                y =diaginput.query.filter_by(patient_id = id).all()
                if len(x)>0 or len(y)>0 :
                    return render_template("diagpatientdisplay.html",x=x,y=y)
                else:
                    flash("Re enter the correct patinet id. There are no patients with the given id ", 'error')
                    return redirect(url_for("diagpatientsearch"))
        return render_template("diagpatientsearch.html")
    return redirect(url_for("beforelogin"))

#add diagnostics page
@app.route('/diagsave', methods = ['GET', 'POST'])
def dia():
    if g.user:
        return render_template("diagadd.html")
    return redirect(url_for("beforelogin"))

@app.route("/diaguserin", methods=["GET","POST"])
def diaguserin():
    if g.user:
        if request.method=="POST":
            if not request.form["patient id"] or not request.form["type of test"]:
                flash('Please enter all the fields', 'error')
                return redirect(url_for("dia"))
            else:
                id=request.form['patient id']
                type=request.form['type of test']
                x =newpatient.query.filter_by(patient_id = id).all()
                y =diagnostics.query.filter_by(test_name= type).all()
                if len(x)>0:
                    if len(y)>0:
                        with sqlite3.connect("hosp.sqlite3") as con:
                            cur = con.cursor()
                            s="select test_id,test_cost from diagnostics where test_name=? ; "
                            for row in cur.execute(s,[type]):
                                testid=row[0]
                                cost=row[1]
                            #query Statement for inserting the data into db
                            cur.execute(" INSERT INTO diaginput(patient_id,test_id,test_name,test_cost) values (?,?,?,?)",(id,testid,type,cost,))
                            con.commit()
                            x =newpatient.query.filter_by(patient_id = id).all()
                            y =diaginput.query.filter_by(patient_id = id).all()
                            if len(x)>0 and len(y)>0 :
                                flash('Diagnostics added successfully','error')
                                return render_template("diagfinaldisp.html",x=x,y=y)
                            else:
                                flash("Re enter the correct patient id. There are no patients with the given id ", 'error')
                                return redirect(url_for("dia"))
                    else:
                        flash(" Please enter the diagnostics field",'error')
                        return redirect(url_for("dia"))
                else:
                    flash("Please enter the correct patient id and Enter all the fields", 'error')
                    return redirect(url_for("dia"))
        return redirect(url_for("dia"))
    return redirect(url_for("beforelogin"))
#-------------------------------------------------------------------------------------# HOSPITAL MANAGEMENT SYSTEM BY K. SUBASH GUPTA
#patient bill details displaying page

@app.route("/finalbill",methods=["GET","POST"])
def finalbill():
    if g.user:
        if request.method == 'POST':
            if not request.form['patient id']:
                flash('Please enter all the fields', 'error')
                return redirect(url_for("finalbill"))
            else:
                id=request.form['patient id']
                x=newpatient.query.filter_by(patient_id = id).all()
                z=diaginput.query.filter_by(patient_id = id).all()
                y=medicinesinput.query.filter_by(patient_id = id).all()
                with sqlite3.connect("hosp.sqlite3") as con:
                    cur = con.cursor()
                    #query Statement for admission date of patient and the type of bed he selected
                    da="select date_of_admission ,type_of_bed from newpatient where patient_id=? ; "
                    date1=cur.execute(da,[id])
                    dates=date1.fetchall()
                    date=None
                    datemoney=None
                    for i in dates:
                        date=i[0]
                        type=i[1]
                    if date is not None:
                        doj=[int(i) for i in date.split("-") if i.isdigit()]
                        from datetime import date
                        today = str(date.today())
                        dod=[int(i) for i in today.split("-") if i.isdigit()]
                        d0=date(doj[0],doj[1],doj[2])
                        d1=date(dod[0],dod[1],dod[2])
                        delta=d1-d0
                        diff=delta.days
                        if diff>0:
                            if type=="Single room":
                                datemoney= 8000*int(diff)
                            elif type=="Semi sharing":
                                datemoney= 4000*int(diff)
                            elif type=="General ward":
                                datemoney= 2000*int(diff)
                        elif diff==0:
                            diff=" Zero"
                            datemoney=0
                        else:
                            diff="You are testing Future days"
                            datemoney=0
                        u="select sum(amount) from medicinesinput where patient_id=? ; "
                        #query Statement for total amount of medicines purchased
                        medicinestotal=cur.execute(u,[id])
                        med=medicinestotal.fetchall()
                        for i in med:
                            medi=i[0]
                        s="select sum(test_cost) from diaginput where patient_id=? ; "
                        #query Statement for total amount of Diagnostics purchased
                        diagtotal=cur.execute(s,[id])
                        diag=diagtotal.fetchall()
                        for i in diag:
                            dia=i[0]
                        grandtotal=0
                        if datemoney is not None and dia is not None and medi is not None:
                            grandtotal=dia+medi+datemoney
                        elif datemoney  is not None and dia is not None:
                            grandtotal=datemoney+dia
                        elif datemoney is not None and medi is not None:
                            grandtotal=datemoney+medi
                        else:
                            grandtotal=datemoney
                        if len(x)>0 or len(y)>0 or len(z)>0 :
                            #forwarding the amount details of pharmacy,diagnostics, bed charges
                            flash("data fetched successful",'error')
                            return render_template("finalout.html",x=x,y=y,z=z,diff=diff,medi=medi,dia=dia,today=today,datemoney=datemoney,grandtotal=grandtotal)
                        else:
                            flash("Please enter the correct patient id",'error')
                            return redirect(url_for("finalbill"))

                    else:
                        flash("Please enter the correct Patient id ",'error')
                        return redirect(url_for("finalbill"))
        return render_template('finalbill.html')
    return redirect(url_for("beforelogin"))

#---------------------------------------------------------------------------------------------------------------# HOSPITAL MANAGEMENT SYSTEM BY K. SUBASH GUPTA
#patient status changing page

@app.route("/dbchange",methods=["GET","POST"])
def dbchange():                 #in this function the status of the patient will be changed to "Discharged"
    if g.user:
        if request.method == 'POST':
            if not request.form['patient id']:
                flash('Please enter all the fields', 'error')
                return redirect(url_for("finalbill"))
            else:
                with sqlite3.connect("hosp.sqlite3") as con:
                    cur = con.cursor()
                    #getting form data
                    id=request.form['patient id']
                    disch="Discharged"
                    e="UPDATE newpatient SET patient_status = ? WHERE patient_id = ? ; "        #update status query
                    cur.execute(e,[disch,id])
                    con.commit()
                    flash("Patient Discharge process completed",'error')
        return render_template("ho.html")
    return redirect(url_for("beforelogin"))

#--------------------------------------------------------------------------------------------------------------------# HOSPITAL MANAGEMENT SYSTEM BY K. SUBASH GUPTA

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)



                                                    # HOSPITAL MANAGEMENT SYSTEM BY K. SUBASH GUPTA
