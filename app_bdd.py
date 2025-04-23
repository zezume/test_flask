from flask import Flask, render_template, request, redirect, url_for
from bdd_class import db, init_app, User, Calculation
import plotly.express as px

# Initialisation de l'application Flask
app = Flask(__name__)

# Configuration de la base de données PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ugo:password@localhost:5432/perso'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données avec l'application Flask
init_app(app)

# Route pour la page d'accueil
@app.route('/')
def index():
    # Rend la page d'accueil (indexbdd.html)
    return render_template('indexbdd.html')

# Route pour ajouter un utilisateur
@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        # Récupération des données du formulaire
        user_name = request.form['name']
        user_email = request.form['email']
        # Création d'un nouvel utilisateur
        user = User(name=user_name, email=user_email)
        # Ajout de l'utilisateur à la base de données
        db.session.add(user)
        db.session.commit()
        # Redirection vers la liste des utilisateurs
        return redirect(url_for('list_users'))
    # Affiche le formulaire pour ajouter un utilisateur
    return render_template('add_user.html')

# Route pour afficher la liste des utilisateurs
@app.route('/list_users')
def list_users():
    # Récupération de tous les utilisateurs depuis la base de données
    users = User.query.all()
    # Rend la page avec la liste des utilisateurs
    return render_template('users.html', users=users)

# Route pour effectuer un calcul
@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        # Récupération des données du formulaire
        user_id = int(request.form['user_id'])
        user_input = int(request.form['number'])
        word_count = int(request.form['word_count'])
        # Exemple de calcul (ajout de 10 au nombre saisi)
        result = user_input + 10
        # Création d'une nouvelle entrée de calcul
        calculation = Calculation(user_id=user_id, user_input=user_input, result=result, word_count=word_count)
        # Ajout du calcul à la base de données
        db.session.add(calculation)
        db.session.commit()
        # Redirection vers la liste des calculs
        return redirect(url_for('list_calculations'))
    # Récupération de tous les utilisateurs pour le formulaire
    users = User.query.all()
    # Affiche le formulaire pour effectuer un calcul
    return render_template('calculate.html', users=users)

# Route pour afficher la liste des calculs
@app.route('/list_calculations')
def list_calculations():
    # Récupération de tous les calculs depuis la base de données
    calculations = Calculation.query.all()
    # Rend la page avec la liste des calculs
    return render_template('calculations.html', calculations=calculations)

# Route pour afficher les statistiques
@app.route('/statistics')
def statistics():
    # Récupération des 5 utilisateurs ayant effectué le plus de requêtes
    stats = db.session.query(User.name, db.func.count(Calculation.id).label('request_count')) \
        .join(Calculation, User.id == Calculation.user_id) \
        .group_by(User.name) \
        .order_by(db.desc('request_count')) \
        .limit(5) \
        .all()

    # Préparation des données pour le graphique
    names = [stat[0] for stat in stats]
    counts = [stat[1] for stat in stats]

    # Création d'un graphique à barres avec Plotly
    fig = px.bar(x=names, y=counts, labels={'x': 'Utilisateurs', 'y': 'Nombre de requêtes'}, title='Top 5 des utilisateurs par requêtes')
    graph_html = fig.to_html(full_html=False)

    # Rend la page avec le graphique
    return render_template('statistics.html', graph_html=graph_html)

# Lancement de l'application en mode debug
if __name__ == '__main__':
    app.run(debug=True)