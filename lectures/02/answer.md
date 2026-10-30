# 第2回 解答

## 演習

- 使ったモデル・設定（`result.json` の `config` から）：
"config": {
    "base_model": "Qwen/Qwen3.5-0.8B",
    "revision": "2fc06364715b967f1860aea9cf38778875588b17",
    "seed": 42,
    "num_train_epochs": 20,
    "warmup_steps": 6,
    "lr": 0.0002,
    "lora_r": 16,
    "lora_alpha": 32,
    "max_seq_len": 512,
    "max_new_tokens": 96,
    "gen": {
      "do_sample": false
    }
  }
- 自分で学習を実行したか（`executed_training_myself`）：はい （実行できた範囲：8. 発展まで実行）
- 学習前：`format_rate` =　0.09523809523809523 / `content_rate` =　0.0
- 学習後：`format_rate` =　1.0 / `content_rate` =　0.9047619047619048
- 退行した質問：成績開示の日時とオフィスアワーの事前予約に関して
- 学習後に残った失敗と、その型（根拠なしの質問に断定した / 根拠ありの質問に確認要求で逃げた / 形式の崩れ）：
    ①根拠なしの質問に断定した（成績開示の日時に対して、課題の締め切りの日時を回答）
    ②根拠なしの質問に断定した（オフィスアワーの事前予約に対して、事前予約に関する回答はせず）
- 知識を問う質問（セクション 6）の結果（学習前の分類 → 学習後の分類）と気づいたこと：根拠があるのに回答を控えることはなくなったが、根拠がないのに自信をもって答えることが多くなった
- 学習で変わったこと・変わらなかったこと：フォーマットのエラーはなくなった、一方で上記に挙げた通り知識の出し惜しみはしなくなったがハルシネーションが起こってしまった。

## 宿題

- 取り組んだレベル：基礎 / 実装 
- 変えた設定やデータ：
    ◆基礎：num_train_epochsを10に変更
    ◆実装：内容を下記の会社向けに変更して実装した
    FAQ = {
        "wifi": "社内Wi-FiのSSIDは 'Office-Guest'、パスワードは 'Welcome2026' です。",
        "shokudo": "社員食堂は12Fにあり、営業時間は11:30〜14:00です。",
        "printer": "複合機での印刷時は、ICカードをリーダーにタッチして認証してください。",
        "meeting_room": "会議室の予約は、グループウェアの『カレンダー』から15分単位で行えます。",
        "trash": "ゴミは、執務室の角にある分別ゴミ箱（燃える、ペットボトル、缶・ビン）へ捨ててください。",
    }
    FAQ_TEXT = "\n".join(f"- {v}" for v in FAQ.values())

    # 根拠あり: (FAQ キー, 質問テンプレート群, 正解の answer に含まれるべき語)
    GROUNDED = {
        "wifi": (["Wi-Fiのパスワードは何ですか", "ネットへの繋ぎ方を教えて", "無線LANのSSIDは？", "社内Wi-Fiに接続したい"], ["Office-Guest", "Welcome2026"]),
        "shokudo": (["食堂はどこにありますか", "お昼ご飯を食べられる場所は？", "社員食堂の営業時間は？", "ランチは何時からですか"], ["12F", "11:30"]),
        "printer": (["プリントアウトのやり方は？", "コピー機の使い方は？", "印刷はどうすればいいですか", "複合機の利用方法"], ["ICカード", "タッチ"]),
        "meeting_room": (["会議室を予約したいです", "ミーティングスペースの確保方法は？", "部屋の予約手順を教えて", "会議室はどうやって取りますか"], ["カレンダー", "15分"]),
        "trash": (["ゴミはどこに捨てればいいですか", "ゴミ箱の場所を教えて", "ゴミの分別ルールは？", "ペットボトルはどこへ？"], ["分別", "ゴミ箱"]),
    }
    # 根拠なし: FAQ に無いので needs_review=true が正解
    UNGROUNDED = [
        "今日の食堂の日替わりメニューは何ですか",
        "社外のゲストも食堂を利用できますか",
        "会議室にプロジェクターはありますか",
        "パソコンの貸出申請はどこで行いますか",
        "粗大ゴミを処分したいのですが",
        "Wi-Fiが繋がらない時の問い合わせ先は？",
        "ICカードを紛失してしまいました",
        "食堂の決済は交通系ICカードが使えますか",
    ]

    # test 専用の追加質問（train / valid には入れない）
    TEST_EXTRA_GROUNDED = {
        "wifi": ["社内ネットワークの接続情報を教えてください", "ゲスト用のWi-Fi情報はどこに載っていますか"],
        "shokudo": ["12階の食堂のオープン時間は何時から何時までですか", "社内でご飯を食べられる場所と時間を教えてください"],
        "printer": ["複合機で印刷を実行する際に必要な認証方法は何ですか", "紙を印刷するときにタッチするものは何ですか"],
        "meeting_room": ["グループウェアでの会議室の予約単位を教えてください", "会議室のスケジュール登録はどこで行いますか"],
        "trash": ["執務室内でのゴミの分別ルールと廃棄場所を教えてください", "ペットボトルや缶はどこに廃棄すればよいですか"],
    }
    TEST_EXTRA_UNGROUNDED = [
        "食堂のランチの平均予算はいくらですか",
        "複合機でスキャンしたデータはどこに送られますか",
        "会議室のキャンセル方法を教えてください",
        "ゴミ箱の回収頻度は週に何回ですか",
    ]
