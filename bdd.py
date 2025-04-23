from flask import Flask, render_template, request, redirect, url_for
from db_connection import db, init_app, User, Calculation
import plotly.express as px

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ugo:password@localhost:5432/perso'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
init_app(app)

@app.route('/')
def index():
    return render_template('indexbdd.html')

@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        user_name = request.form['name']
        user_email = request.form['email']
        user = User(name=user_name, email=user_email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('list_users'))
    return render_template('add_user.html')

@app.route('/list_users')
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        user_input = int(request.form['number'])
        word_count = int(request.form['word_count'])
        result = user_input + 10  # Example calculation
        calculation = Calculation(user_id=user_id, user_input=user_input, result=result, word_count=word_count)
        db.session.add(calculation)
        db.session.commit()
        return redirect(url_for('list_calculations'))
    users = User.query.all()
    return render_template('calculate.html', users=users)

@app.route('/list_calculations')
def list_calculations():
    calculations = Calculation.query.all()
    return render_template('calculations.html', calculations=calculations)

@app.route('/statistics')
def statistics():
    stats = db.session.query(User.name, db.func.count(Calculation.id).label('request_count')) \
        .join(Calculation, User.id == Calculation.user_id) \
        .group_by(User.name) \
        .order_by(db.desc('request_count')) \
        .limit(5) \
        .all()

    names = [stat[0] for stat in stats]
    counts = [stat[1] for stat in stats]

    fig = px.bar(x=names, y=counts, labels={'x': 'Users', 'y': 'Number of Requests'}, title='Top 5 Users by Requests')
    graph_html = fig.to_html(full_html=False)

    return render_template('statistics.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)