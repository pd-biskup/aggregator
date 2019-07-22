from flask import Blueprint, render_template
from server.single.database import database
from aggregator.register import register
from server.single.database import PluginModel, UserModel
from server.single.admin import admin_panel


single_user_server = Blueprint('single_user', __name__)
plugins = []
for plugin in PluginModel.select():
    plugins.append(register[plugin.plugin])


@single_user_server.route('/', methods=['GET'])
def index():
    plugins = register.list_plugins()
    models = list(PluginModel.select())
    views = [[register[m.plugin](m.id, m.params, m.data) for m in models]]
    layout = {
        'rows': len(views),
        'cols': len(views[0]),
        'templates': views
    }
    return render_template('single.html', layout=layout, plugins=plugins)


@single_user_server.route('/add-plugin/<plugin>', methods=['POST'])
def add_plugin(plugin):
    if plugin in register:
        user, _ = UserModel.get_or_create(username='user')
        view = PluginModel(plugin=plugin, user=user, col=0, row=0, height=1, width=1)
        view.save()
        return '', 200
    return '', 400


@single_user_server.route('/remove-plugin/<int:id>', methods=['DELETE'])
def remove_plugin(id):
    plugin = PluginModel.get_or_none(id=id)
    if plugin:
        plugin.delete_instance()
        return '', 200
    return '', 400


@single_user_server.route('/save-param/<int:plugin_id>/<param_name>/<path:value>', methods=['POST'])
def save_param(plugin_id, param_name, value):
    plugin = PluginModel.get_or_none(id=plugin_id)
    if plugin and plugin.plugin in register:
        schema = register[plugin.plugin].__paramschema__
        for param in schema:
            if param_name == param.name:
                params = plugin.params
                if not params:
                    params = {}
                params[param_name] = param.validate(value)
                plugin.params = params
                plugin.save()
                return '', 200
    return '', 400
