# 特許CSV入力アダプター

このファイルは、`otb_patents_list.csv`の1行を要求機能②のCapability Cardへ変換する規則を定める。CSVは1行を1公報として扱う。

## 1. 対象行の選択

1. `公報番号`を一次キーとする。
2. 複数行CSVに対してユーザーが公報番号を指定した場合、完全一致する1行だけを読む。
3. 公報番号が未指定の場合、`公報番号`と`発明の名称`だけを一覧表示し、選択を待つ。
4. 同一・類似の題名があっても題名だけで選択しない。
5. 複数公報を自動で結合しない。複数指定時は「独立に処理」か「一つの特許群として統合」かを確認する。

## 2. CSV列の読み替え

| CSV列 | Capability Cardでの用途 | 扱い |
|---|---|---|
| 公報番号 | `patent_or_seed_id` | 原文FACT |
| 発明の名称 | `title` | 原文FACT |
| url | `evidence.source_url` | 原文FACT |
| 技術分野 | `domain`、`existing_situations`の手掛かり | 原文はFACT、用途への抽象化はINFERENCE |
| 背景技術 | `prior_art`、既存文脈 | 特許記載としてFACT |
| 発明が解決しようとする課題 | `problem` | 特許記載としてFACT |
| 課題を解決するための手段 | `mechanism`の中心 | 特許記載としてFACT。請求項と照合する |
| 発明の効果 | `claimed_effect` | 「特許が主張する効果」としてFACT。実証済み事実とはみなさない |
| 発明の概要 | `mechanism`、`capability`、`input_output`の補助 | 原文はFACT、能力表現への抽象化はINFERENCE |
| 発明を実施するための形態 | `conditions`、`constraints`、実施例 | 空欄はUNKNOWN |
| 特許請求の範囲 | `mechanism`、`required_elements`、権利範囲 | 原文FACT。発明の必須要素を優先して抽出する |

## 3. Capability Card出力

発散前確認票の前に、内部的に次の項目を作る。

- `patent_or_seed_id`
- `title`
- `mechanism`
- `capability`
- `input_output`
- `conditions`
- `constraints`
- `existing_situations`
- `evidence`
- `unknowns`

`capability`は製品名や現在用途ではなく、他産業へ移せる動詞句で書く。例：`物体固有の応答差を検出し、非接触で同一性を判定する`。

## 4. 根拠区分

- `FACT`：選択行の原文に明示される内容。
- `INFERENCE`：複数の原文記載から導いた技術能力・条件・既存用途の抽象化。
- `ASSUMPTION`：原文だけでは確定せず、発散のために置く仮定。
- `UNKNOWN`：選択行に情報がない、または判断できない内容。

FACTには、可能な限り根拠列名を付ける。空欄や不足情報を他の公報行から補完してはならない。

## 5. 禁止事項

- CSV全行を一つの特許として要約する。
- 題名が似ている公報を同一発明と断定する。
- `発明の効果`を外部で検証済みの効果として表現する。
- 空欄を推測でFACTにする。
- 対象行が確定する前にStakeholder、Situation距離、候補を生成する。
