# PBL Req② Gemini Gem実装パッケージ v1.0

## まず行うこと

1. Google Geminiで新しいGemを作る。
2. `01_gem_instructions.md` の「以下をGemの指示欄へ貼り付ける」以降を指示へ貼る。
3. Knowledgeとして次の4ファイルを追加する。
   - `02_situation_framework.csv`
   - `03_stakeholder_framework.csv`
   - `04_meaning_lens_framework.csv`
   - `05_generation_rules.md`
4. `06_test_cases.md` のTC01をquickで実行する。
5. 出力を `08_evaluation_checklist.csv` で確認する。
6. quickが通ったら同じTC01をstandardで3回実行し、候補重複と再現性を測る。

## ファイル一覧

| file | purpose | Gem Knowledge |
|---|---|---|
| `00_design_report.md` | 現状整理、4案比較、推奨設計、根拠、未解決論点 | 不要 |
| `01_gem_instructions.md` | Gem指示欄へ貼る完成版 | 指示欄 |
| `02_situation_framework.csv` | JSIC 19＋横断overlay 8 | 必須 |
| `03_stakeholder_framework.csv` | 5 Actor Function | 必須 |
| `04_meaning_lens_framework.csv` | 4 family・12 Lens | 必須 |
| `05_generation_rules.md` | 生成、quota、重複、出力schema | 必須 |
| `06_test_cases.md` | OTB実例3件のテスト入力 | 不要 |
| `07_expected_output_sample.csv` | TC01 quickの期待出力サンプル12件 | 不要 |
| `08_evaluation_checklist.csv` | Gem動作検証チェックリスト | 不要 |

## 重要な読み方

- 12 Meaning Lensは完成版BtoB Context Mapではなく、Gem v1を動かし、実データから再クラスタリングするための暫定体系。
- JSICは全直積するリストでなく、遠い産業を見落とさない探索母集団。
- Stakeholder 5群は会社・組織・Roleの一覧でなく、Situation内で価値を担う機能の分類。
- Req②は候補を評価しない。Role詳細化、事業モデル、採点はReq③へ渡す。

