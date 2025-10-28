from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Pensionne(db.Model):
    __tablename__ = 'pensionnes'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    cin = db.Column(db.String(20), nullable=False)
    lieu_naissance = db.Column(db.String(50), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    type_pension = db.Column(db.String(50), nullable=False)
    montant_pension = db.Column(db.Float, nullable=False, default=0.0)
    montant_opposition = db.Column(db.Float, nullable=False, default=0.0)
    montant_net = db.Column(db.Float, nullable=False, default=0.0)
    statut = db.Column(db.String(20), nullable=False, default='Non envoyé')
    periode = db.Column(db.String(7), nullable=False)  # Format YYYY-MM
    mois_paiement = db.Column(db.String(7), nullable=False)  # Format YYYY-MM
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Date de création

    def __repr__(self):
        return f"<Pensionne {self.nom} {self.prenom} ({self.periode})>"
