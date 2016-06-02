from flask import render_template, Flask
from command_injection import Grocery, save_grocery, reset_groceries, get_groceries

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


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
