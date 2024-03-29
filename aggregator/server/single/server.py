from flask import Blueprint, render_template
from server.single.database import database
from aggregator.register import register
from server.single.database import PluginModel, UserModel
from server.single.admin import admin_panel
from utils.log import get_logger


log = get_logger('server')
single_user_server = Blueprint('single_user', __name__)
plugins = []
for plugin in PluginModel.select():
    plugins.append(register[plugin.plugin])


@single_user_server.route('/', methods=['GET'])
def index():
    plugins = register.list_plugins()
    models = list(PluginModel.select())
    views = [[register[m.plugin](m.id, m.size, m.params, m.data) for m in models]]
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
        size = register[plugin].__sizes__[0]
        view = PluginModel(plugin=plugin, user=user, size=size)
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
    log.debug(f'Save value: {value}')
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


@single_user_server.route('/save-size/<int:plugin_id>/<int:size>', methods=['POST'])
def save_size(plugin_id, size):
    plugin = PluginModel.get_or_none(id=plugin_id)
    if plugin and plugin.plugin in register:
        sizes = register[plugin.plugin].__sizes__
        if size in sizes:
            plugin.size = size
            plugin.save()
            return '', 200
    return '', 400
