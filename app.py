from flask import Flask, make_response, flash, request, redirect, render_template, jsonify
import io
import csv

from my_special_functions import my_special_func_a, my_special_func_web
ALLOWED_EXTENSIONS = {'csv'}
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'supersicrit'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_file():
    return render_template('home.html')

@app.route('/uploadajax', methods=['POST'])
def read_data():
    myfile = request.files.get('file')
    reader = csv.DictReader(io.StringIO(myfile.read().decode('utf-8-sig')))
    fieldnames = reader.fieldnames
    fileData = [row for row in reader]
    return render_template("display_data.html", data=fieldnames)

@app.route('/get_report', methods=['POST'])
def test_route():
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    myfile = request.files['file']
    reader = csv.DictReader(io.StringIO(myfile.read().decode('utf-8-sig')))
    data = my_special_func_web(report=reader, first_name=firstName, last_name=lastName)
    if data:
        fieldnames = data[0].keys()
        print(fieldnames)
        si = io.StringIO()
        cw = csv.DictWriter(si, fieldnames=fieldnames, extrasaction='ignore')
        cw.writeheader()
        [cw.writerow(i) for i in data]

        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=testarino.csv"
        output.headers["Content-type"] = "text/csv"
        return output
    else:
        return "<body>no luck bucko</body>"

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)