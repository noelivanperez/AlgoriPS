from plugins.ts_analyzer import Plugin


def test_name_version():
    plugin = Plugin()
    assert plugin.name() == "ts-analyzer"
    assert plugin.version() == "0.1"
