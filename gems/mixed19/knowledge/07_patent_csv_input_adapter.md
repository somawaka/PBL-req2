# 特許CSV入力アダプター

`otb_patents_list.csv`の1行をReq②のCapability Cardへ変換する。CSVは1行を1公報として扱う。

## 対象行

1. `公報番号`を一次キーとする。
2. 公報番号指定時は完全一致する1行だけを読む。
3. 未指定時は公報番号と発明の名称を表で表示し、選択を待つ。
4. 類似題名だけで同一発明と判断しない。
5. 複数公報を自動で結合しない。

## CSV列の読み替え

| CSV列 | Capability Cardでの用途 | 扱い |
|---|---|---|
| 公報番号 | patent_or_seed_id | 原文FACT |
| 発明の名称 | title | 原文FACT |
| url | evidence.source_url | 原文FACT |
| 技術分野 | domain、existing_situationsの手掛かり | 原文はFACT、用途抽象化はINFERENCE |
| 背景技術 | prior_art、既存文脈 | 特許記載としてFACT |
| 発明が解決しようとする課題 | problem | 特許記載としてFACT |
| 課題を解決するための手段 | mechanismの中心 | 特許記載としてFACT。請求項と照合する |
| 発明の効果 | claimed_effect | 特許が主張する効果としてFACT。外部実証済みとはみなさない |
| 発明の概要 | mechanism、capability、input_outputの補助 | 原文はFACT、能力抽象化はINFERENCE |
| 発明を実施するための形態 | conditions、constraints、実施例 | 空欄はUNKNOWN |
| 特許請求の範囲 | mechanism、required_elements、権利範囲 | 原文FACT。必須要素を優先する |

## Capability Card

- patent_or_seed_id
- title
- mechanism
- capability
- input_output
- conditions
- constraints
- existing_situations
- evidence
- unknowns

capabilityは現在の製品・用途名ではなく、他産業へ移せる動詞句で書く。

## 根拠区分

- FACT：選択行の原文に明記された内容
- INFERENCE：原文から導いた抽象化
- ASSUMPTION：発散のために置く仮定
- UNKNOWN：選択行に情報がない内容

空欄を別の公報行から補完しない。対象行確定前に距離分類・候補生成を開始しない。

