from flask import Flask, render_template, request
import joblib

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
    pred = str(pred[0])+"rupees"
    return render_template('ab.html', pred = pred)
    


if __name__ == '__main__':
    app.run(debug=True, port=3000)