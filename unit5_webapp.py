from flask import Flask, flash, redirect, render_template, \
     request, url_for
app = Flask(__name__)
import appconfig
app.secret_key = appconfig.SECRET_KEY

from flask_sqlalchemy import SQLAlchemy

from flask_wtf import Form
from wtforms import DecimalField
from wtforms.validators import DataRequired


from datetime import datetime
import statistics

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.sqlalchemy_database_uri= appconfig.SQLALCHEMY_DATABASE_URI
app.sqlalchemy_track_modifications = appconfig.SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)

class Formdata(db.Model):
    __tablename__ = 'formdata'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    firstname = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    age = db.Column(db.Integer)
    income = db.Column(db.Integer)
    satisfaction = db.Column(db.Integer)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)

    def __init__(self, firstname, email, age, income, satisfaction, q1, q2):
        self.firstname = firstname
        self.email = email
        self.age = age
        self.income = income
        self.satisfaction = satisfaction
        self.q1 = q1
        self.q2 = q2

db.create_all()

class DataForm(Form):
    number_of_records = DecimalField('Number of records:', validators=[DataRequired()])

@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/form")
def show_form():
    return render_template('form.html')

@app.route("/dataform", methods=['GET', 'POST'])
def data_form():
    form = DataForm()
    if form.validate_on_submit():
        flash("Validation successful")
        return redirect('/result')
    return render_template("data_form.html", form=form)


@app.route("/raw")
def show_raw():
    fd = db.session.query(Formdata).all()
    return render_template('raw.html', formdata=fd)


@app.route("/result")
def show_result():
    fd_list = db.session.query(Formdata).all()

    # Some simple statistics for sample questions
    satisfaction = []
    q1 = []
    q2 = []
    for el in fd_list:
        satisfaction.append(int(el.satisfaction))
        q1.append(int(el.q1))
        q2.append(int(el.q2))

    if len(satisfaction) > 0:
        mean_satisfaction = statistics.mean(satisfaction)
    else:
        mean_satisfaction = 0

    if len(q1) > 0:
        mean_q1 = statistics.mean(q1)
    else:
        mean_q1 = 0

    if len(q2) > 0:
        mean_q2 = statistics.mean(q2)
    else:
        mean_q2 = 0

    # Prepare data for google charts
    data = [['Satisfaction', mean_satisfaction], ['Python skill', mean_q1], ['Flask skill', mean_q2]]

    return render_template('result.html', data=data)


@app.route("/save", methods=['POST'])
def save():
    # Get data from FORM
    firstname = request.form['firstname']
    email = request.form['email']
    age = request.form['age']
    income = request.form['income']
    satisfaction = request.form['satisfaction']
    q1 = request.form['q1']
    q2 = request.form['q2']

    # Save the data
    fd = Formdata(firstname, email, age, income, satisfaction, q1, q2)
    db.session.add(fd)
    db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run()
