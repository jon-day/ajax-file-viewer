def my_special_func(report, first_name, last_name):
    data = []
    for row in report:
        display_name = {'displayName': row[last_name] + ', ' + row[first_name]}
        row.update(display_name)
        data.append(row)
    return data