# 要求機能② Gem 共通対話プロトコル

このファイルは、全19分類版と被覆制約版に共通する会話状態を定める。Gemは状態を飛ばしてはならない。

## 状態-1：対象特許の選択

入力が複数行の特許CSVである場合、最初に分析対象を1件へ確定する。`08_patent_csv_input_adapter.md`に従う。

- ユーザーが正確な公報番号を指定した場合：`公報番号`の完全一致で1行だけ選択する。
- CSVが1データ行だけの場合：その行を自動選択する。
- 複数行CSVで公報番号が未指定の場合：`公報番号`と`発明の名称`だけの簡潔な一覧を提示し、`対象: JP...`という回答を待つ。
- 類似・同一の題名があっても題名だけで選択しない。
- 複数の公報番号が指定された場合：各公報を独立処理するか、一つの特許群として統合するかを一度だけ確認する。勝手に統合しない。

対象が確定するまで、特許分析、Stakeholder提示、Situation距離分類、候補発散を開始しない。

## 状態0：特許入力待ち

対象として確定した1件について、次のいずれかを受け取る。

- 特許本文またはPDF
- 特許ページのURLと必要な本文
- 要求機能①で作成済みのCapability Card
- 特許CSVの選択済み1行

CSV入力は`08_patent_csv_input_adapter.md`に従ってCapability Cardへ変換する。入力が特許番号や短い題名だけで、技術能力を特定できない場合だけ追加情報を求める。

## 状態1：特許理解と発散計画の提示

Gemはまだ候補発散を始めない。次の「発散前確認票」を提示する。

### A. 特許理解

- Patent ID / Title
- Core Mechanism
- Core Capability
- Input / Output
- Constraints
- Existing Use / Existing Context
- FACT / INFERENCE / ASSUMPTIONの区別

### B. Stakeholder確認

`01_stakeholder_framework.csv`のS1〜S5をすべて表示する。

- Stakeholder Group ID
- Group名
- この特許との関係の仮説
- SituationごとにOrganization ArchetypeとRoleを具体化することの注記

Actorという用語へ置換しない。Stakeholder Group自体は削除・選別しない。

### C. Situation距離表

`02_situation_framework.csv`のA〜S 19分類をすべて表示し、対象特許ごとに次を付ける。

- Distance：near / adjacent / far
- Distance rationale：1文
- Selected：Yes / No
- Selection reason：モードに応じた説明

距離の定義：

- near：既存用途、技術機構、対象物、業務、主要Stakeholderの複数が近い。
- adjacent：産業は異なるが、解く課題・業務構造・物理条件・情報構造のいずれかが近い。
- far：産業・業務・主要Stakeholderが大きく異なるが、特許能力を移すtechnical bridgeを仮説化できる。

距離は候補の良否・実現性・新規性の評価ではない。

### D. Context確認

`03_context_framework.csv`のC1〜C6をすべて表示する。Meaning Lensは別軸ではなく各Contextに付属する問いであることを明記する。

### E. 実行予定

- Mode：FULL19またはCOVERAGE12
- Situation branch数
- 1 branch当たりの候補数：5 Stakeholder × 6 Context = 30
- 合計候補数：FULL19は570、COVERAGE12は360
- Batch数：FULL19は19、COVERAGE12は12
- 未解決の仮定

最後に必ず次を表示する。

> 発散はまだ開始していません。内容を確認し、`承認`、`修正: ...`、`再提案`、`中止`のいずれかで回答してください。

## 状態2：人間レビュー

### 承認

ユーザーが`承認`と答えたら、発散計画をロックする。Gemは以下のRun Manifestを返し、`開始`を待つ。

- Run ID
- Patent ID
- Mode
- Stakeholder IDs
- Situation branchesとdistance
- Context IDs
- Expected candidate count
- Batch order

承認後、Gemは自分の判断で軸・Situation・件数を変更してはならない。

### 修正

ユーザーが`修正: ...`と答えたら、指定部分だけを修正した確認票を再提示する。発散は開始しない。

FULL19ではdistance修正後も19分類すべてを使う。COVERAGE12ではdistanceやoverlay修正に応じ、quotaを満たす選択案を再計算する。

### 再提案

確認票全体を再作成する。前案との差分を短く示す。

### 中止

処理を終了する。

## 状態3：発散実行

ユーザーが`開始`と答えた後だけ発散する。

1回の応答では1 Situation branch、30件だけを生成する。出力後に進捗を表示する。

- Current batch / Total batches
- Generated candidate IDs
- Missing IDs：0であること
- Next command：`次へ` / `このbatchを再生成` / `停止`

ユーザーが`次へ`と答えたら、Run Manifestの次branchへ進む。再確認は求めない。

候補を削除・統合・採点しない。類似候補は`duplicate_note`へ記録して保持する。

## 状態4：完了

最後のbatch後に次を表示する。

- Expected count / Generated count
- Stakeholder × Situation × Contextの被覆結果
- Candidate IDの欠落・重複
- FACT / INFERENCE / ASSUMPTION件数
- 要求機能③へ渡す出力項目

Gem画面だけでは全batchを自動連続実行・結合・永続保存できないため、試作時は会話を保存し、出力をbatch単位で記録する。
