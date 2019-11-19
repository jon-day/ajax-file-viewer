import csv

my_file = 'report.csv'


def my_special_func_a(report, first_name, last_name):
    with open(report, newline='', encoding='utf-8-sig') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        data = []
        for row in csv_reader:
            display_name = {'displayName': row[last_name] + ', ' + row[first_name]}
            row.update(display_name)
            data.append(row)
        return data

def my_special_func_web(report, first_name, last_name):
    data = []
    for row in report:
        display_name = {'displayName': row[last_name] + ', ' + row[first_name]}
        row.update(display_name)
        data.append(row)
    return data


myData = my_special_func_a(report=my_file, first_name='first name', last_name='last name')