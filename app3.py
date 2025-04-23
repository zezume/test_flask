from flask import Flask, render_template, request, redirect, url_for

# Initialisation de l'application Flask
app = Flask(__name__)

# Définition de la route pour l'URL racine ('/')
@app.route('/')
def bonjour():
    # Cette fonction est appelée lorsque l'utilisateur accède à la page d'accueil ('/').
    # Elle rend le modèle HTML 'bonjour.html'.
    return render_template('bonjour.html')

# Liste des élèves avec leurs informations (nom, prénom, classe)
liste_eleves = [
    {'nom': 'Dupont', 'prenom': 'Jean', 'classe': '2A'},
    {'nom': 'Dupont', 'prenom': 'Jeanne', 'classe': 'TG2'},
    {'nom': 'Marchand', 'prenom': 'Marie', 'classe': '2A'},
    {'nom': 'Martin', 'prenom': 'Adeline', 'classe': '1G1'},
    {'nom': 'Dupont', 'prenom': 'Lucas', 'classe': '2A'}
]

# Définition de la route pour afficher les élèves
@app.route('/eleves')
def eleves():
    # Récupération du paramètre 'classe' dans l'URL (si présent)
    classe = request.args.get('classe')

    # Si une classe est spécifiée, filtrer les élèves par classe
    if classe:
        liste_eleves_classe = [eleve for eleve in liste_eleves if eleve['classe'] == classe]
        # Rendre le modèle HTML 'eleves.html' avec la liste filtrée
        return render_template('eleves.html', liste_eleves=liste_eleves_classe)

    # Si aucune classe n'est spécifiée, afficher tous les élèves
    return render_template('eleves.html', liste_eleves=liste_eleves)

# Lancement de l'application en mode debug
if __name__ == '__main__':
    app.run(debug=True)