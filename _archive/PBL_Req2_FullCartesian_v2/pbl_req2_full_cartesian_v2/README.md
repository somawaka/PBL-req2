# PBL 要求機能② 全直積版 v2

前版の24案選択方式を撤回し、合意済みの全直積へ戻した設計・実装素材である。

## 構成

- `00_design_report_v2.md`：フィードバック反映後の設計報告書。
- `01_stakeholder_framework.csv`：5 Stakeholder。
- `02_situation_framework.csv`：19 Situation。
- `03_context_framework.csv`：6 Contextとlens prompt。
- `04_generation_rules.md`：全直積・非削除・出力ルール。
- `05_api_system_instruction.md`：Gemini API用System Instruction。
- `06_test_capability_card_OTB094.md`：テスト入力。
- `scripts/build_cartesian_grid.py`：570セルの決定論的生成。
- `scripts/build_situation_batches.py`：30件×19 Situationへの分割。
- `scripts/submit_gemini_batch.py`：Gemini Batch API送信例。
- `scripts/validate_completed_csv.py`：全直積・ID・欠損の検査。
- `generated/OTB094_cartesian_grid.csv`：生成済み570セル骨格。
- `generated/OTB094_situation_batches.jsonl`：生成済み19 batch入力。

## ローカル生成

```bash
python scripts/build_cartesian_grid.py \
  --patent-id OTB094 \
  --patent-title "電磁指紋による真贋判定" \
  --output generated/OTB094_cartesian_grid.csv

python scripts/build_situation_batches.py \
  --grid generated/OTB094_cartesian_grid.csv \
  --capability-card 06_test_capability_card_OTB094.md \
  --output generated/OTB094_situation_batches.jsonl
```

## API送信例

`google-genai`と`pydantic`を導入し、`GEMINI_API_KEY`を設定してから実行する。モデル名は実行時点で利用可能なgenerateContent互換モデルを明示する。

```bash
python scripts/submit_gemini_batch.py \
  --batches generated/OTB094_situation_batches.jsonl \
  --system-instruction 05_api_system_instruction.md \
  --model YOUR_CURRENT_MODEL
```

Batch APIは非同期処理である。返されたjob nameで状態と結果を取得し、19出力をCSVへ結合後、`validate_completed_csv.py`で570セルを検査する。

## Gem画面で試す場合

Framework 3ファイルと`05_api_system_instruction.md`をKnowledge/指示として使い、`generated/OTB094_situation_batches.jsonl`から1行ずつ入力する。1回30件を全件返すことを確認する。Gem画面はプロンプト検証用、本実行はAPIを想定する。
