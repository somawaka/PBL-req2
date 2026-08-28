# 2種類のGem 共通生成ルール

## 1. Modeで変えるもの

- FULL19：19 JSIC Situationをすべてbranchとして使う。
- COVERAGE12：19 Situationを距離分類し、near 3 / adjacent 3 / far 4 / frontier 2の12branchを使う。

Mode間で変えるのはSituation branchの構成だけである。

## 2. Mode間で変えないもの

- Stakeholder S1〜S5。
- Context C1〜C6。
- 1branch当たりの全直積：5 Stakeholder × 6 Context = 30候補。
- Candidate出力項目。
- 承認前に発散しない対話手順。
- 候補を削除・統合・採点しないルール。

## 3. 用語階層

`Stakeholder Group > Organization Archetype > Role`

- Actorという語へ置換しない。
- Company名は根拠がある場合だけ使用し、通常はOrganization Archetypeで書く。
- Roleは当該SituationとStakeholder Groupに依存して具体化する。

## 4. ContextとMeaning Lens

- Contextは発散軸のカテゴリ値である。
- Meaning Lensは各Contextを意味仮説へ適用するための質問文である。
- Meaning Lensを第4軸として掛け合わせない。

## 5. 候補生成

承認済みRun Manifestのbranchを順番に処理する。

1. branchの具体的な現場・業務・状態を定める。
2. S1〜S5のOrganization ArchetypeとRoleをSituation依存で具体化する。
3. 5 Stakeholder × 6 Contextの30tupleを作る。
4. 30tupleすべてへInterpretationを1件ずつ生成する。
5. Candidate ID集合と30件を検査する。

## 6. Interpretation

次の問いへ答える。

> このStakeholderが、このSituationに置かれ、このContextから見たとき、この特許はどのような意味・価値を持つのか。

単なる用途名や機能便益で終わらず、技術能力からのtechnical bridgeと、Stakeholderの判断・行動・関係の変化を含める。

## 7. 保持ルール

- 遠い、不自然、採算不明、実現困難に見えることを理由に削除しない。
- 類似候補を統合しない。`duplicate_note`に記録して保持する。
- 市場性・新規性・事業性・技術適合性・実現可能性の採点は要求機能③で行う。
- 不確実な仮説は`assumption`と`evidence_status`に残す。

## 8. 出力項目

- candidate_id
- stakeholder_id / stakeholder_name
- situation_id / situation_name / situation_detail
- overlay_id / overlay_name（frontier以外は空欄）
- context_id / context_name
- organization_archetype
- role
- interpretation
- technical_bridge
- behavior_change
- assumption
- evidence_status
- duplicate_note
