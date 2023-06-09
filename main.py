from flask import Flask, render_template, request
import joblib
import numpy as np
import random
import matplotlib
import matplotlib.pyplot as plt
import base64
import io
import os
app = Flask(__name__)
df = [0, 0, 0]
matplotlib.use('Agg')

rf = joblib.load('IndiVolt/rfmodel.joblib')
def generate_pie_chart(data, labels):

    fig, ax = plt.subplots()
    ax.pie(data, labels=labels)

    
    chart_path = os.path.join(app.static_folder, 'pie.png')
    plt.savefig(chart_path, format='png', bbox_inches='tight')
    return chart_path

@app.route('/', methods = ['GET'])
def index():
    return render_template('ab.html')
@app.route('/plan', methods = ['GET', 'POST'])
def plan():
    return render_template('plan.html')
@app.route('/submit', methods = ['POST', 'GET'])
def submit():
    norooms = request.form['norooms']
    nopeople = request.form['nopeople']
    area = request.form['area']
    acs = request.form['acs']
    tvs = request.form['tvs']
    incomes = request.form['income']
    kids = request.form['kids']
    actime = request.form['actime']
    df[0] = actime
    tvtime = request.form['tvtime']
    df[1] = tvtime
    arr = [[norooms, nopeople, area, acs, tvs,1, incomes, kids, 1,actime, tvtime]]
    pred = rf.predict(arr)
    df[2] = pred
    pred = int(pred[0])
    
    #make pred global
    
    i = random.uniform(0.5, 1.5)
    rencost  = np.round(pred - (12*i/100)*pred)
    profit = np.round(int(pred) - rencost)
    percent = np.round((profit/int(pred))*100)
    data = [pred, profit]
    labels = ['Current Cost', 'Your savings']
    chart_data = generate_pie_chart(data, labels)
    return render_template('dashboard.html', currcost = pred, rencost = rencost, profit = profit, percent = percent)
@app.route('/output', methods = ['GET', 'POST'])
def output():
    target =float( request.form['target'])
    pred = df[2]
    scale = target/pred
    #get hours for ac and tv with new scale
    actime = float(df[0])
    newactime = np.round(actime*scale)[0]
    tvtime = float(df[1])
    newtvtime = np.round(tvtime*scale)[0]

    return render_template('output.html', newactime = newactime, newtvtime = newtvtime, actime=actime, tvtime=tvtime)

if __name__ == '__main__':
    app.run(debug=True, port=3000)