from plugins.eslint_plugin import Plugin


def test_name_version():
    plugin = Plugin()
    assert plugin.name() == "eslint-plugin"
    assert plugin.version() == "0.1"
