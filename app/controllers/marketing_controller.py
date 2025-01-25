from datetime import datetime, timedelta  # Importar solo lo necesario
from flask import render_template, redirect, url_for
from flask_login import login_required
from app.models.user_model import Users, Transaction
from app.models.marketing_model import MarketingMetrics
from sqlalchemy import func
from app import app, db

@app.route('/admin/marketing', methods=['GET'])
@login_required
def marketing_dashboard():
    breadcrumbs = [{'url': '/admin', 'text': 'Admin'}, {'url': '/admin/marketing', 'text': 'Marketing Dashboard'}]

    # Cálculo de métricas
    stats = calculate_marketing_metrics()

    # Guardar métricas diarias si no existe un registro para hoy
    today = datetime.utcnow().date()
    latest_metrics = MarketingMetrics.query.order_by(MarketingMetrics.created_at.desc()).first()
    if not latest_metrics or latest_metrics.created_at.date() < today:
        MarketingMetrics.save_metrics(stats)

    # Obtener métricas históricas y convertirlas a diccionarios
    metrics_history = [
        metric.to_dict() for metric in MarketingMetrics.query.order_by(MarketingMetrics.created_at.asc()).all()
    ]

    # Datos granulares
    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).all()
    users = Users.query.order_by(Users.registered_on.desc()).all()
    now = datetime.utcnow()

    return render_template(
        'admin/marketing_dashboard.html',
        breadcrumbs=breadcrumbs,
        stats=stats,
        metrics_history=metrics_history,  # Pasar la lista de diccionarios
        transactions=transactions,
        users=users,
        timedelta = timedelta,
        now=now
    )



@app.route('/admin/old_marketing')
@login_required
def old_marketing_dashboard():
    breadcrumbs = [{'url': '/admin', 'text': 'Admin'}, {'url': '/admin/marketing', 'text': 'Marketing Dashboard'}]

    # Cálculo de métricas
    stats = calculate_marketing_metrics()

    # Datos granulares
    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).all()
    users = Users.query.order_by(Users.registered_on.desc()).all()
    now = datetime.utcnow()

    # Pasar timedelta al contexto
    return render_template(
        'admin/marketing_dashboard.html',
        breadcrumbs=breadcrumbs,
        stats=stats,
        transactions=transactions,
        users=users,
        now=now,
        timedelta=timedelta  # Pasar timedelta aquí
    )

def calculate_marketing_metrics():
    """Calcula las métricas clave para el panel de marketing."""
    stats = {}
    now = datetime.utcnow()
    one_month_ago = now - timedelta(days=30)

    # Total de clientes
    total_customers = Users.query.filter(Users.active == True).count()

    # Total de cancelaciones
    churned_customers = Users.query.filter(Users.active == False).count()

    # Churn Rate
    stats['churn_rate'] = (churned_customers / total_customers * 100) if total_customers > 0 else 0

    # Customer Lifetime Value (CLV)
    avg_purchase_value = db.session.query(func.avg(Transaction.amount)).scalar() or 0
    avg_purchase_frequency = db.session.query(func.count(Transaction.id) / total_customers).scalar() or 0

    # Convertir valores a float antes de realizar operaciones matemáticas
    avg_purchase_value = float(avg_purchase_value)
    avg_purchase_frequency = float(avg_purchase_frequency)

    stats['clv'] = avg_purchase_value * avg_purchase_frequency * 12  # 12 = relación promedio en meses

    # CAC
    total_marketing_costs = 5000  # Supuesto de marketing mensual
    new_customers = Users.query.filter(Users.registered_on >= one_month_ago).count()
    stats['cac'] = (total_marketing_costs / new_customers) if new_customers > 0 else 0

    # MRR y ARR
    mrr = db.session.query(func.sum(Transaction.amount)).filter(Transaction.timestamp >= one_month_ago).scalar() or 0
    stats['mrr'] = float(mrr)  # Convertir a float
    stats['arr'] = stats['mrr'] * 12

    # NRR
    upsell_revenue = db.session.query(func.sum(Transaction.amount)).filter(Transaction.description.like('%Upgrade%')).scalar() or 0
    upsell_revenue = float(upsell_revenue)  # Convertir a float
    stats['nrr'] = ((stats['mrr'] + upsell_revenue - churned_customers) / stats['mrr'] * 100) if stats['mrr'] > 0 else 0

    # Expansion Revenue Rate
    stats['expansion_revenue_rate'] = (upsell_revenue / stats['mrr'] * 100) if stats['mrr'] > 0 else 0

    return stats
  