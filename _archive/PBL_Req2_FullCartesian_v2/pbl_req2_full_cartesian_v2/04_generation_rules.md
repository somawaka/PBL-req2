# 要求機能② 生成ルール v2

## 1. 絶対条件

1. `Stakeholder × Situation × Context` の全直積を生成する。
2. 既定軸は Stakeholder 5、Situation 19、Context 6であり、候補幹は必ず570件とする。
3. LLMに組合せの選択・削除・統合をさせない。直積とCandidate IDの採番はプログラムで行う。
4. 技術から遠い、不自然、実現性が低そうという理由で候補を除外しない。
5. 重複は削除せず、`duplicate_note` に類似候補IDまたは類似理由を記録する。評価・統合は要求機能③で行う。

## 2. 用語階層

`Stakeholder Group > Organization Archetype > Role`

- Stakeholder Group：人間が固定する5分類。
- Organization Archetype：SituationごとにAIが具体化する組織類型。実在企業名ではない。
- Role：その組織内外で技術に関わる役割。必要な範囲でAIが具体化する。
- Actorという語はStakeholderとの混同を避けるため使用しない。

## 3. ContextとMeaning Lens

- Contextは全直積を構成する第3軸である。
- Meaning Lensは独立軸ではなく、各Contextを候補解釈へ適用するための質問文（`lens_prompt`）である。
- したがって、ContextとMeaning Lensを掛け合わせない。両者は1対1の「カテゴリと操作質問」の関係である。

## 4. 処理単位

19 Situationをすべて順番に処理する。Situationごとに次を実行する。

1. 5 Stakeholder Groupそれぞれについて、そのSituationに存在し得るOrganization ArchetypeとRoleを具体化する。
2. プログラムが5 Stakeholder × 6 Contextの30セルを提示する。
3. LLMは30セルすべてにInterpretationを1件ずつ付与する。
4. 出力件数30、Candidate ID集合一致、必須列欠損0を検査する。
5. 19 Situationの出力を結合し、570件であることを検査する。

あるStakeholderが通常は弱いSituationでも空欄にしない。最も近い主体を具体化し、`assumption` に成立条件を書く。

## 5. Interpretationの要件

Interpretationは次の問いへ一文または二文で答える。

> このStakeholderが、このSituationに置かれ、このContextから見たとき、この特許はどのような意味・価値を持つのか。

各候補は次を含む。

- `situation_detail`：具体的な現場・業務・状態。
- `organization_archetype`：企業名でない組織類型。
- `role`：技術に関わる役割。
- `interpretation`：意味・価値の自然言語表現。
- `technical_bridge`：特許能力と候補文脈をつなぐ説明。
- `behavior_change`：誰の判断・行動・関係がどう変わるか。
- `assumption`：成立に必要だが未確認の条件。
- `evidence_status`：`FACT` / `INFERENCE` / `ASSUMPTION`。
- `duplicate_note`：類似が疑われる候補。削除はしない。

## 6. 禁止事項

- 出力しやすい組合せだけを選ぶ。
- 近接産業だけを残す。
- ContextをAI判断で選択する。
- 同じ意味に見える候補をReq②で削る。
- 市場性・事業性・新規性・実現可能性の点数で足切りする。
- Company、Organization、Roleを同じ列へ混在させる。
- 根拠なく実在企業名・制度名・市場規模を断定する。

## 7. 要求機能③への受け渡し

570件を保持したまま、要求機能③で新規性・有用性・事業性・技術適合性・意外性・重複性を評価する。Req②で付ける`technical_bridge`や`assumption`は評価点ではなく、Req③で検証すべき根拠と未確定事項である。
