from flask import render_template, Flask, request, make_response, send_file, Markup
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
import sys

from command_injection import Grocery, save_grocery, reset_groceries, get_groceries


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
@app.route('/overview')
def index():
    return render_template('overview.html')

@app.route('/sql_injection_raw')
def sql_injection_raw():
    param = request.args.get('param', 'not set')
    result = db.engine.execute(param)
    return render_template('sql_injection.html', result=result)

@app.route('/sql_injection_filtering')
def sql_injection_filtering():
    param = request.args.get('param', 'not set')
    Session = sessionmaker(bind=db.engine)
    session = Session()
    result = session.query(User).filter("username={}".format(param))
    return render_template('sql_injection.html', result=result)

@app.route('/path_traversal', methods=['GET'])
def path_traversal():
    image_name = request.args.get('image_name')
    print(image_name)
    print('s', os.path.join(os.getcwd(), image_name))
    if not image_name:
        return 404
    print('s', os.path.join(os.getcwd(), image_name))
    return send_file(os.path.join(os.getcwd(), image_name))

@app.route('/xss', methods=['GET'])
def xss():
    param = request.args.get('param', 'not set')

    html = open('templates/xss.html').read()
    response = make_response(html.replace('{{ param }}', param))
    return response

@app.route('/xss_sanitised', methods=['GET'])
def xss_sanitised():
    param = request.args.get('param', 'not set')

    param = Markup.escape(param)

    html = open('templates/xss.html').read()
    response = make_response(html.replace('{{ param }}', param))
    return response

@app.route('/danger')
def danger():
    return render_template('danger.html')

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
