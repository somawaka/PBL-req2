# PBL Req2 GemC：Mixed-Coverage19

GemCは、三菱電機OTB特許からBtoBの意味的価値候補を発散するReq②プロトタイプである。

全19産業を残し、既存用途からの距離に応じて各産業内の探索密度を変更する。

| distance | 候補数 / 産業 | 探索方法 |
|---|---:|---|
| near | 6 | rotation 0 |
| adjacent | 12 | rotation 0, 1 |
| far | 30 | 5 Stakeholder × 6 Contextの全直積 |

## Gem作成手順

1. Geminiで新しいGemを作る。
2. 名前を`PBL Req2 Mixed-Coverage19`とする。
3. `01_gemc_mixed_coverage_instructions.md`の本文をInstructionsへ貼る。
4. `knowledge/`内の7ファイルをKnowledgeへ追加する。
5. `test/01_test_prompts.md`の入力でPreviewを行う。
6. `test/02_test_checklist.csv`で挙動を確認する。

## Knowledgeへ追加するファイル

- `01_stakeholder_framework.csv`
- `02_situation_framework.csv`
- `03_context_framework.csv`
- `04_mixed_coverage_rules.md`
- `05_generation_rules_common.md`
- `06_interaction_protocol_gemc.md`
- `07_patent_csv_input_adapter.md`

特許CSV、特許PDF、Capability Cardは固定Knowledgeではなく、会話開始時の入力として渡す。

## 会話フロー

1. 人間：特許情報または特許CSVを入力する。
2. Gem：対象特許を確定し、特許理解、Stakeholder、19産業のdistance、探索密度、候補総数を提示する。
3. 人間：`承認`または修正指示を返す。
4. Gem：Run Manifestを表示し、`開始`を待つ。
5. 人間：`開始`と送る。
6. Gem：A〜S順に1 Situationずつ、候補をMarkdown表で生成する。
7. 人間：各batch後に`次へ`と送る。

## GemA / GemB / GemCの違い

| Gem | Situation | Stakeholder × Context | 候補数 |
|---|---|---|---:|
| A Full-19 | 19産業すべて | 全産業で30件 | 570 |
| B Coverage-12 | 12 branchを選択 | 選択branchで30件 | 360 |
| C Mixed-Coverage19 | 19産業すべて | near 6 / adjacent 12 / far 30 | 特許ごとに可変 |

## 出力形式

GemCでは、各batchの候補一覧を必ずMarkdown表で表示する。GemBで見られた箇条書き形式への変更を禁止している。

## 現在の制約

Gemでは1回の応答で1 Situationを安定運用単位とするため、各batch後に`次へ`が必要である。全19batchの自動実行、結果保存、欠落検査、部分再実行、CSV結合は将来のGemini APIバックエンドで行う。

