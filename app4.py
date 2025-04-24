from random import randint
from flask import Flask, render_template, request, redirect, url_for, session
import secrets
from io import BytesIO
from PyPDF2 import PdfReader

# Initialisation de l'application Flask
app = Flask(__name__)
app.secret_key = secrets.token_hex()  # Clé secrète pour sécuriser les sessions

# Liste des utilisateurs avec leurs identifiants
utilisateurs = [
    {"nom": "admin", "mdp": "1234"},
    {"nom": "marie", "mdp": "nsi"},
    {"nom": "paul", "mdp": "azerty"}
]

# Route pour compter les mots dans un fichier PDF
@app.route('/compteur_pdf', methods=["POST", "GET"])
def compteur_pdf():
    if request.method == "POST":
        if 'file' not in request.files:  # Vérifie si un fichier a été téléchargé
            return render_template("compteur_pdf.html", error="Aucun fichier n'a été téléchargé.")

        file = request.files['file']
        if file.filename == '':  # Vérifie si le fichier est vide
            return render_template("compteur_pdf.html", error="Le fichier téléchargé est vide.")

        try:
            # Charger le fichier PDF et compter les mots
            pdf_file = BytesIO(file.read())
            reader = PdfReader(pdf_file)
            word_count = 0
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    word_count += len(text.split())
            return render_template("compteur_pdf.html", word_count=word_count)
        except Exception as e:
            return render_template("compteur_pdf.html", error=f"Erreur lors du traitement du PDF : {e}")
    else:
        return render_template("compteur_pdf.html")

# Route pour calculer la somme des chiffres d'un nombre
@app.route('/somme', methods=["GET", "POST"])
def somme():
    if request.method == "POST":
        donnees = request.form
        a = int(donnees.get('nombre'))
        somme = 0
        for i in str(a):  # Parcourt chaque chiffre du nombre
            somme += int(i)
        session['somme'] = somme  # Stocke la somme dans la session
        return render_template("somme.html", somme=somme)
    else:
        return render_template("somme.html")

# Route pour le jeu du nombre mystère
@app.route('/jeu', methods=["GET", "POST"])
def jeu():
    if request.method == "POST":
        reponse = int(request.form.get('nombre'))  # Récupère la réponse de l'utilisateur
        session['essais'].append(reponse)
        if reponse == session['nb']:
            session['en_cours'] = False
            message = "Bravo, c'est gagné !"
        elif reponse < session['nb']:
            message = "Non, c'est plus !"
        else:
            message = "Non, c'est moins !"

        session['nb_essais'] -= 1  # Décrémente le nombre d'essais restants

        if session['nb_essais'] == 0:
            session['en_cours'] = False
            message = "C'est perdu !"
        return render_template('nombre-mystere.html', message=message)
    else:
        # Initialisation du jeu
        nb_mystere = randint(0, 100)
        session['nb'] = nb_mystere
        session['en_cours'] = True
        session['nb_essais'] = 10
        session['essais'] = []
        return render_template('nombre-mystere.html')

# Route pour la page d'accueil
@app.route("/")
def index():
    return render_template("index.html")

# Fonction pour rechercher un utilisateur dans la liste
def recherche_utilisateur(nom_utilisateur, mot_de_passe):
    for utilisateur in utilisateurs:
        if utilisateur['nom'] == nom_utilisateur and utilisateur['mdp'] == mot_de_passe:
            return utilisateur
    return None

# Route pour la connexion
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        donnees = request.form
        nom = donnees.get('nom')
        mdp = donnees.get('mdp')

        utilisateur = recherche_utilisateur(nom, mdp)

        if utilisateur is not None:  # Si l'utilisateur est trouvé
            session['nom_utilisateur'] = utilisateur['nom']
            return redirect(url_for('index'))
        else:
            return redirect(request.url)
    else:
        if 'nom_utilisateur' in session:  # Si l'utilisateur est déjà connecté
            return redirect(url_for('index'))
        return render_template("login.html")

# Route pour la déconnexion
@app.route('/logout')
def logout():
    session.pop('nom_utilisateur', None)  # Supprime l'utilisateur de la session
    return redirect(url_for('login'))

# Route pour compter les visites d'une page
@app.route("/compteur")
def compteur():
    if "compteur" not in session:
        session['compteur'] = 1
    else:
        session['compteur'] += 1
    nb_visites = session['compteur']
    return f"Vous avez visité cette page {nb_visites} fois"

# Route pour le traitement des données utilisateur
@app.route("/traitement", methods=["POST", "GET"])
def traitement():
    if request.method == "POST":
        donnees = request.form
        nom = donnees.get('nom')
        mdp = donnees.get('mdp')
        if nom == 'admin' and mdp == '1234':  # Vérifie les identifiants
            return render_template("traitement.html", nom_utilisateur=nom)
        else:
            return render_template("traitement.html")
    else:
        return redirect(url_for('index'))

# Lancement de l'application en mode debug
if __name__ == '__main__':
    app.run(debug=True)