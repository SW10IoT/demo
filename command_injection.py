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
