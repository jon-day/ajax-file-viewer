from flask import Flask, make_response, request, render_template
import io
import csv

# This is some example business logic that we want to hook up to flask
from my_special_functions import my_special_func

app = Flask(__name__)
app.debug = False
app.config['SECRET_KEY'] = 'supersicrit'
# I want a max file size of 32 MB.
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024
# My 'business logic' only works on csv files. So we need what they can upload.
ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('home.html')


# this route will get the fieldnames of the uploaded csv file
@app.route('/get_fieldnames', methods=['POST'])
def read_data():
    file = request.files.get('file')
    if file and allowed_file(file.filename):
        reader = csv.DictReader(io.StringIO(file.read().decode('utf-8-sig')))
        fieldnames = reader.fieldnames
        return render_template("reveal and populate drop-downs.html", data=fieldnames)
    else:
        return "<h1>Wrong File Type. Please use a csv file.</h1>"

# this route will take the selected fieldnames and generate the output file for the user.
@app.route('/generate_report', methods=['POST'])
def test_route():
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    file = request.files['file']
    if file and allowed_file(file.filename):
        reader = csv.DictReader(io.StringIO(file.read().decode('utf-8-sig')))
        data = my_special_func(report=reader, first_name=first_name, last_name=last_name)
        if data:
            fieldnames = data[0].keys()
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
