from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import pyodbc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@CHE/FlaskDB?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
db = SQLAlchemy(app, engine_options={'echo':True})

#---------------class ----Model-----class will become model if it inherits from db.Model class
#------ https://docs.sqlalchemy.org/en/20/tutorial/index.html  -- more info------------
class Customer(db.Model):
    Id = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(50))
    Email = db.Column(db.String(50))
    Phone = db.Column(db.Integer)
    def __init__(self, name, email, phone) -> None:
        super().__init__()
        self.Name = name
        self.Email = email
        self.Phone = phone
#----------------in terminal >> py -m flask shell   >>> db.create_all()---------

#-------function/actions------for--- CRUD--Operations----------------------------
@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    all_customers = Customer.query.all() # select * from dbo.customers
    return render_template('index.html', customers= all_customers, title='Customers Info')
#----------------------Create---------------------------------------------------
@app.route('/create', methods=['POST'])
def create():
    if request.method=='POST':
        # capture data from html-form
        name = request.form['name']   
        email = request.form['email']   
        phone = request.form['phone']   
        # create new customer object
        new_cust_obj = Customer(name, email, phone)
        db.session.add(new_cust_obj)
        db.session.commit()  # save changes in database
    return redirect(url_for('index'))
#----------------------Update/Edit---------------------------------------------------
@app.route('/update/[id]', methods=['GET', 'POST'])
def update():
    if request.method =='POST':
        # capture data from html-form
        Id_from_form = request.form['id']
        Cust_in_DB  = Customer.query.get(Id_from_form)
        Cust_in_DB.Name = request.form['name']   
        Cust_in_DB.Email = request.form['email']   
        Cust_in_DB.Phone = request.form['phone']   
        # update customer 
        db.session.commit()  # save changes in database
    return redirect(url_for('index'))

#------------------Delete--------------------------------------
@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
        # capture poor guy from database
        poor_cust  = Customer.query.get(id)
        db.session.delete(poor_cust)
        db.session.commit()  # save changes in database
        return redirect(url_for('index'))

#--------------------------------------------------------------
if __name__=='__main__':
    app.run(debug=True)