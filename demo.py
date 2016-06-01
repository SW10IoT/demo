from flask import render_template, Flask
app = Flask(__name__)

@app.route('/')
@app.route('/overview')
def index():
    return render_template('overview.html')

if __name__ == '__main__':
    app.run(debug = True)
