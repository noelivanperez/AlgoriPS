import importlib


def test_main_invokes_cli(monkeypatch):
    called = {}

    def fake_cli():
        called['run'] = True

    monkeypatch.setattr('algorips.cli.main.cli', fake_cli)
    import algorips.__main__ as main
    main.cli()
    assert called.get('run') is True
