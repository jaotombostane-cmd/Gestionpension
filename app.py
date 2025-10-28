from flask import Flask, render_template, request, redirect, url_for, session
from models import db, Pensionne
from datetime import datetime
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# ---------- Configuration ----------
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL",
    f"sqlite:///{os.path.join(basedir, 'pensions.db')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get("SECRET_KEY", "change_this_secret_key")

db.init_app(app)

# ---------- Création DB si nécessaire (développement seulement) ----------
if not os.path.exists(os.path.join(basedir, 'pensions.db')):
    with app.app_context():
        db.create_all()
        print("Database created (SQLite local).")

# ---------- Routes ----------
@app.route('/', methods=['GET', 'POST'])
def choose_period():
    if request.method == 'POST':
        month = request.form['month']
        year = request.form['year']
        session['periode'] = f"{year}-{month.zfill(2)}"
        return redirect(url_for('index'))
    return render_template('choose_period.html')


@app.route('/index')
def index():
    periode = session.get('periode')
    if not periode:
        return redirect(url_for('choose_period'))
    pensionnes = Pensionne.query.filter_by(periode=periode).all()
    return render_template('index.html', pensionnes=pensionnes, periode=periode)


@app.route('/add', methods=['GET', 'POST'])
def add_pensionne():
    types_pension = ["Secours au décès", "Retraite", "Autre"]
    if request.method == 'POST':
        nom = request.form.get('nom', '').strip()
        prenom = request.form.get('prenom', '').strip()
        cin = request.form.get('cin', '').strip()
        lieu_naissance = request.form.get('lieu_naissance', '').strip()
        date_naissance_str = request.form.get('date_naissance', '')
        type_pension = request.form.get('type_pension', 'Autre')

        try:
            montant_pension = float(request.form.get('montant_pension', 0))
        except ValueError:
            montant_pension = 0

        try:
            montant_opposition = float(request.form.get('montant_opposition', 0))
        except ValueError:
            montant_opposition = 0

        montant_net = montant_pension - montant_opposition
        periode = session.get('periode', datetime.now().strftime("%Y-%m"))

        date_naissance = datetime.strptime(date_naissance_str, '%Y-%m-%d') if date_naissance_str else datetime.now()

        pensionne = Pensionne(
            nom=nom or "Inconnu",
            prenom=prenom or "Inconnu",
            cin=cin or "000000",
            lieu_naissance=lieu_naissance or "Inconnu",
            date_naissance=date_naissance,
            type_pension=type_pension,
            montant_pension=montant_pension,
            montant_opposition=montant_opposition,
            montant_net=montant_net,
            statut='Non envoyé',
            periode=periode,
            mois_paiement=periode
        )

        db.session.add(pensionne)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_pensionne.html', types_pension=types_pension)


@app.route('/ticket/<int:id>')
def ticket(id):
    pensionne = Pensionne.query.get_or_404(id)
    return render_template('ticket.html', pensionne=pensionne)


# ---------- Lancement ----------
# Note: Render utilisera gunicorn, donc app.run() n'est pas nécessaire en production
if __name__ == '__main__':
    app.run(debug=True)
