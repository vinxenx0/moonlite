from app import db
from datetime import datetime, timedelta


class MarketingMetrics(db.Model):
    __tablename__ = 'marketing_metrics'
    id = db.Column(db.Integer, primary_key=True)
    churn_rate = db.Column(db.Float, nullable=False)
    clv = db.Column(db.Float, nullable=False)
    cac = db.Column(db.Float, nullable=False)
    mrr = db.Column(db.Float, nullable=False)
    arr = db.Column(db.Float, nullable=False)
    nrr = db.Column(db.Float, nullable=False)
    expansion_revenue_rate = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<MarketingMetrics {self.id}>'

    def to_dict(self):
        """Convierte el objeto en un diccionario serializable"""
        return {
            "id": self.id,
            "churn_rate": self.churn_rate,
            "clv": self.clv,
            "cac": self.cac,
            "mrr": self.mrr,
            "arr": self.arr,
            "nrr": self.nrr,
            "expansion_revenue_rate": self.expansion_revenue_rate,
            "created_at": self.created_at.isoformat(),  # Convertir datetime a string
            "updated_at": self.updated_at.isoformat()   # Convertir datetime a string
        }

