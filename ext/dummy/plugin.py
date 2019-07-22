from aggregator.plugin import Plugin, StringParam, BoolParam, NumberParam


class DummyPlugin(Plugin):

    __pluginname__ = 'dummy'
    __location__ = __file__
    __paramschema__ = (
        StringParam('string', 'String parameter.'),
        BoolParam('bool', 'Bool Parameter.'),
        NumberParam('int', 'Integer Parameter', step=1, min=0, max=10),
        NumberParam('float', 'Float Parameter', step=0.01)
    )
