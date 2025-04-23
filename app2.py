from flask import Flask, render_template
import datetime

# Initialisation de l'application Flask
app = Flask(__name__)

# Définition de la route pour l'URL racine ('/')
@app.route('/')
def heure():
    # Récupération de la date et de l'heure actuelles
    date_heure = datetime.datetime.now()
    heure = date_heure.hour
    minute = date_heure.minute
    seconde = date_heure.second

    # Rendu du modèle 'heure.html' avec les variables heure, minute et seconde
    return render_template('heure.html', heure=heure, minute=minute, seconde=seconde)

# Lancement de l'application en mode debug
if __name__ == '__main__':
    app.run(debug=True)