from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def bonjour():
    return render_template('bonjour.html')

liste_eleves = [
    {'nom': 'Dupont', 'prenom': 'Jean', 'classe': '2A'},
    {'nom': 'Dupont', 'prenom': 'Jeanne', 'classe': 'TG2'},
    {'nom': 'Marchand', 'prenom': 'Marie', 'classe': '2A'},
    {'nom': 'Martin', 'prenom': 'Adeline', 'classe': '1G1'},
    {'nom': 'Dupont', 'prenom': 'Lucas', 'classe': '2A'}
]
@app.route('/eleves')
def eleves():
    classe = request.args.get('classe')

    if classe:
        liste_eleves_classe = [eleve for eleve in liste_eleves if eleve['classe'] == classe]
        return render_template('eleves.html', liste_eleves=liste_eleves_classe)

    return render_template('eleves.html', liste_eleves=liste_eleves)

if __name__ == '__main__':
    app.run(debug=True)