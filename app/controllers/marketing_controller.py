from flask import render_template, redirect, url_for
from flask_login import login_required
from app.models.user_model import Users, Transaction
from app.models.marketing_model import MarketingMetrics
from app import db
from datetime import datetime, timedelta
from sqlalchemy import func

@app.route('/admin/marketing')
@login_required
def marketing_dashboard():
    """Carga las métricas de marketing desde la base de datos o las calcula si no existen."""
    breadcrumbs = [{'url': '/admin', 'text': 'Admin'}, {'url': '/admin/marketing', 'text': 'Marketing Dashboard'}]

    # Consultar métricas de marketing existentes
    marketing_data = MarketingMetrics.query.first()
    if not marketing_data:
        # Si no existen datos, calcular y almacenar métricas iniciales
        stats = calculate_marketing_metrics()
        marketing_data = MarketingMetrics(
            churn_rate=stats['churn_rate'],
            clv=stats['clv'],
            cac=stats['cac'],
            mrr=stats['mrr'],
            arr=stats['arr'],
            nrr=stats['nrr'],
            expansion_revenue_rate=stats['expansion_revenue_rate']
        )
        db.session.add(marketing_data)
        db.session.commit()
    else:
        # Cargar métricas desde la base de datos
        stats = {
            'churn_rate': marketing_data.churn_rate,
            'clv': marketing_data.clv,
            'cac': marketing_data.cac,
            'mrr': marketing_data.mrr,
            'arr': marketing_data.arr,
            'nrr': marketing_data.nrr,
            'expansion_revenue_rate': marketing_data.expansion_revenue_rate
        }

    return render_template('admin/marketing_dashboard.html', breadcrumbs=breadcrumbs, stats=stats)

def calculate_marketing_metrics():
    """Calcula métricas clave de marketing y las devuelve como un diccionario."""
    stats = {}
    now = datetime.utcnow()
    one_month_ago = now - timedelta(days=30)

    # Número de clientes
    total_customers = Users.query.filter(Users.active == True).count()

    # Número de cancelaciones
    churned_customers = Users.query.filter(Users.active == False).count()

    # Churn Rate
    stats['churn_rate'] = (churned_customers / total_customers * 100) if total_customers > 0 else 0

    # Customer Lifetime Value (CLV)
    avg_purchase_value = db.session.query(func.avg(Transaction.amount)).scalar() or 0
    avg_purchase_frequency = db.session.query(func.count(Transaction.id) / total_customers).scalar() or 0
    avg_relationship_duration = 12  # Suposición de relación promedio en meses
    stats['clv'] = avg_purchase_value * avg_purchase_frequency * avg_relationship_duration

    # CAC
    total_marketing_costs = 5000  # Valor de ejemplo
    new_customers = Users.query.filter(Users.registered_on >= one_month_ago).count()
    stats['cac'] = (total_marketing_costs / new_customers) if new_customers > 0 else 0

    # MRR y ARR
    mrr = db.session.query(func.sum(Transaction.amount)).filter(Transaction.timestamp >= one_month_ago).scalar() or 0
    stats['mrr'] = mrr
    stats['arr'] = mrr * 12

    # NRR
    upsell_revenue = db.session.query(func.sum(Transaction.amount)).filter(Transaction.description.like('%Upgrade%')).scalar() or 0
    stats['nrr'] = ((mrr + upsell_revenue - churned_customers) / mrr * 100) if mrr > 0 else 0

    # Expansion Revenue Rate
    stats['expansion_revenue_rate'] = (upsell_revenue / mrr * 100) if mrr > 0 else 0

    return stats
