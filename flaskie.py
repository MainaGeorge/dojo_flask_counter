from flask import Flask, render_template, request, url_for, redirect
from csv import DictReader, DictWriter


app = Flask(__name__)
app.debug = True
app.port = 5000


def write_to_csv(list_obj):
    with open('database.csv', 'w') as file_pointer:
        headers = ['Id', 'Story Title', 'User Story', 'Acceptance Criteria',
                   'Business Value', 'Estimation', 'Status']
        csv_writer = DictWriter(file_pointer, fieldnames=headers)
        csv_writer.writeheader()
        for each_dict in list_obj:
            csv_writer.writerow(each_dict)


def read_from_csv(list_obj):
    try:
        with open('database.csv', 'r')as file_pointer:
            csv_reader = DictReader(file_pointer)
            for line in csv_reader:
                list_obj.append(dict(line))
        return list_obj
    except FileNotFoundError:
        return []


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        database = read_from_csv(list())

    elif request.method == 'POST':
        database = read_from_csv(list())
        input_dict = dict(request.form)
        if not input_dict.get('Id'):
            input_dict['Id'] = len(database) + 1
            database.append(input_dict)
            write_to_csv(database)
            database = read_from_csv(list())
        else:
            for each_dict in database:
                if each_dict['Id'] == input_dict['Id']:
                    index_modified = database.index(each_dict)
                    break
            database[index_modified] = input_dict
            write_to_csv(database)
            database = read_from_csv(list())
    return render_template('index.html', database=database)


@app.route('/add-new-story', methods=['GET', 'POST'])
def add_new_story():
    if request.method == 'GET':
        return render_template('add_new_story.html')
    elif request.method == 'POST':
        return redirect(url_for('index'))


@app.route('/update-user-story/<user_number>', methods=['GET', 'POST'])
def update_user_story(user_number=None):
    database = read_from_csv(list())
    user_data = None
    if request.method == 'GET':
        for each_dict in database:
            if each_dict['Id'] == user_number:
                user_data = each_dict
                break
        options = ['Planning', 'Todo', 'In Progress', 'Review', 'Done']
        return render_template('update.html', user_data=user_data, options=options)
    elif request.method == 'POST':
        return redirect(url_for('index'))





if __name__ == '__main__':
    app.run()