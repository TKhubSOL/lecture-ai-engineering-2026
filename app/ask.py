"""第1回: 素のLLMに質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする
    uv run python -m app.ask --chat     # 会話モード

ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import errors
from google.genai import types

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"
SUMMARY_AFTER_EXCHANGES = 5
RECENT_EXCHANGES = 4


def _content(role: str, text: str) -> types.Content:
    return types.Content(role=role, parts=[types.Part.from_text(text=text)])


def _print_usage(response, purpose: str | None = None) -> None:
    usage = response.usage_metadata
    if usage is not None:
        label = f"[usage:{purpose}]" if purpose else "[usage]"
        print(
            f"{label} input_tokens={usage.prompt_token_count} "
            f"output_tokens={usage.candidates_token_count}"
        )


def ask(question: str) -> str:
    client = genai.Client(api_key=get_api_key())
    response = client.models.generate_content(model=MODEL, contents=question)
    _print_usage(response)
    return response.text


class Conversation:
    def __init__(self, client):
        self.client = client
        self.history: list[types.Content] = []
        self.summary = ""

    def ask(self, question: str) -> str:
        contents = []
        if self.summary:
            contents.extend(
                [
                    _content("user", f"これまでの会話の要約です。文脈として使ってください。\n{self.summary}"),
                    _content("model", "要約を踏まえて会話を続けます。"),
                ]
            )
        contents.extend(self.history)
        user_message = _content("user", question)
        response = self.client.models.generate_content(
            model=MODEL, contents=[*contents, user_message]
        )
        answer = response.text or ""
        self.history.extend([user_message, _content("model", answer)])
        _print_usage(response)

        if len(self.history) >= SUMMARY_AFTER_EXCHANGES * 2:
            self._summarize_history()

        return answer

    def _summarize_history(self) -> None:
        split_at = len(self.history) - RECENT_EXCHANGES * 2
        old_messages = self.history[:split_at]
        old_conversation = "\n".join(
            f"{'ユーザー' if message.role == 'user' else 'アシスタント'}: "
            f"{' '.join(part.text for part in message.parts if part.text)}"
            for message in old_messages
        )
        previous_summary = f"以前の要約:\n{self.summary}\n\n" if self.summary else ""
        prompt = (
            "以下の会話を、次の質問に必要な事実・ユーザーの目的・未解決事項を残して、"
            "簡潔な要約にしてください。\n\n"
            f"{previous_summary}要約に追加する会話:\n{old_conversation}"
        )
        response = self.client.models.generate_content(model=MODEL, contents=prompt)
        _print_usage(response, "summary")
        if response.text:
            self.summary = response.text
            self.history = self.history[split_at:]


def run_chat(initial_question: str | None = None) -> None:
    conversation = Conversation(genai.Client(api_key=get_api_key()))
    question = initial_question
    while True:
        if question is None:
            try:
                question = input("[質問] ")
            except EOFError:
                print()
                return

        question = question.strip()
        if question.lower() in {"/exit", "/quit"}:
            return
        if not question:
            question = None
            continue

        print(f"[質問] {question}\n")
        print(conversation.ask(question))
        print()
        question = None


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?")
    parser.add_argument("--chat", action="store_true", help="会話履歴を保って続けて質問する")
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    if args.chat:
        try:
            run_chat(args.question)
        except errors.APIError as e:
            print(api_error_message(e.code, e.message))
            raise SystemExit(1)
        return

    question = args.question or DEFAULT_QUESTION
    print(f"[質問] {question}\n")
    try:
        print(ask(question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
