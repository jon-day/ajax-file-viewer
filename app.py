from flask import Flask, make_response, flash, request, redirect, render_template, jsonify
import io
import csv
from flask_debugtoolbar import DebugToolbarExtension
from my_special_functions import my_special_func_a, my_special_func_web
UPLOAD_FOLDER = 'uploads\\'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xlsx', 'xls'}
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'supersicrit'
toolbar = DebugToolbarExtension(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/exportFile', methods=['GET'])
def index():
    data = my_special_func_a()
    if data:
        fieldnames = data[0].keys()
        
        si = io.StringIO()
        cw = csv.DictWriter(si, fieldnames=fieldnames, extrasaction='ignore')    
        [cw.writerow(i) for i in data]
        
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=report.csv"
        output.headers["Content-type"] = "text/csv"
        return output
    else:
        return "no luck bucko"


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            reader = csv.DictReader(io.StringIO(file.read().decode('utf-8')))
            data = [row for row in reader]

            return jsonify(data)
    return render_template('home.html')


@app.route('/uploadajax', methods=['POST'])
def read_data():
    myfile = request.files.get('file')
    reader = csv.DictReader(io.StringIO(myfile.read().decode('utf-8-sig')))
    fieldnames = reader.fieldnames
    fileData = [row for row in reader]
    return render_template("display_data.html", data=fieldnames)

@app.route('/test_route', methods=['POST'])
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