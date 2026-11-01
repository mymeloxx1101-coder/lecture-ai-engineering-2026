from types import SimpleNamespace

from app import ask as ask_module


class FakeModels:
    def generate_content(self, *, model, contents):
        return SimpleNamespace(
            text="回答",
            usage_metadata=SimpleNamespace(
                prompt_token_count=12,
                candidates_token_count=7,
            ),
        )


class FakeClient:
    def __init__(self, *, api_key):
        self.models = FakeModels()


def test_ask_prints_input_and_output_tokens(monkeypatch, capsys):
    monkeypatch.setattr(ask_module.genai, "Client", FakeClient)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")

    assert ask_module.ask("質問") == "回答"
    assert capsys.readouterr().out == "[tokens] 入力=12 出力=7\n"
