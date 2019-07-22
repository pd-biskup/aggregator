from flask import Blueprint, render_template, request
from server.single.database import PluginModel


admin_panel = Blueprint('admin', __name__, url_prefix='/admin')


@admin_panel.route('/', methods=['GET', 'POST', 'UPDATE', 'DELETE'])
def admin():
    if request.method == 'GET':
        plugins = list(PluginModel.select())
        return render_template("admin.html", plugins=plugins)
