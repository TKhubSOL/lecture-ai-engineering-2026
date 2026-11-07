# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：第1回ではハルシネーションが発生し、正確な回答が返ってこなかった。一方で今回はglossary.jsonで記載された内容が回答として返ってきており、検索して回答してくれることがわかった。
- `--trace` で見えたツール呼び出し（ツール名と引数）：
    [tool call]   search_glossary({'query': 'LoRA'})
    [tool call]   search_glossary({'query': 'QLoRA'})
- 1つの質問での LLM 呼び出し回数（`requests`）：2
- 追加したツールと、docstring に書いた説明：
    [make_quiz]
    指定した回の用語から1つを選び、確認問題と答えを返す。
    「第2回の確認問題を出して」のように、復習用の問題を求められたときに使う。
    引数: {"lecture": {"type": "integer"}}

## 宿題

- 取り組んだレベル：基礎 / 実装 
- やったこと：
    # 基礎
    1. app/agent.py の INSTRUCTIONS から「必ず search_glossary で用語集を確認する」という指示を削除し、「LoRA と QLoRA の違い」を同じ条件で --trace 付きで質問した。
    2. app/tool.py の search_glossary 関数の docstirng から「1つだけ入れる」という指示を「まとめて入れる」という指示に変更して、「LoRA と QLoRA の違い」を同じ条件で --trace 付きで質問した。

    # 実装
    save_learning_log を追加し、学習記録を日付別のMarkdownファイルとして learning_log/ に追記するようにした。ツールには requires_approval=True を設定し、CLIで保存内容を表示して承認を確認した後、DeferredToolResults と会話履歴を渡して実行を再開するようにした。


- 結果：
    # 基礎
    1. 指示を削除した後も、search_glossary が LoRA と QLoRA についてそれぞれ呼び出された。回答の主な内容と関係する回は同じで、表現や強調の仕方に小さな違いがあった。

    # デフォルトの実行結果
    [model] gemini-3.5-flash-lite
    講座の用語集によると、LoRAとQLoRAの違いは以下の通りです。

    * **LoRA**
    事前学習済みの重みは固定したまま、重みの更新分を2つの小さな低ランク行列の積で表し、その小さな行列だけを学習するPEFT手法です。学習するパラメータが少なく、アダプタと呼ばれる小さなファイルで保存できます。

    * **QLoRA**
    ベースモデルの重みを4ビットなどに**量子化**してメモリを大幅に節約したうえで、LoRAによる学習を行う手法です。これにより、より大きなモデルを比較的小さなGPUでも扱えるようになります。

    関係する回：第2回

    --- trace ---
    [tool call]   search_glossary({'query': 'LoRA'})
    [tool call]   search_glossary({'query': 'QLoRA'})
    [tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
    [tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
    [usage] RunUsage(cost=Decimal('0.0008194'), details={'text_prompt_tokens': 1198}, input_text_tokens=1198, input_tokens=1198, output_tokens=184, requests=2, tool_calls=2)

    # INSTRUCTIONS の指示文一部削除の実行結果
    [model] gemini-3.5-flash-lite
    LoRAとQLoRAの主な違いは、**ベースモデルの重みの保持方法とメモリ効率**にあります。

    * **LoRA（Low-Rank Adaptation）**
    * 事前学習済みの重みはそのまま（通常は16ビットなどの精度）固定し、重みの更新分（低ランク行列）だけを新たに学習する手法です。学習パラメータや保存ファイルを大幅に削減できます。
    * **QLoRA（Quantized LoRA）**
    * LoRAの仕組みに加え、ベースモデルの重みを**4ビットなどに量子化**してメモリをさらに大幅に節約した状態で学習する手法です。これにより、より大きなモデルを小さなGPUでも効率よく扱えるようになります。

    （第2回）

    --- trace ---
    [tool call]   search_glossary({'query': 'LoRA'})
    [tool call]   search_glossary({'query': 'QLoRA'})
    [tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
    [tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
    [usage] RunUsage(cost=Decimal('0.0008825'), details={'text_prompt_tokens': 1300}, input_text_tokens=1300, input_tokens=1300, output_tokens=197, requests=2, tool_calls=2)

    2. tool_callsがこれまで2だったのが、1となった。
    # search_glossary 関数の docstirng分変更時の実行結果
    [model] gemini-3.5-flash-lite
    **LoRA（Low-Rank Adaptation）**と**QLoRA（Quantized LoRA）**は、どちらも大規模言語モデル（LLM）などを効率的にファインチューニングするためのPEFT（Parameter-Efficient Fine-Tuning）手法ですが、次のような違いがあります。

    * **LoRA**:
    事前学習済みの重みを固定したまま、追加の低ランクな小さな行列（アダプタ）のみを学習することで、学習パラメータ数やメモリ消費量を大幅に削減します。本講座の演習でも扱います。
    * **QLoRA**:
    ベースモデルの重みを **4ビットなどに量子化** してメモリ消費量をさらに極限まで削減した上で、LoRAを適用して学習する手法です。LoRAよりもさらに大きなモデルを、より小規模なGPU環境で扱えるようにします。

    関係する回：第2回

    --- trace ---
    [tool call]   search_glossary({'query': 'LoRA QLoRA'})
    [tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
    [usage] RunUsage(cost=Decimal('0.0008336'), details={'text_prompt_tokens': 1037}, input_text_tokens=1037, input_tokens=1037, output_tokens=209, requests=2, tool_calls=1)


    # 実装
    「第2回で学んだLoRAの要点を学習記録に保存して」と実行すると、用語集を検索した後、保存する内容が表示されて承認を求められた。y を入力すると保存が完了し、learning_log/2026-11-07.md に記録された。

    # 実行結果
    uv run python -m app.agent --trace "第2回で学んだLoRAの要点を学習記録に保存して"
    [model] gemini-3.5-flash-lite
    save_learning_log を実行しますか？
    引数: {"content": "第2回：LoRAについて学習した。\n・LoRAとは：事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。\n・特徴：学習するパラメータが少なく、アダプタと呼ばれる小さなファイルで保存できる。\n・関連用語：ランク（LoRAのr）、QLoRA"}
    保存を承認しますか？ [y/N]: y
    第2回で学んだLoRAの要点を学習記録に保存しました。

    （関係する回：第2回）

    --- trace ---
    [tool call]   search_glossary({'query': 'LoRA'})
    [tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
    [tool call]   save_learning_log({'content': '第2回：LoRAについて学習した。\n・LoRAとは：事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。\n・特徴：学習するパラメータが少なく、アダプタと呼ばれる小さなファイルで保存できる。\n・関連用語：ランク（LoRAのr）、QLoRA'})
    [tool return] save_learning_log -> 学習記録を learning_log/2026-11-07.md に保存しました。…
    [usage] RunUsage(cost=Decimal('0.0003438'), details={'text_prompt_tokens': 921}, input_text_tokens=921, input_tokens=921, output_tokens=27, requests=1, tool_calls=1)



- 気づき・疑問：
    # 基礎
    INSTRUCTIONS の指示を1つ削除しても検索の呼び出しはなくならなかった。search_glossary の docstring にも用語を答える前に検索するよう記載があり、モデルがそちらを手がかりにした可能性がある。回答の言い回しには揺れもあるため、指示の効果を確かめるには、ツールの説明も含めて条件をそろえ、複数回比較する必要がある。

    # 実装
    承認待ちにすることで、ツールが実行される前に保存内容を確認できた。保存する記録の内容はモデルが作るため、承認前に表示された内容を読んでから判断することが大切だと分かった。

