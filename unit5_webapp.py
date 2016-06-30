from flask import Flask, flash, redirect, render_template, \
     request, url_for

app = Flask(__name__)
import appconfig
app.secret_key = appconfig.SECRET_KEY

from flask_sqlalchemy import SQLAlchemy

from flask_wtf import Form
from wtforms import DecimalField
from wtforms.validators import DataRequired

import pandas as pd
import numpy as np
import pycountry
# import matplotlib.pyplot as plt

from datetime import datetime
import statistics

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.sqlalchemy_database_uri= appconfig.SQLALCHEMY_DATABASE_URI
app.sqlalchemy_track_modifications = appconfig.SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)

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

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/result")
def show_result():
    df = pd.read_excel('ebola_data_db_format.xlsx')
    df = df[df["Country"].map(lambda x: x.find("2") == -1)]

    colors = []
    for index, row in df.iterrows():
        if row["Country"] == "United States of America":
            row["Country"] = "United States"
        df.loc[index, 'Country'] = pycountry.countries.get(name=row["Country"]).alpha3
        if row["value"] > 10000:
            colors.append('A')
        elif row["value"] > 9000:
            colors.append('B')
        elif row["value"] > 8000:
            colors.append('C')
        elif row["value"] > 7000:
            colors.append('D')
        elif row["value"] > 6000:
            colors.append('E')
        elif row["value"] > 5000:
            colors.append('F')
        elif row["value"] > 4000:
            colors.append('G')
        elif row["value"] > 3000:
            colors.append('H')
        elif row["value"] > 2000:
            colors.append('I')
        elif row["value"] > 1000:
            colors.append('J')
        elif row["value"] > 100:
            colors.append('K')
        elif row["value"] > 0:
            colors.append('L')
        elif row["value"] == 0:
            colors.append('M')
        else:
            colors.append('Error')
    df["Colors"] = colors
    filtered_df = df[df["Indicator"]=="Cumulative number of confirmed Ebola cases"]
    values_color_data = filtered_df[['Country', 'Colors', 'value']]
    color_data = filtered_df[['Country', 'Colors']]
    return render_template('result.html', values_color_data=values_color_data, color_data=color_data, chart_title="Cumulative number of confirmed Ebola cases")

@app.route('/result', methods=['POST'])
def show_result_post():
    df = pd.read_excel('ebola_data_db_format.xlsx')
    df = df[df["Indicator"]==request.form['parameter_name']]
    date_range = request.form["daterange"].split(" - ")
    date_range = list(map(lambda x: x.replace("-", ""), date_range))
    df = df[(df['Date'] >= date_range[0]) & (df['Date'] <= date_range[1])]
    df = df[df["Country"].map(lambda x: x.find("2") == -1)]

    colors = []
    for index, row in df.iterrows():
        if row["Country"] == "United States of America":
            row["Country"] = "United States"
        df.loc[index, 'Country'] = pycountry.countries.get(name=row["Country"]).alpha3
        if row["value"] > 10000:
            colors.append('A')
        elif row["value"] > 9000:
            colors.append('B')
        elif row["value"] > 8000:
            colors.append('C')
        elif row["value"] > 7000:
            colors.append('D')
        elif row["value"] > 6000:
            colors.append('E')
        elif row["value"] > 5000:
            colors.append('F')
        elif row["value"] > 4000:
            colors.append('G')
        elif row["value"] > 3000:
            colors.append('H')
        elif row["value"] > 2000:
            colors.append('I')
        elif row["value"] > 1000:
            colors.append('J')
        elif row["value"] > 100:
            colors.append('K')
        elif row["value"] > 0:
            colors.append('L')
        elif row["value"] == 0:
            colors.append('M')
        else:
            colors.append('Error')
    df["Colors"] = colors
    values_data = df[['Country', 'Colors', 'value']]
    color_data = df[['Country', 'Colors']]
    return render_template('result.html', values_color_data=values_data, color_data=color_data, chart_title=request.form["parameter_name"])


if __name__ == "__main__":
    app.debug = True
    app.run()
