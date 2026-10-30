"""ツールのテスト（LLMもAPIキーも使わない）。"""

import json

from app import tools


def test_glossary_ids_are_unique_and_related_links_exist():
    terms = tools.load_glossary()
    ids = [t["id"] for t in terms]
    assert len(ids) == len(set(ids))
    for t in terms:
        for r in t["related"]:
            assert r in ids, f"{t['id']} の related に存在しない id: {r}"


def test_search_finds_term_by_name_and_alias():
    for query in ["LoRA", "lora", "Low-Rank Adaptation"]:
        hits = json.loads(tools.search_glossary(query))
        assert hits[0]["term"] == "LoRA", query


def test_search_finds_course_specific_term():
    hits = json.loads(tools.search_glossary("lecNN-start"))
    assert hits[0]["term"] == "lecNN-start タグ"


def test_search_limits_number_of_results():
    hits = json.loads(tools.search_glossary("エージェント"))
    assert 1 <= len(hits) <= tools.MAX_RESULTS


def test_search_reports_not_found():
    assert "見つかりませんでした" in tools.search_glossary("存在しない用語xyz")


def test_lecture_summary():
    assert "エージェント" in tools.get_lecture_summary(3)
    assert "まだありません" in tools.get_lecture_summary(99)


def test_default_question_of_lecture1_is_answerable_from_glossary():
    """第1回の既定の質問（app.ask）は、第3回のエージェントが用語集で正しく答えられること。"""
    from app.ask import DEFAULT_QUESTION

    assert "3レベル" in DEFAULT_QUESTION
    hits = json.loads(tools.search_glossary("3レベル"))
    assert hits[0]["term"] == "宿題の3レベル"


def test_ask_prints_input_and_output_token_usage(monkeypatch, capsys):
    from types import SimpleNamespace

    from app import ask

    response = SimpleNamespace(
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=5),
        text="回答",
    )
    fake_client = SimpleNamespace(
        models=SimpleNamespace(generate_content=lambda **kwargs: response)
    )
    monkeypatch.setattr(ask.genai, "Client", lambda api_key: fake_client)

    assert ask.ask("質問") == "回答"
    assert "[usage] input_tokens=12 output_tokens=5" in capsys.readouterr().out


def test_conversation_summarizes_old_exchanges_and_keeps_recent_history():
    from types import SimpleNamespace

    from app.ask import Conversation

    requests = []

    def generate_content(*, model, contents):
        requests.append(contents)
        if isinstance(contents, str):
            return SimpleNamespace(text="会話の要約", usage_metadata=None)
        return SimpleNamespace(text=f"回答{len(requests)}", usage_metadata=None)

    conversation = Conversation(SimpleNamespace(models=SimpleNamespace(generate_content=generate_content)))
    for index in range(1, 6):
        conversation.ask(f"質問{index}")

    assert conversation.summary == "会話の要約"
    assert len(conversation.history) == 8

    conversation.ask("質問6")
    next_request = requests[-2]
    assert "質問1" not in [part.text for message in next_request for part in message.parts]
    assert "これまでの会話の要約です。" in next_request[0].parts[0].text
    assert "質問2" in [part.text for message in next_request for part in message.parts]
