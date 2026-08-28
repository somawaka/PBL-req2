# Mixed19

19産業を一つも削除せず、各産業内の探索密度をnear 6、adjacent 12、far 30へ変える方式です。

## Gemの作成

1. `instructions.md` の本文をGemの「指示」へ貼り付ける。
2. `knowledge/` 内の7ファイルをすべてKnowledgeへ追加する。
3. `tests/prompts.md` と `tests/checklist.csv` を使ってPreviewを確認する。
4. 特許CSV、特許PDF、またはCapability Cardは、会話開始時に入力する。

## 実行

`特許入力 → 19産業の距離分類と探索密度 → 人間確認 → 承認 → Run Manifest → 開始 → 1産業ずつ生成 → 次へ`

合計候補数は `6 × N_near + 12 × N_adjacent + 30 × N_far` です。farは低評価という意味ではなく、意外な意味的価値を逃さないため最も深く探索します。

各batchの候補一覧はMarkdown表で出力します。
