# 探索方式の説明

## 1. 共通する設計範囲

3方式はいずれも、Req①で理解した特許を入力として、Req②でBtoBの意味的価値候補を発散し、Req③へ未評価候補を渡します。

固定する主な分類は次のとおりです。

- Stakeholder：5 Group
- Situation：日本標準産業分類の大分類19区分
- Context：6つのBtoB意味文脈
- Interpretation：Stakeholder × Situation × Contextで特許が持つ意味・価値の仮説

Organization ArchetypeとRoleは固定軸ではありません。対象Situationに存在し得る組織類型と具体的役割として、LLMが各batchで具体化します。

## 2. Full19

### 処理

1. 19 Situationをnear / adjacent / farへ分類する。
2. 距離分類は表示・説明のために使い、Situationを削除しない。
3. 各SituationでStakeholder 5 × Context 6の全30tupleを生成する。
4. 19 × 30 = 570候補を得る。

### 意図

全直積を合意事項として実行する基準方式です。LLMに「良さそうな組合せ」を選ばせないため、常識的・既存用途に近い候補だけが残ることを防ぎます。

### 制約

19batchが必要で、Gemでは各batch後の `次へ` が必要です。候補数を減らさないため、出力量の問題は解消しません。

## 3. Coverage12

### 処理

1. 19 Situationをすべてnear / adjacent / farへ分類する。
2. quotaに従い、near 3、adjacent 3、far 4を選ぶ。
3. 8つの横断overlay候補からfrontier 2を選び、基礎Situationと組み合わせる。
4. 合計12 Situation branchを固定する。
5. 各branchでStakeholder 5 × Context 6の全30tupleを生成し、360候補を得る。

### 意図

候補の意味的価値を採点せず、生成前にSituationの被覆を制御します。nearだけに偏らず、farとfrontierをquotaで必ず残すことがポイントです。

### 制約

選択されなかった7つの標準産業は生成対象から外れます。したがって、Full19との比較実験として、落ちた領域と得られた意外性を確認する必要があります。

## 4. Mixed19

### 処理

1. 19 Situationをすべてnear / adjacent / farへ分類し、一つも削除しない。
2. 各SituationのContextごとに、決定論的ローテーションでStakeholderを割り当てる。
3. nearは6件、adjacentは12件、farは30件を生成する。
4. 合計は `6 × N_near + 12 × N_adjacent + 30 × N_far` で決まる。

### 意図

Situationの被覆を維持しつつ、既存用途に近い領域のtuple数を減らします。farほど深く探索するため、「遠いから落とす」というReq②に不適切な足切りを避けます。

### 制約

nearとadjacentでは3軸の全tupleを生成しません。結果の価値評価ではありませんが、探索密度の設計自体が結果へ影響するため、Full19との比較が必要です。

## 5. 比較

| 観点 | Full19 | Coverage12 | Mixed19 |
|---|---|---|---|
| 19産業の保持 | 全件 | 12枝へ選択 | 全件 |
| 3軸全直積 | 全産業 | 選択枝のみ | farのみ |
| 候補数 | 570固定 | 360固定 | 可変 |
| 意外な産業の保証 | 高い | far/frontier quotaで保証 | 全産業保持＋farを深掘り |
| 再現性 | 高い | Situation選択にLLM推論を含む | 距離分類にLLM推論、tuple割当は決定論的 |
| Gemのbatch数 | 19 | 12 | 19 |
| 主な比較目的 | 網羅性の基準 | 産業選択による削減 | tuple密度による削減 |

## 6. AIが推論する箇所

人間・Knowledgeが固定するのは、分類枠、候補数ルール、ID規則、承認済みRun Manifestです。

LLMは主に次を推論・生成します。

- 特許記載から抽象化したCore Capability
- 19 Situationのnear / adjacent / farとその理由
- Coverage12で採用する12枝
- Situation依存のOrganization ArchetypeとRole
- interpretation、technical_bridge、behavior_change
- assumption、evidence_status、duplicate_note

入力にない性能、実証、企業、規制適合性をFACTとして補完してはいけません。不明はUNKNOWN、発散のための仮置きはASSUMPTIONとして残します。

## 7. 人間確認とRun Manifest

発散前にAIは、対象特許の理解、Stakeholder、Situationの距離分類、Context、探索対象、候補数を提示します。人間は `承認`、`修正: ...`、`再提案`、`中止` のいずれかを返します。

承認後に固定するRun Manifestは、実行ID、対象特許、方式、Situation順序、距離、候補数、batch順を記録する実行計画です。Gem自体が永続保存するわけではありません。将来バックエンド化した際には、結果の保存、参照、再実行、部分再開を可能にする管理単位として利用できます。
