from flask import Flask, make_response, request, render_template
import io
import csv

from my_special_functions import my_special_func
ALLOWED_EXTENSIONS = {'csv'}
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'supersicrit'
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/uploadajax', methods=['POST'])
def read_data():
    file = request.files.get('file')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        reader = csv.DictReader(io.StringIO(file.read().decode('utf-8-sig')))
        fieldnames = reader.fieldnames
        fileData = [row for row in reader]
        return render_template("display_data.html", data=fieldnames)
    else:
        return "<h1>Wrong File Type. Please use a csv file.</h1>"

@app.route('/get_report', methods=['POST'])
def test_route():
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    file = request.files['file']
    if file and allowed_file(file.filename):
        reader = csv.DictReader(io.StringIO(file.read().decode('utf-8-sig')))
        data = my_special_func(report=reader, first_name=firstName, last_name=lastName)
        if data:
            fieldnames = data[0].keys()
            print(fieldnames)
            si = io.StringIO()
            cw = csv.DictWriter(si, fieldnames=fieldnames, extrasaction='ignore')
            cw.writeheader()
            [cw.writerow(i) for i in data]

            output = make_response(si.getvalue())
            output.headers["Content-Disposition"] = "attachment; filename=output.csv"
            output.headers["Content-type"] = "text/csv"
            return output
        else:
            return "<h1>Unable to process the Data</h1>"
    else:
        return "<h1>Wrong File Type. Please use a csv file.</h1>"

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)