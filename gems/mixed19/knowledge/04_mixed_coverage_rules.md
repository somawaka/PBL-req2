# GemC Mixed-Coverage19 割当ルール

## 1. 目的

19のSituationを一つも除外せず、既存用途からの距離に応じてStakeholder × Contextの探索密度を変える。

この処理は意味的価値の評価・選別ではない。生成前に固定した距離分類と数式だけでtupleを決める。

## 2. Distanceと探索密度

| distance | rotations | 1 Situation当たりの候補数 | 被覆 |
|---|---|---:|---|
| near | 0 | 6 | 全5 Stakeholderと全6 Contextを各1回以上含む |
| adjacent | 0, 1 | 12 | 2つの相補的なローテーションを含む |
| far | 0, 1, 2, 3, 4 | 30 | Stakeholder 5 × Context 6の全直積 |

farは優先度が低いという意味ではない。既存用途から遠いため、意外な意味的価値を逃さないよう最も深く探索する。

## 3. 決定論的なtuple割当

0始まり番号を次のように定義する。

- Situation：A=0、B=1、…、S=18
- Context：C1=0、C2=1、…、C6=5
- Stakeholder：S1=1、S2=2、…、S5=5
- Rotation：r=0、1、2、3、4

Stakeholderは次式で決定する。

`stakeholder_index = ((situation_index + context_index + rotation) mod 5) + 1`

例としてSituation Aでは、rotation 0が次となる。

| Context | Stakeholder |
|---|---|
| C1 | S1 |
| C2 | S2 |
| C3 | S3 |
| C4 | S4 |
| C5 | S5 |
| C6 | S1 |

Situation Bでは開始位置が1つ移動し、rotation 0はC1→S2から始まる。この移動により、全Situationを通してStakeholder × Contextの偏りを抑える。

## 4. 被覆特性

rotation 0だけで19 × 6 = 114候補となり、次を満たす。

- Situation × Contextの全114ペアを含む。
- Situation × Stakeholderの全95ペアを含む。
- Stakeholder × Contextの全30ペアを含む。

ただし、nearとadjacentでは全ての3軸tupleを含まない。farだけが3軸全直積となる。

## 5. 候補数

`N_near + N_adjacent + N_far = 19`

合計候補数は次で計算する。

`expected_total = 6 × N_near + 12 × N_adjacent + 30 × N_far`

例：near 5、adjacent 6、far 8の場合は342候補となる。

## 6. Candidate ID

`{PatentID}-{SituationID}-{StakeholderID}-{ContextID}`

同一Situation・Stakeholder・Contextのtupleは一度しか現れないため、Candidate IDへrotationを含めない。出力には監査用として`coverage_rotation`を残す。

## 7. 禁止事項

- LLMが関連性、実現性、価値、新規性を見てtupleを選ぶ。
- nearのSituation自体を削除する。
- farを「実現性が低い」として浅く探索する。
- 生成後のInterpretationを見て候補を削除する。
- 重複候補をReq②で統合する。

## 8. 将来の段階的全直積

全Situationをrotation 0だけで実行すると114候補となる。rotation 1〜4を順次追加すれば、各回114候補ずつ、5回の和集合で570tupleの全直積へ到達できる。

GemCの標準Modeではdistance別にrotation数を変える。バックエンド実装時は、保存済みRun Manifestへ未実行rotationを追加することで、後から全直積へ拡張できる。

