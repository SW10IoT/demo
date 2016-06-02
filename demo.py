from flask import render_template, Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


################# COMMAND INJECTION ###############################
from flask_wtf import Form
from wtforms.fields import SubmitField, StringField
import subprocess
import os


class Grocery(Form):
    grocery_name = StringField('Grocery')
    add_grocery = SubmitField('Add Grocery')
    reset_groceries = SubmitField('Reset Groceries')

def save_grocery(grocery_name):
    command = 'echo ' + grocery_name + ' >> ' + ' groceries.txt'
    subprocess.call(command, shell=True)

def get_groceries():
    filename = 'groceries.txt'
    if os.path.isfile(filename):
        with open(filename, 'r') as fd:
            for line in fd:
                yield line

def reset_groceries():
    filename = 'groceries.txt'
    if os.path.isfile(filename):
        os.remove(filename)


################### ROUTES #########################
@app.route('/')
@app.route('/overview')
def index():
    return render_template('overview.html')

@app.route('/command_injection', methods=['GET', 'POST'])
def command_injection():
    form = Grocery()
    if form.validate_on_submit():
        if form.reset_groceries.data:
            reset_groceries()
        elif form.grocery_name != '':
            save_grocery(form.grocery_name.data)
            form.grocery_name.data = ''
            groceries = list(get_groceries())
            return render_template('command_injection.html', form=form, groceries=groceries)
    groceries = list(get_groceries())
    return render_template('command_injection.html', form=form, groceries=groceries)

if __name__ == '__main__':
    app.run(debug = True)
