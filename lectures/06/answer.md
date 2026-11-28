# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：glossary_search_glossary
- STEP 2 の [tool call]：glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]：fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]：aws_aws___search_documentation({'search_phrase': 'Amazon S3 バージョニング 概要', 'topics': ['general']}), aws_aws___search_documentation({'topics': ['general'], 'search_phrase': 'Versioning overview Amazon S3 bucket versions'})
- 気づき・疑問：MCPサーバー経由でもツール名や説明文、引数など通常のツールと同じ形で運用されていた。最後の補足にて講師の方より触れられていたが、これまで以上にMCPとは内部で何が行われているのかわからなくなっており、信頼できるものしか運用しないようにしないといけないと感じた。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎
- やったこと：これまで演習で変更していたapp/mcp_servers.json を変更せずに、app/mcp_server.py にget_lecture_summaryを追加した。
- 結果：下記のように、json側を変更せずにツールが増えたことを確認した。
$ uv run python -m app.mcp_agent --trace "第2回では何を学びますか？"
[server] glossary: コマンドで起動（uv run python -m app.mcp_server）
[server] fetch: コマンドで起動（uvx mcp-server-fetch==2026.11.11 --no-readability-js）
[server] aws: URL に接続（https://knowledge-mcp.global.api.aws）
[model] gemini-3.5-flash-lite
[tools] MCP サーバー（app/mcp_servers.json）
第2回では、「ファインチューニングとLoRA」について学びます。

### 主な内容
- **事前学習とファインチューニング**：事前学習とファインチューニングの違いや、それぞれが向く場面・向かない場面についての理解。
- **SFT（教師あり微調整）**：入力と望ましい出力のペアを用いて、モデルの出力形式や口調などを最適化する方法。
- **PEFTとLoRA**：全パラメータを更新するのではなく、小さな低ランク行列を追加して効率的に学習・調整を行うLoRAの考え方。
- **演習（Google Colab）**：小さなモデル（Qwen2.5-0.5B / Qwen3.5-0.8Bなど）を架空のFAQデータでLoRA学習させ、学習の前後で出力形式（JSONなど）がどのように変わるかを体験します。

（関連する回：第2回）

--- trace ---
[tool call]   glossary_get_lecture_summary({'lecture': 2})
[tool return] glossary_get_lecture_summary -> # 第2回 ファインチューニングとLoRA

## この回のねらい

- 事前学習とファインチューニングの違い、ファインチューニングが向く場面と向かない場面を理解する
- LoRAの考え方を理解し、Google Colab上で小さなモデルを…
[usage] 入力 5,942 tokens / 出力 222 tokens / モデル応答 2 回
- 気づき・疑問：質問内容によって `glossary_get_lecture_summary` を選び、サーバーから取得した結果を基に回答している点が興味深かった。ツールの説明文や引数の設計が、モデルが使用するツールの選択にどのように影響するのか確認してみたい。