- 結果（比較表や数字）：
    # ◆基礎　学習後の結果：
    {
    "summary": {
        "label": "after",
        "n": 21,
        "format_rate": 1.0,
        "content_rate": 0.8571428571428571,
        "both_rate": 0.8571428571428571,
        "seconds": 49.7
    },
    "rows": [
        {
        "question": "提出の期限は？",
        "raw": "{\"answer\": \"課題の提出期限は 9 月 30 日 23:59（日本時間）です。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "提出期限の日付と時刻を教えてください",
        "raw": "{\"answer\": \"課題の提出期限は 9 月 30 日 23:59（日本時間）です。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "課題の締切は何月何日の何時ですか",
        "raw": "{\"answer\": \"課題の提出期限は 9 月 30 日 23:59（日本時間）です。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "提出場所は？",
        "raw": "{\"answer\": \"提出先は学習ポータルの「課題」欄です。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "課題の提出はどこで行いますか",
        "raw": "{\"answer\": \"提出先は学習ポータルの「課題」欄です。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "提出物を出す先を教えてください",
        "raw": "{\"answer\": \"提出先は学習ポータルの「課題」欄です。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "PDF 以外でも出せますか",
        "raw": "{\"answer\": \"この FAQ には記載がありません。提出先は学習ポータルの「課題」欄です。\", \"needs_review\": true}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": false
        },
        {
        "question": "提出するファイルの形式は何ですか",
        "raw": "{\"answer\": \"提出形式は PDF 1 ファイルで、ファイル名は 学籍番号_課題番号.pdf です。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "提出ファイルは何形式で、いくつ出しますか",
        "raw": "{\"answer\": \"提出形式は PDF 1 ファイルで、ファイル名は 学籍番号_課題番号.pdf です。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "相談できる時間帯は？",
        "raw": "{\"answer\": \"質問は毎週火曜 17:00〜18:00 のオフィスアワーで受け付けます。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "オフィスアワーの曜日と時間を教えてください",
        "raw": "{\"answer\": \"質問は毎週火曜 17:00〜18:00 のオフィスアワーで受け付けます。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "質問を受け付けてもらえるのは何曜日の何時からですか",
        "raw": "{\"answer\": \"質問は毎週火曜 17:00〜18:00 のオフィスアワーで受け付けます。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "締切後の扱いを教えてください",
        "raw": "{\"answer\": \"期限後の提出は、期限から 48 時間以内なら減点のうえ受け付けます。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "提出が締切に間に合わなかったらどうなりますか",
        "raw": "{\"answer\": \"期限後の提出は、期限から 48 時間以内なら減点のうえ受け付けます。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "期限後に提出した課題は受理されますか",
        "raw": "{\"answer\": \"期限後の提出は、期限から 48 時間以内なら減点のうえ受け付けます。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "成績はいつ出ますか",
        "raw": "{\"answer\": \"この FAQ には記載がありません。必ず確認が必要です。\", \"needs_review\": true}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": true
        },
        {
        "question": "講義の録画は公開されますか",
        "raw": "{\"answer\": \"この FAQ には記載がありません。必ず確認が必要です。\", \"needs_review\": true}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": true
        },
        {
        "question": "課題の文字数に制限はありますか",
        "raw": "{\"answer\": \"この FAQ には記載がありません。提出先は学習ポータルの「課題」欄です。\", \"needs_review\": true}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": true
        },
        {
        "question": "提出した課題へのフィードバックはもらえますか",
        "raw": "{\"answer\": \"この FAQ には記載がありません。運営に確認が必要です。\", \"needs_review\": true}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": true
        },
        {
        "question": "参考文献の書き方に指定はありますか",
        "raw": "{\"answer\": \"この FAQ には記載がありません。提出先は学習ポータルの「参考文献」欄です。\", \"needs_review\": true}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": true
        },
        {
        "question": "オフィスアワーは事前予約が必要ですか",
        "raw": "{\"answer\": \"この FAQ には記載がありません。必ず確認が必要です。\", \"needs_review\": true}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": true
        }
    ]
    }

    # ◆実装（学習前）：
    {
    "summary": {
        "label": "before",
        "n": 21,
        "format_rate": 0.047619047619047616,
        "content_rate": 0.0,
        "both_rate": 0.0,
        "seconds": 39.3
    },
    "rows": [
        {
        "question": "社内Wi-Fiに接続したい",
        "raw": "{\"answer\": \"社内Wi-FiのSSIDは 'Office-Guest'、パスワードは 'Welcome2026' です。\"}",
        "format_ok": false,
        "format_reason": "missing_key",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": false
        },
        {
        "question": "社内ネットワークの接続情報を教えてください",
        "raw": "{\"answer\": \"SSID: Office-Guest, Password: Welcome2026\"}",
        "format_ok": false,
        "format_reason": "missing_key",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": false
        },
        {
        "question": "ゲスト用のWi-Fi情報はどこに載っていますか",
        "raw": "{\"answer\": \"Office-Guest\"}",
        "format_ok": false,
        "format_reason": "missing_key",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": false
        },
        {
        "question": "ランチは何時からですか",
        "raw": "{\"answer\": \"確認が必要\"}",
        "format_ok": false,
        "format_reason": "missing_key",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": false
        },
        {
        "question": "12階の食堂のオープン時間は何時から何時までですか",
        "raw": "{\"answer\": \"11:30〜14:00\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": false
        },
        {
        "question": "社内でご飯を食べられる場所と時間を教えてください",
        "raw": "{\"answer\": \"社員食堂は12Fにあり、営業時間は11:30〜14:00です。\"}",
        "format_ok": false,
        "format_reason": "missing_key",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": false
        },
        {
        "question": "複合機の利用方法",
        "raw": "{\"answer\": \"複合機での印刷時は、ICカードをリーダーにタッチして認証してください。\"}",
        "format_ok": false,
        "format_reason": "missing_key",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": false
        },
        {
        "question": "複合機で印刷を実行する際に必要な認証方法は何ですか",
        "raw": "{\"answer\": \"複合機での印刷時は、ICカードをリーダーにタッチして認証してください。\"}",
        "format_ok": false,
        "format_reason": "missing_key",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": false
        },
        {
        "question": "紙を印刷するときにタッチするものは何ですか",
        "raw": "{\"answer\": \"複合機での印刷時は、ICカードをリーダーにタッチして認証してください\"}",
        "format_ok": false,
        "format_reason": "missing_key",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": false
        },
        {
        "question": "会議室はどうやって取りますか",
        "raw": "{\"answer\": \"グループウェアの『カレンダー』から15分単位で行えます\"}",
        "format_ok": false,
        "format_reason": "missing_key",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": false
        },
        {
        "question": "グループウェアでの会議室の予約単位を教えてください",
        "raw": "{\"answer\": \"15分\"}",
        "format_ok": false,
        "format_reason": "missing_key",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": false
        },
        {
        "question": "会議室のスケジュール登録はどこで行いますか",
        "raw": "{\"answer\": \"グループウェアの『カレンダー』から15分単位で行えます\"}",
        "format_ok": false,
        "format_reason": "missing_key",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": false
        },
        {
        "question": "ペットボトルはどこへ？",
        "raw": "{\"answer\": \"ペットボトルは、ゴミ箱の「ペットボトル」に捨ててください。\"}",
        "format_ok": false,
        "format_reason": "missing_key",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": false
        },
        {
        "question": "執務室内でのゴミの分別ルールと廃棄場所を教えてください",
        "raw": "{\"answer\": \"燃える、ペットボトル、缶・ビンへ捨ててください。\"}",
        "format_ok": false,
        "format_reason": "missing_key",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": false
        },
        {
        "question": "ペットボトルや缶はどこに廃棄すればよいですか",
        "raw": "{\"answer\": \"ペットボトルや缶は、執務室の角にある分別ゴミ箱（燃える、ペットボトル、缶・ビン）へ捨ててください。\"}",
        "format_ok": false,
        "format_reason": "missing_key",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": false
        },
        {
        "question": "パソコンの貸出申請はどこで行いますか",
        "raw": "{\"answer\": \"確認が必要\"}",
        "format_ok": false,
        "format_reason": "missing_key",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": true
        },
        {
        "question": "食堂の決済は交通系ICカードが使えますか",
        "raw": "{\"answer\": \"確認が必要\"}",
        "format_ok": false,
        "format_reason": "missing_key",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": true
        },
        {
        "question": "食堂のランチの平均予算はいくらですか",
        "raw": "{\"answer\": \"確認が必要\"}",
        "format_ok": false,
        "format_reason": "missing_key",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": true
        },
        {
        "question": "複合機でスキャンしたデータはどこに送られますか",
        "raw": "{\"answer\": \"複合機での印刷時は、ICカードをリーダーにタッチして認証してください。\"}",
        "format_ok": false,
        "format_reason": "missing_key",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": true
        },
        {
        "question": "会議室のキャンセル方法を教えてください",
        "raw": "{\"answer\": \"グループウェアの『カレンダー』から会議室の予約を15分単位で行えます。\"}",
        "format_ok": false,
        "format_reason": "missing_key",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": true
        },
        {
        "question": "ゴミ箱の回収頻度は週に何回ですか",
        "raw": "{\"answer\": \"確認が必要\"}",
        "format_ok": false,
        "format_reason": "missing_key",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": true
        }
    ]
    }

    # ◆実装（学習後）：
    {
    "summary": {
        "label": "after",
        "n": 21,
        "format_rate": 1.0,
        "content_rate": 0.8095238095238095,
        "both_rate": 0.8095238095238095,
        "seconds": 45.4
    },
    "rows": [
        {
        "question": "社内Wi-Fiに接続したい",
        "raw": "{\"answer\": \"社内Wi-FiのSSIDは 'Office-Guest'、パスワードは 'Welcome2026' です。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "社内ネットワークの接続情報を教えてください",
        "raw": "{\"answer\": \"この FAQ には記載がありません。確認が必要です。\", \"needs_review\": true}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": false
        },
        {
        "question": "ゲスト用のWi-Fi情報はどこに載っていますか",
        "raw": "{\"answer\": \"社内Wi-FiのSSIDは 'Office-Guest'、パスワードは 'Welcome2026' です。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "ランチは何時からですか",
        "raw": "{\"answer\": \"この FAQ には記載がありません。運営に確認が必要です。\", \"needs_review\": true}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": false
        },
        {
        "question": "12階の食堂のオープン時間は何時から何時までですか",
        "raw": "{\"answer\": \"社員食堂は12Fにあり、営業時間は11:30〜14:00です。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "社内でご飯を食べられる場所と時間を教えてください",
        "raw": "{\"answer\": \"社員食堂は12Fにあり、営業時間は11:30〜14:00です。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "複合機の利用方法",
        "raw": "{\"answer\": \"複合機での印刷時は、ICカードをリーダーにタッチして認証してください。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "複合機で印刷を実行する際に必要な認証方法は何ですか",
        "raw": "{\"answer\": \"複合機での印刷時は、ICカードをリーダーにタッチして認証してください。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "紙を印刷するときにタッチするものは何ですか",
        "raw": "{\"answer\": \"複合機での印刷時は、ICカードをリーダーにタッチして認証してください。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "会議室はどうやって取りますか",
        "raw": "{\"answer\": \"会議室の予約は、グループウェアの『カレンダー』から15分単位で行えます。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "グループウェアでの会議室の予約単位を教えてください",
        "raw": "{\"answer\": \"会議室の予約は、グループウェアの『カレンダー』から15分単位で行えます。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "会議室のスケジュール登録はどこで行いますか",
        "raw": "{\"answer\": \"会議室の予約は、グループウェアの『カレンダー』から15分単位で行えます。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "ペットボトルはどこへ？",
        "raw": "{\"answer\": \"ゴミは、執務室の角にある分別ゴミ箱（燃える、ペットボトル、缶・ビン）へ捨ててください。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "執務室内でのゴミの分別ルールと廃棄場所を教えてください",
        "raw": "{\"answer\": \"ゴミは、執務室の角にある分別ゴミ箱（燃える、ペットボトル、缶・ビン）へ捨ててください。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "ペットボトルや缶はどこに廃棄すればよいですか",
        "raw": "{\"answer\": \"ゴミは、執務室の角にある分別ゴミ箱（燃える、ペットボトル、缶・ビン）へ捨ててください。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": false
        },
        {
        "question": "パソコンの貸出申請はどこで行いますか",
        "raw": "{\"answer\": \"この FAQ には記載がありません。確認が必要です。\", \"needs_review\": true}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": true
        },
        {
        "question": "食堂の決済は交通系ICカードが使えますか",
        "raw": "{\"answer\": \"食堂は12Fにあり、営業時間は11:30〜14:00です。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": true
        },
        {
        "question": "食堂のランチの平均予算はいくらですか",
        "raw": "{\"answer\": \"この FAQ には記載がありません。運営に確認が必要です。\", \"needs_review\": true}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": true
        },
        {
        "question": "複合機でスキャンしたデータはどこに送られますか",
        "raw": "{\"answer\": \"複合機での印刷時は、ICカードをリーダーにタッチして認証してください。\", \"needs_review\": false}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": false,
        "both_ok": false,
        "gold_needs_review": true
        },
        {
        "question": "会議室のキャンセル方法を教えてください",
        "raw": "{\"answer\": \"この FAQ には記載がありません。確認が必要です。\", \"needs_review\": true}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": true
        },
        {
        "question": "ゴミ箱の回収頻度は週に何回ですか",
        "raw": "{\"answer\": \"この FAQ には記載がありません。確認が必要です。\", \"needs_review\": true}",
        "format_ok": true,
        "format_reason": "",
        "content_ok": true,
        "both_ok": true,
        "gold_needs_review": true
        }
    ]
    }
- ファインチューニングが向く場面・向かない場面についての考察：
    基礎、実装ともに学習後はフォーマットの不備がなくなっていたことから回答を整えるのには有用であると考えられる。一方で、学習後も回答の内容の失敗は残っており、正確な回答が求められるときはRAGなどの別の技術を用いたほうが良いと考えた。
