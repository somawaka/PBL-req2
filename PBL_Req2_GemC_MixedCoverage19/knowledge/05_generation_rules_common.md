# GemC 共通生成・出力ルール

## 1. 用語階層

`Stakeholder Group > Organization Archetype > Role`

- Stakeholder GroupはS1〜S5の固定分類である。
- Actorという語へ置換しない。
- Organization Archetypeは対象Situationに存在し得る組織類型である。
- Roleはその組織内外で技術に関与する具体的役割である。
- Company名は根拠がある場合だけ使用する。

## 2. ContextとMeaning Lens

- ContextはC1〜C6の発散軸である。
- Meaning LensはContextを意味仮説へ適用するための問いである。
- Meaning Lensを第4軸として掛け合わせない。

## 3. 候補生成

1. 承認済みRun Manifestから現在のSituationとdistanceを読む。
2. `04_mixed_coverage_rules.md`で使用rotationとtupleを確定する。
3. Situationの具体的な現場・業務・状態を1つ設定する。
4. S1〜S5のOrganization ArchetypeとRoleをSituation依存で具体化する。
5. 指定tupleへInterpretationを1件ずつ生成する。
6. Candidate ID、件数、rotation、被覆を検査する。

## 4. Interpretation

次の問いへ答える。

> このStakeholderが、このSituationに置かれ、このContextから見たとき、この特許はどのような意味・価値を持つのか。

単なる用途名や機能便益で終わらず、technical bridgeとStakeholderの判断・行動・関係の変化を含める。

## 5. 保持ルール

- 遠い、不自然、採算不明、実現困難に見えることを理由に削除しない。
- 類似候補を統合しない。`duplicate_note`に類似IDと残すべき差を記録する。
- 市場性、新規性、事業性、技術適合性、実現可能性の評価はReq③で行う。
- 不確実性は`assumption`と`evidence_status`へ残す。

## 6. 候補表のカラムガイド

各batchの候補表直前に、次の表を必ず表示する。

| カラム | 意味 | 設置目的 |
|---|---|---|
| `interpretation` | そのStakeholder・Situation・Contextで特許が持つ意味・価値の仮説 | 発散結果の中心を示す |
| `technical_bridge` | 元の特許能力が新しいSituationで、なぜ・どのように機能し得るか | 単なる連想と技術に基づく転用仮説を区別する |
| `behavior_change` | 導入前後でStakeholderの判断・行動・関係がどう変わるか | 用途ではなく意味的価値になっているかを示す |
| `assumption` | 候補成立に必要だが入力特許では確認できない条件 | 不確実な候補を削除せずReq③で検証可能にする |
| `evidence_status` | technical bridgeの根拠状態。FACT / INFERENCE / ASSUMPTION | 特許記載とAI推論・仮定を混同しない |
| `duplicate_note` | 類似候補のCandidate IDと残すべき相違点。類似なしは`none` | Req②で削除せずReq③の重複整理へ渡す |

## 7. 表形式の必須ルール

- Batch summary、Organization Archetype / Role、カラムガイド、候補一覧、検査結果をすべてMarkdown表で表示する。
- 候補一覧を箇条書きへ変更しない。
- 1候補は表の1行とし、セル内で改行しない。
- セル内の縦棒`|`は`／`へ置換する。
- 表の前後へ長い解説を追加しない。
- 出力上限が近い場合は各セルを簡潔にし、行数・Candidate ID・必須カラムを優先する。

## 8. FACTとAI推論の境界

### 人間・Knowledgeが固定する情報

- Stakeholder S1〜S5
- Situation A〜S
- Context C1〜C6
- distanceごとのrotation数
- tuple割当式
- Candidate ID規則
- 人間が承認したRun Manifest

### AIが入力から抽出・抽象化する情報

- mechanism、problem、claimed effect、existing useの原文抽出はFACT。
- 特許機構を産業横断的な動詞句へ変換したcore capabilityはINFERENCE。
- input / output、conditions、constraintsは、原文明記部分をFACT、抽象化部分をINFERENCEとする。

### AIが発散のために推論・生成する情報

- 19 Situationのnear / adjacent / far分類と理由
- Situation依存のOrganization ArchetypeとRole
- interpretation、technical_bridge、behavior_change
- assumption、evidence_status、duplicate_note

### 禁止する事実補完

- 入力特許にない構造、性能値、実施条件、実証結果、導入企業、規制適合性をFACTとして補わない。
- 空欄を別の公報行や一般常識で埋めない。
- 情報がなければ`UNKNOWN`、発散に必要な仮置きなら`ASSUMPTION`とする。
- AI生成候補を既に存在する用途・市場・事業として表現しない。

