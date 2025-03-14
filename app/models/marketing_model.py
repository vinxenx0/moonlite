from app import db
from datetime import datetime

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

    @classmethod
    def save_metrics(cls, stats):
        """Guarda las métricas calculadas en la base de datos."""
        metric = cls(
            churn_rate=stats['churn_rate'],
            clv=stats['clv'],
            cac=stats['cac'],
            mrr=stats['mrr'],
            arr=stats['arr'],
            nrr=stats['nrr'],
            expansion_revenue_rate=stats['expansion_revenue_rate']
        )
        db.session.add(metric)
        db.session.commit()

    def to_dict(self):
        """Convierte una instancia del modelo en un diccionario."""
        return {
            'id': self.id,
            'churn_rate': self.churn_rate,
            'clv': self.clv,
            'cac': self.cac,
            'mrr': self.mrr,
            'arr': self.arr,
            'nrr': self.nrr,
            'expansion_revenue_rate': self.expansion_revenue_rate,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

    def __repr__(self):
        return f'<MarketingMetrics {self.id} - {self.created_at}>'
