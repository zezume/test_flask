from flask import Flask, render_template
import datetime

app = Flask(__name__)

@app.route('/')
def heure():
    date_heure = datetime.datetime.now()
    heure = date_heure.hour
    minute = date_heure.minute
    seconde = date_heure.second

    return render_template('heure.html',heure=heure, minute=minute, seconde=seconde)
if __name__ == '__main__':
    app.run(debug=True)