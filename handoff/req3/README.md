# Mixed19｜Req②からReq③への出力仕様

## 結論

Req③が受け取る単位は、**意味的価値候補1件につき1行、全17列**です。

17列のうち中心となる成果は `interpretation` です。これは、

> このStakeholderが、このSituationに置かれ、このContextから見たとき、この特許はどのような意味・価値を持つのか

を自然言語で表した、Req②の発散結果そのものです。

他の列は、`interpretation` を理解・評価・追跡するための補助情報です。Req②では候補を採点・足切りせず、未評価の `IDEA / HYPOTHESIS` としてReq③へ渡します。

## 出力の読み方

| 層 | 主な列 | 答える問い | Req③での役割 |
|---|---|---|---|
| 発想の視点 | `stakeholder_*`、`situation_*`、`context_*`、`organization_archetype`、`role` | 誰が、どの産業・意味文脈から見ているか | 評価対象の前提条件を理解する |
| **意味的価値** | **`interpretation`** | **その視点から特許が持つ新しい意味・価値は何か** | **新規性・有用性・事業性・意外性等の主評価対象** |
| 技術との接続 | `technical_bridge` | 元特許の能力が、新しいSituationでなぜ機能し得るか | 技術適合性・実現可能性の根拠にする |
| 行動・関係の変化 | `behavior_change` | 導入前後で判断・行動・関係がどう変わるか | 単なる用途名ではなく意味的価値になっているかを見る |
| 不確実性 | `assumption`、`evidence_status` | 何が未確認で、どこまでが事実・推論・仮定か | リスクと追加調査項目を特定する |
| 識別・被覆 | `candidate_id`、`distance`、`coverage_rotation`、`duplicate_note` | どの候補で、どの探索条件から生まれたか | 欠落・類似・探索偏りを確認する |

## Mixed19の候補カラム

候補表では、次の順序を固定します。

1. `candidate_id`
2. `stakeholder_id`
3. `stakeholder_name`
4. `situation_id`
5. `situation_name`
6. `distance`
7. `coverage_rotation`
8. `context_id`
9. `context_name`
10. `organization_archetype`
11. `role`
12. `interpretation`
13. `technical_bridge`
14. `behavior_change`
15. `assumption`
16. `evidence_status`
17. `duplicate_note`

各列の定義、生成主体、設置理由、Req③での使い方は `mixed19_candidate_schema.csv` またはWorkbookの `Column Guide` シートに記載しています。

## 特に重要な列

### interpretation

Req②が発散する**意味的価値仮説**です。単なる転用先・用途名ではなく、技術がStakeholderの認識、判断、行動、関係、責任などをどう変えるかまで含めます。Req③はこの列を主評価対象にします。

### technical_bridge

元特許のどの能力を、対象Situationの何へ接続するのかを説明します。`interpretation` が単なる連想ではなく、技術に接続した仮説であるかを確かめるための列です。

### behavior_change

導入前と導入後の違いを示します。用途を挙げただけの候補と、Stakeholderに新しい意味的価値を生む候補を区別する助けになります。

### assumption

候補成立に必要だが、入力特許だけでは確認できない条件です。Req②では不確実だからという理由で候補を削除せず、Req③の検証課題として残します。

### evidence_status

`technical_bridge` の根拠状態を `FACT / INFERENCE / ASSUMPTION` で示します。候補全体の品質点や採否ではありません。

### duplicate_note

似ている候補がある場合に、相手のIDと「似ていても残す差」を記録します。Req②では削除せず、Req③で統合・代表化を検討します。類似がなければ `none` です。

## 固定情報とAI生成情報

| 区分 | 列 |
|---|---|
| 固定分類・決定論的計算 | `candidate_id`、Stakeholder、Situation、`coverage_rotation`、Context |
| AI推論後に人間が承認 | `distance` |
| AIが生成する仮説 | `organization_archetype`、`role`、`interpretation`、`behavior_change`、`assumption`、`duplicate_note` |
| 特許事実とAI推論を組み合わせる | `technical_bridge`、`evidence_status` |

AIは不足情報を事実として補完しません。推論や成立条件は、それぞれ `evidence_status` と `assumption` に明示します。

## ファイル

| ファイル | 用途 |
|---|---|
| `mixed19_candidate_schema.csv` | 17列の定義、設置理由、Req③での使い方 |
| `mixed19_candidate_sample.csv` | OTB094「電磁指紋」を用いた候補6件 |
| `mixed19_output_guide.xlsx` | 上記を人が読みやすい4シートに整理したWorkbook |

サンプルは `near`、`adjacent`、`far` を各2件含みます。完全なGem/API実行結果でも、品質評価済みの候補でもありません。Req③の入力設計、評価列設計、Gem表示を試すためのfixtureです。

## Req③での推奨取扱い

1. `interpretation` を主評価対象とする。
2. `technical_bridge`、`behavior_change`、`assumption` を評価理由と検証課題に利用する。
3. `distance` は品質点ではなく、探索条件・比較軸として扱う。
4. `evidence_status` は `technical_bridge` の根拠区分として読む。
5. Req②の17列は上書きせず、Req③の評価点、理由、判定、統合先ID等を新しい列として追加する。

Schema version: `mixed19-req2-output-v0.2`
