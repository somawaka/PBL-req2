# Req2 → Req3 受け渡し仕様

## 目的

Req2が生成するBtoB文脈・意味的価値候補を、Req3の評価Gemまたは将来のバックエンドへ渡すための暫定インターフェースです。

現時点ではGemini APIによる570件等の完全実行を行わず、カラム定義と少数の設計サンプルを提供します。

## ファイル

| ファイル | 用途 |
|---|---|
| `req2_candidate_schema.csv` | 候補カラムの型、必須性、適用方式、意味、Req3で必要な理由 |
| `req2_candidate_sample.csv` | OTB094「電磁指紋」を用いた6件のサンプル |
| `req2_run_manifest_sample.csv` | 方式、予定候補数、batch、距離、rotationとサンプル行の対応 |
| `req2_output_contract.xlsx` | 上記を人が確認しやすいWorkbookにまとめたもの |

CSVはUTF-8です。Gemへ渡す場合は、まずREADMEとschemaをKnowledgeとして参照させ、評価対象としてcandidate sampleを入力します。

## 現行Gem出力との関係

現行Gemは、発散前にRun ManifestをMarkdown表で表示し、発散中は候補をbatch単位のMarkdown表で表示します。Gem単体には複数batchを自動でCSVへ統合・保存する機能がありません。

このサンプルCSVでは、Req3へ渡す際の追跡性を確保するため、現行候補列の前に次の4列を追加しています。

| 追加列 | 出所 | 意味 |
|---|---|---|
| `run_id` | Run Manifest | Req2の実行単位 |
| `mode` | Run Manifest | FULL19 / COVERAGE12 / MIXED19 |
| `patent_id` | 入力・Run Manifest | 元特許・技術シーズ |
| `batch_id` | Run Manifest | Situationまたはfrontier branch |

候補本体の列は、Stakeholder、Situation、Context、Organization Archetype、Role、Interpretation、Technical Bridge、Behavior Change、Assumption、Evidence Status、Duplicate Noteを中心とします。方式固有列として、Coverage12のoverlay、Mixed19のcoverage rotationがあります。

## 識別ルール

Req3側の候補主キーは、`candidate_id`単独ではなく次を使用します。

`run_id + candidate_id`

同じ特許をFull19、Coverage12、Mixed19で実行すると、同じ`candidate_id`が別runに現れる可能性があるためです。

## 空欄とUNKNOWN

- 空欄：その方式では構造的に該当しない。例：Full19の`overlay_id`、Coverage12の`coverage_rotation`
- `UNKNOWN`：本来確認したい情報だが入力や根拠から判定できない
- `ASSUMPTION`：候補を成立させるために明示的に置いた仮定

## Req3での取扱い

1. Run Manifestを読み、方式、予定候補数、batch構成を確認する。
2. `run_id + candidate_id`の重複と、batchごとの欠落を検査する。
3. Interpretationを評価対象の中心とする。
4. Technical Bridge、Behavior Change、Assumptionを、評価理由と検証課題に利用する。
5. Req2の元列は上書きせず、Req3の評価点、理由、判定、統合先ID等を新しい列として追加する。

`evidence_status`はTechnical Bridgeの根拠状態です。候補全体が実証済みか、良い候補かを示す点数ではありません。

`duplicate_note`もReq2による削除結果ではありません。似ている候補を残したまま、Req3で統合・代表化を検討するためのメモです。

## サンプルの位置付け

サンプルはOTB094「電磁指紋」の既存期待出力を、現行Full19 / Coverage12 / Mixed19のカラムへ写像した設計例です。

- 完全なGem実行結果ではありません。
- 候補の品質評価は行っていません。
- 570件、360件、Mixed19全件を代表する統計標本ではありません。
- Req3の入力設計と表示確認のためのfixtureです。

Schema version: `req2-req3-contract-v0.1`
