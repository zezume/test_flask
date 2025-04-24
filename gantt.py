from random import randint
from flask import Flask, render_template, request, redirect, url_for, session
import secrets
import plotly.express as px
import pandas as pd
from io import BytesIO
from PyPDF2 import PdfReader

# Initialisation de l'application Flask
app = Flask(__name__)
app.secret_key = secrets.token_hex()  # Clé secrète pour sécuriser les sessions

data = [
    {"Intervenant": "Alice", "Début": "2023-10-01", "Fin": "2023-10-05", "Projet": "Projet A"},
    {"Intervenant": "Alice", "Début": "2023-10-05", "Fin": "2023-10-08", "Projet": "Projet C"},
    {"Intervenant": "Bob", "Début": "2023-10-03", "Fin": "2023-10-07", "Projet": "Projet B"},
    {"Intervenant": "Charlie", "Début": "2023-10-02", "Fin": "2023-10-06", "Projet": "Projet A"},
    {"Intervenant": "David", "Début": "2023-10-04", "Fin": "2023-10-08", "Projet": "Projet C"},
]
@app.route('/gantt')
def gantt():
    # Génère un graphique Gantt, couleur depand du projet, axe Y sont les intervenants
    df = pd.DataFrame(data)
    fig = px.timeline(df, x_start='Début', x_end='Fin', y='Intervenant', color='Projet')
    fig.update_layout(title='Graphique Gantt', xaxis_title='Date')
    fig.update_xaxes(tickformat="%Y-%m-%d")
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(title_font_weight='bold')

    # Convertit le graphique en HTML
    graph_html = fig.to_html(full_html=False)

    # Affiche le graphique dans le template
    return render_template("gantt.html", graph_html=graph_html)

# Lancement de l'application en mode debug
if __name__ == '__main__':
    app.run(debug=True)
