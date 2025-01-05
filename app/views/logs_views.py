from flask import render_template
from flask_login import login_required
from app.models.usage_model import Activity
from app import app, db


@app.route('/admin/activity')
@login_required
def activity():
    breadcrumbs = [{
        'url': '/admin',
        'text': 'Admin'
    }, {
        'url': '/admin/activity',
        'text': 'Actividad'
    }]
    # Consulta todos los registros de UserUsage
    records = Activity.query.all()
    # Renderiza la plantilla 'user_usage.html' y pasa los registros como contexto
    return render_template('activity.html',
                           records=records,
                           breadcrumbs=breadcrumbs)
