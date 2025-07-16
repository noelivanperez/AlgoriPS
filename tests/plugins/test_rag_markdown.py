from plugins.rag_markdown import Plugin


def test_name_version():
    plugin = Plugin()
    assert plugin.name() == "rag-markdown"
    assert plugin.version() == "0.1"
