from flask import Flask, render_template, request
import joblib
import numpy as np
import random

app = Flask(__name__)
rf = joblib.load('Indivolt/rfmodel.joblib')

@app.route('/', methods = ['GET'])
def index():
    return render_template('ab.html')
@app.route('/submit', methods = ['POST'])
def submit():
    norooms = request.form['norooms']
    nopeople = request.form['nopeople']
    area = request.form['area']
    acs = request.form['acs']
    tvs = request.form['tvs']
    incomes = request.form['income']
    kids = request.form['kids']
    actime = request.form['actime']
    tvtime = request.form['tvtime']
    arr = [[norooms, nopeople, area, acs, tvs,1, incomes, kids, 1,actime, tvtime]]
    pred = rf.predict(arr)
    pred = int(pred[0])
    i = random.uniform(0.5, 1.5)
    print(i)
    rencost  = np.round(pred - (12*i/100)*pred)
    profit = np.round(int(pred) - rencost)
    percent = np.round((profit/int(pred))*100)
    return render_template('dashboard.html', currcost = pred, rencost = rencost, profit = profit, percent = percent)
    


if __name__ == '__main__':
    app.run(debug=True, port=3000)