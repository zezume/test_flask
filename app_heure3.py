from random import randint

from flask import Flask, render_template, request, redirect, url_for, session
import secrets
import requests
from io import BytesIO
from PyPDF2 import PdfReader

app = Flask(__name__)
app.secret_key = secrets.token_hex()

utilisateurs = [
    {"nom": "admin", "mdp": "1234"},
    {"nom": "marie", "mdp": "nsi"},
    {"nom": "paul", "mdp": "azerty"}
]


@app.route('/compteur_pdf', methods=["POST", "GET"])
def compteur_pdf():
    if request.method == "POST":
        if 'file' not in request.files:
            return render_template("compteur_pdf.html", error="Aucun fichier n'a été téléchargé.")

        file = request.files['file']
        if file.filename == '':
            return render_template("compteur_pdf.html", error="Le fichier téléchargé est vide.")

        try:
            # Charger le fichier PDF en mémoire
            pdf_file = BytesIO(file.read())
            reader = PdfReader(pdf_file)

            # Extraire le texte et compter les mots
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
@app.route('/somme', methods=["GET", "POST"])
def somme():
    if request.method == "POST":
        donnees = request.form
        a = int(donnees.get('nombre'))
        somme=0
        for i in str(a):
            print(i)
            somme += int(i)
            session['somme'] = somme
        return render_template("somme.html", somme=somme)
    else:
        return render_template("somme.html")

@app.route('/jeu', methods=["GET", "POST"])
def jeu():
    if request.method == "POST":
        #traiter les données
        reponse = int(request.form.get('nombre'))
        session['essais'].append(reponse)
        if reponse == session['nb']:
            session['en_cours'] = False
            message = "Bravo, c'est gagné !"
        elif reponse < session['nb']:
            message = "Non, c'est plus !"
        else:
            message = "Non, c'est moins !"

        session['nb_essais'] = session['nb_essais'] - 1

        if session['nb_essais'] == 0:
            session['en_cours'] = False
            message = "C'est perdu !"
        print(session)
        return render_template('nombre-mystere.html', message=message)
    else:
        nb_mystere = randint(0, 100)
        session['nb'] = nb_mystere
        session['en_cours'] = True
        session['nb_essais'] = 10
        session['essais'] = []
        print(session)
        # affichage du formulaire
        return render_template('nombre-mystere.html')

@app.route("/")
def index():
    return render_template("index.html")

def recherche_utilisateur(nom_utilisateur, mot_de_passe):
    for utilisateur in utilisateurs:
        if utilisateur['nom'] == nom_utilisateur and utilisateur['mdp'] == mot_de_passe:
            return utilisateur
    return None

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        donnees = request.form
        nom = donnees.get('nom')
        mdp = donnees.get('mdp')

        utilisateur = recherche_utilisateur(nom, mdp)

        if utilisateur is not None:
            print("utilisateur trouvé")
            session['nom_utilisateur'] = utilisateur['nom']
            print(session)
            return redirect(url_for('index'))
        else:
            print("utilisateur inconnu")
            return redirect(request.url)
    else:
        print(session)
        if 'nom_utilisateur' in session:
            return redirect(url_for('index'))
        return render_template("login.html")

@app.route('/logout')
def logout():
    print(session)
    session.pop('nom_utilisateur', None)
    print(session)
    return redirect(url_for('login'))

@app.route("/compteur")
def compteur():
    if "compteur" not in session:
        session['compteur'] = 1
    else:
        session['compteur'] = session['compteur'] + 1
    print(session)
    nb_visites = session['compteur']
    return f"Vous avez visité cette page {nb_visites} fois"


@app.route("/traitement", methods=["POST", "GET"])
def traitement():
    if request.method == "POST":
        donnees = request.form
        nom = donnees.get('nom')
        mdp = donnees.get('mdp')
        if nom == 'admin' and mdp == '1234':
            return render_template("traitement.html", nom_utilisateur=nom)
        else:
            return render_template("traitement.html")
    else:
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
