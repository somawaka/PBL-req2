# PBL Req2 — BtoB文脈発散プロトタイプ

三菱電機Open Technology Bank（OTB）の特許から、人間が思いつきにくいBtoBの利用文脈と意味的価値候補を発散する「要求機能②」の研究用プロトタイプです。

このリポジトリは候補の評価・選別を目的としません。新規性、有用性、事業性、技術適合性、実現可能性などの評価は、後段の「要求機能③」で行う想定です。

## 3つの探索方式

| 方式 | Situationの扱い | 1 Situation内の探索 | 想定候補数 | 主な用途 |
|---|---|---|---:|---|
| [Full19](gems/full19/) | 日本標準産業分類19区分をすべて使用 | Stakeholder 5 × Context 6の全直積 | 570 | 全探索の基準・比較対象 |
| [Coverage12](gems/coverage12/) | near 3、adjacent 3、far 4、frontier 2を選択 | 選択した12枝で全直積 | 360 | Situationを被覆制約付きで絞る実験 |
| [Mixed19](gems/mixed19/) | 19区分をすべて保持 | near 6、adjacent 12、far 30 | 特許ごとに可変 | 全産業を残しつつ探索密度を変える実験 |

詳しい処理、違い、使い分けは [docs/methods.md](docs/methods.md) を参照してください。

## 使い始める

1. 比較したい方式を上表から選び、そのフォルダの `README.md` を読む。
2. `instructions.md` の本文をGemの「指示」へ貼り付ける。
3. 同じ方式の `knowledge/` 内にあるファイルをすべてGemのKnowledgeへ追加する。
4. 会話開始時に [data/otb_patents_list.csv](data/otb_patents_list.csv)、特許PDF、またはReq①のCapability Cardを入力する。
5. Gemが提示する特許理解・Stakeholder・Situation・Context・候補数を人間が確認する。
6. `承認`、続いて `開始` と入力し、各batch後に `次へ` と入力する。

特許データは固定Knowledgeではなく、実行ごとの会話入力です。

## リポジトリ構成

| パス | 内容 |
|---|---|
| `gems/` | 現行のGem A/B/C。各フォルダは単独で利用できるよう自己完結させています |
| `docs/` | 探索方式、設計判断、使い分けの説明 |
| `data/` | 実行時に入力する特許データと取扱説明 |
| `handoff/req3/` | Mixed19がReq③へ渡す17列の候補スキーマと出力例 |
| `_archive/` | 過去の設計・試作。現行Gemへの投入対象ではありません |

各Gemで共通ファイルが重複しているのは意図的です。共有相手が1方式だけを取得して、そのフォルダ内でGem作成を完結できることを優先しています。

## Req③への受け渡し

Mixed19の候補カラムと少数の出力例は [handoff/req3/](handoff/req3/) を参照してください。Req②の主成果である `interpretation` と、それを支える `technical_bridge`、`behavior_change`、`assumption` 等の関係を説明しています。完全なAPI実行結果ではなく、Req③の入力設計とGem試作に使うためのインターフェース例です。

## 共通の会話フロー

`特許入力 → AIによる特許理解と探索計画 → 人間の確認・修正 → Run Manifest固定 → batch発散`

人間の承認前には候補生成を始めません。Stakeholder、Situationの距離分類、探索密度、候補数を先に確認することで、大量生成後の出戻りを防ぎます。

## 現在の制約

Gemini Gemでは、一度の応答で全産業分を安定して出力することが難しいため、現状は1回1産業（または1枝）をbatchとして生成し、`次へ` の入力で進めます。無人連続実行、並列化、結果保存、欠落検査、部分再実行、CSV結合には、将来的にGemini APIを用いたバックエンドが必要です。

## 共有時の注意

- 本リポジトリは研究・試作段階です。生成候補は未評価のIDEA / HYPOTHESISです。
- 外部共有前に、入力する特許情報・会議資料・実験結果の共有可否を確認してください。
- ライセンスは未設定です。利用範囲を広げる場合は、共同研究先と方針を決めてください。
- ZIPはソースと重複し更新漏れを起こすため管理対象から外しています。必要な場合はGitHubの「Download ZIP」またはReleaseで配布してください。
