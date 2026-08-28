# 2種類のGem 作成・試験手順

## 1. 今回作るGem

### Gem A：PBL Req2 Full-19

- Situation：日本標準産業分類19件をすべて使用。
- Distance：near / adjacent / farを表示するが、選別には使わない。
- 発散数：19 Situation × 5 Stakeholder × 6 Context = 570件。
- 1回の出力：1 Situation、30件。

### Gem B：PBL Req2 Coverage-12

- Situation：19件を距離分類後、near 3 / adjacent 3 / far 4を選択。
- Frontier：8 overlayから2件を選び、基礎JSIC Situationと組み合わせる。
- 発散数：12 branch × 5 Stakeholder × 6 Context = 360件。
- 1回の出力：1 branch、30件。

両GemでStakeholder 5、Context 6、出力形式、会話手順を同じにする。これにより、Situation処理の違いを比較できる。

## 2. Gem Aの作成

1. GeminiのGems管理画面で新しいGemを作る。
2. 名前を`PBL Req2 Full-19`とする。
3. Instructions欄へ`02_full19_gem_instructions.md`の本文を貼る。
4. Knowledgeへ次の6ファイルを追加する。
   - `01_stakeholder_framework.csv`
   - `02_situation_framework.csv`
   - `03_context_framework.csv`
   - `07_generation_rules_common.md`
   - `01_interaction_protocol.md`
   - `08_patent_csv_input_adapter.md`
5. Previewで後述のテスト入力を実行する。
6. Instructionsが勝手に変更されていないことを確認し、保存する。

## 3. Gem Bの作成

1. 新しいGemをもう1つ作る。
2. 名前を`PBL Req2 Coverage-12`とする。
3. Instructions欄へ`03_coverage12_gem_instructions.md`の本文を貼る。
4. Knowledgeへ次の7ファイルを追加する。
   - `01_stakeholder_framework.csv`
   - `02_situation_framework.csv`
   - `03_context_framework.csv`
   - `07_generation_rules_common.md`
   - `01_interaction_protocol.md`
   - `04_coverage_overlay_framework.csv`
   - `08_patent_csv_input_adapter.md`
5. 同じ特許でPreviewする。
6. 保存する。

`OTB094_cartesian_grid.csv`や`OTB094_situation_batches.jsonl`は特定特許用の実行データであり、GemのKnowledgeには追加しない。

## 4. 最初の入力

特許PDF、特許本文、要求機能①のCapability Card、または`otb_patents_list.csv`をGemの会話に添付する。特許CSVは会話ごとの入力データであり、固定Knowledgeには追加しない。

公報番号が決まっている場合は、次を送る。

```text
添付CSVの公報番号 JPxxxxxxxxxx を対象に要求機能②を開始してください。
まず対象行だけを読み込み、特許を分析し、共通対話プロトコルの「状態1：発散前確認票」までを出してください。
この時点では候補発散を開始しないでください。
```

公報番号をまだ決めていない場合は、次を送る。

```text
添付CSVから、公報番号と発明の名称だけの一覧を表示してください。
私が対象を指定するまで、特許分析・距離分類・候補発散は開始しないでください。
```

PDF、本文、Capability Cardを1件だけ入力する場合は、次を送る。

```text
添付した特許を対象に要求機能②を開始してください。
まず特許を分析し、共通対話プロトコルの「状態1：発散前確認票」までを出してください。
この時点では候補発散を開始しないでください。
```

## 5. 人間が行う確認

発散前確認票で次を確認する。

- 特許のCore Mechanism / Capabilityが正しいか。
- 既存用途と技術制約が正しいか。
- Stakeholder S1〜S5がすべて表示されているか。
- 19 Situationがすべてnear / adjacent / farへ分類されているか。
- 距離理由が特許能力に基づいているか。
- Coverage版はnear 3 / adjacent 3 / far 4 / frontier 2になっているか。
- Context C1〜C6がすべて使われるか。
- 予定候補数がFull 570、Coverage 360になっているか。

問題がなければ`承認`、修正したければ例えば次のように返す。

```text
修正:
- Situation B「漁業」はfarではなくadjacentとしてください。理由は〇〇です。
- S2のこの特許との関係は、導入企業内の品質保証部門を中心にしてください。
修正後の確認票を再提示し、まだ発散は開始しないでください。
```

GemがRun Manifestを返したら内容を確認し、`開始`と送る。以降は1batchごとに`次へ`を送る。

## 6. バックエンドは今すぐ必要か

最初の目的が会話フロー、距離分類、30候補の品質を確かめることであれば、バックエンドは不要である。まず両Gemで次を行う。

1. 同じ特許を入力。
2. 発散前確認票を比較。
3. 人間が修正・承認。
4. 最初の2〜3batchだけ生成。
5. 欠落、重複、意外性、説明可能性を比較。

最初から570件と360件を最後まで手作業で生成する必要はない。プロンプトと状態遷移を先に検証する。

## 7. バックエンドが必要になる条件

次を行う段階ではバックエンドを作る。

- 570件・360件を自動で最後まで生成する。
- Candidate IDを機械的に採番・検査する。
- 承認したRun Manifestを保存し、途中再開する。
- 失敗batchだけ再実行する。
- 全batchをCSVへ結合する。
- 2方式の処理時間・コスト・出力品質を記録する。
- 複数特許を連続評価する。

## 8. バックエンド段階でユーザーが行うこと

1. Google AI Studioまたは利用するGoogle Cloud環境でAPIキーと課金条件を確認する。
2. APIキーをローカル環境変数`GEMINI_API_KEY`へ設定する。チャットやファイル本文へ貼らない。
3. 利用可能なGeminiモデルを選ぶ。
4. 特許情報をAPIへ送信してよいか、機密区分を三菱電機側と確認する。
5. こちらが用意するバックエンドコードをローカルまたは承認済みクラウド環境で実行する。

コード側は、確認票保存、承認待ち、2方式のbranch確定、30件batch生成、結果検査、CSV結合まで共通化できる。

## 9. CSV入力の注意

- 現在のCSVは1行を1公報として扱う。
- 同一または類似の発明名称があっても、`公報番号`で区別する。
- `発明を実施するための形態`が空欄の場合は`UNKNOWN`とし、別行から補完しない。
- 複数公報を一つの技術シーズとして扱う場合は、将来`技術シーズID`、`代表公報`、`公報間の関係`をCSVへ追加する。その運用が決まるまでは1公報ずつ試す。
