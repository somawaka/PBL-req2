# Coverage12

19産業を確認したうえで、near 3、adjacent 3、far 4、frontier 2の合計12枝を選択し、各枝で全直積する方式です。

## Gemの作成

1. `instructions.md` の本文をGemの「指示」へ貼り付ける。
2. `knowledge/` 内の7ファイルをすべてKnowledgeへ追加する。
3. 特許CSV、特許PDF、またはCapability Cardは、会話開始時に入力する。

## 実行

`特許入力 → 19産業の距離分類と12枝の提案 → 人間確認 → 承認 → Run Manifest → 開始 → 1枝30件 → 次へ`

候補は12batch、合計360件です。候補生成後の価値評価ではなく、生成前のSituation被覆制御として使います。
