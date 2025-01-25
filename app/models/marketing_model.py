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
        return f'<MarketingMetrics {self.created_at} - {self.id}>'

    @staticmethod
    def save_metrics(metrics):
        """Guardar métricas calculadas en la base de datos."""
        new_metrics = MarketingMetrics(
            churn_rate=metrics['churn_rate'],
            clv=metrics['clv'],
            cac=metrics['cac'],
            mrr=metrics['mrr'],
            arr=metrics['arr'],
            nrr=metrics['nrr'],
            expansion_revenue_rate=metrics['expansion_revenue_rate'],
        )
        db.session.add(new_metrics)
        db.session.commit()
