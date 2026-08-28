# Req② Knowledge：生成規則 v1.0

## 1. 基本原則

このKnowledgeは、特許から新しいBtoB文脈・意味的価値の「候補幹」を発散するために使う。`Stakeholder × Situation × Context` の全直積は行わない。

- Situationは探索空間の被覆アンカーである。
- Stakeholderは固定された企業名やRole一覧ではなく、5つのActor Function群である。
- Meaning Lensは独立した第3軸ではなく、SituationとActorの関係ができた後に適用する意味変化の問いである。
- Req②では事業性・実現性で候補を落とさない。評価・Role詳細化・事業モデル化は原則Req③へ渡す。
- 事実、入力からの推論、未検証仮説を混ぜない。

## 2. 入力契約：Capability Card

入力が特許公報全文でも短い紹介文でも、最初に次のカードへ正規化する。情報がない欄は `UNKNOWN` とし、埋め合わせて事実化しない。

| field | 内容 |
|---|---|
| patent_or_seed_id | 特許番号、OTBシーズ名、管理ID |
| title | 技術名 |
| mechanism | 物理・情報・制御上の仕組み |
| capability | その仕組みが「何を可能にするか」 |
| input_output | 入力、処理、出力 |
| conditions | 成立条件、必要設備、対象物、接触/非接触、環境条件 |
| constraints | 適用限界、測定・材料・安全・規制・精度等 |
| existing_situations | 既に明示された用途・産業・主体 |
| evidence | 入力に明記された事実と出典 |
| unknowns | 不明事項 |

`capability` は製品名ではなく、産業間で転用できる動詞句で書く。例：「USB機器を識別する」だけでなく、「製造ばらつき由来の複製困難な物理特性を測定し、追加識別回路なしで個体を照合する」。

## 3. 探索モードと候補数

| mode | Situation枝 | 1枝あたり候補 | 最終候補数 | 用途 |
|---|---:|---:|---:|---|
| quick | 12 | 1 | 12 | 挙動確認、短時間試験 |
| standard | 12 | 2 | 24 | 既定。発散とGem実装負荷の均衡 |
| wide | 12 | 3 | 36 | 重要シーズの広域探索 |

最終候補数は重複統合後の数である。統合で不足した場合、被覆不足のdistance bucket、stakeholder group、lens familyから再生成して補充する。

## 4. Situation枝の選択

### 4.1 standardの固定割当

12枝を次の比率で選ぶ。

- `near`: 3枝。同一または非常に近い産業・業務構造。
- `adjacent`: 3枝。産業は異なるが、タスク、制約、資産、検証方法のいずれかが近い。
- `far`: 4枝。産業・顧客・価値論理が明確に異なる。常識的な市場規模や相性だけで落とさない。
- `frontier`: 2枝。FRONTIER_OVERLAYを起点に、対応するJSICアンカーも併記する横断領域。

quickとwideでも枝数と割当は同じ。1枝あたり候補数だけを変える。

### 4.2 選択規則

1. `02_situation_framework.csv` のJSIC A〜S（T「分類不能」は使わない）を一度走査する。
2. 特許能力との距離を、既存用途ではなく次の4要素で暫定判定する：対象物、業務、制約、価値論理。
3. far枝は同じ大分類に偏らせず、原則4つの異なるJSIC大分類から選ぶ。
4. frontier枝は2つの異なるoverlayから選び、それぞれ関連JSICを付ける。
5. 産業名だけで終えず、「どの現場で、いつ、何が起きているか」を1文で具体化する。
6. 遠いが技術的橋渡しを1文で説明できない枝は、空想として採用せず別の遠距離枝に置換する。

## 5. Situation依存のActor生成

Situation枝ごとに `03_stakeholder_framework.csv` の5群を参照し、その現場に実在し得る組織類型を生成する。

- `stakeholder_group_id` は固定分類。
- `organization_archetype` はAIが生成する組織の類型。例：病院運営法人、漁業協同組合、認定修理事業者。
- `company_name` は出典のある事実でない限り生成しない。
- `role` はReq②の全候補では展開しない。技術価値の理解に不可欠な場合だけ `role_hint` を1つ付け、詳細化はReq③へ送る。
- 同じ組織が複数機能を持つ場合、候補の主たる機能を `primary_actor_function`、影響を受ける相手を `counterparty_or_affected_actor` とする。

standardの24候補全体で、S1〜S5をprimaryとして各3件以上含め、1群が8件を超えないようにする。ただし技術的に不自然な割当は禁止し、不足理由をcoverage auditに記す。

## 6. Meaning Lensの条件適用

SituationとActorの緊張・未充足ジョブを先に記述し、その後で `04_meaning_lens_framework.csv` から適合するLensを選ぶ。

- Lensを先に選んで候補を捏造しない。
- 同一Situation枝の2候補は、原則として異なるfamilyを使う。
- standard全体で4 familyを各4件以上、12 Lens中8 Lens以上を使用する。
- 同一Lensは4件を超えない。
- 意味仮説は `From: 現在の意味/状態 → To: 新しい意味/状態` で書く。
- 「効率化」「コスト削減」「安全性向上」だけを意味的価値としない。それによって誰の判断、関係、正当性、アイデンティティがどう変わるかまで書く。

## 7. 反常識枠（wildcard）

standardでは24件中4件以上を `wildcard=true` とする。少なくともfarから2件、frontierから1件を含める。次のいずれかを明示的に使う。

- 価値受領者を、買い手ではなく保守者・監査者・地域・下流事業者へ反転する。
- 技術の制約を欠点でなく、証拠、儀式、責任分界、希少性として読み替える。
- 平常時でなく、異常、引渡し、廃棄、再販、制度変更の瞬間へ置く。
- 製品機能でなく、組織間の信頼、権限、記憶、正当性を変える。

wildcardであっても、technical_bridgeと検証すべき前提を必ず記す。

## 8. 候補生成テンプレート

候補1件につき次を満たす。

1. Situation：産業＋具体現場＋業務状態。
2. Actor：誰が主に価値を認識し、誰との関係が変わるか。
3. Tension：現在の未充足、摩擦、曖昧さ。
4. Technical bridge：Capabilityがその状況で働く因果的な橋。
5. Meaning shift：From→To。
6. Behavior change：導入後に誰が何を違って行うか。
7. Evidence boundary：FACT / INFERENCE / ASSUMPTION。
8. Req③ unknowns：技術適合、規制、データ、導入主体、支払意思など後で検証する点。

## 9. 重複処理

### 9.1 構造キー

次の4要素を正規化した `cluster_key` を作る。

`situation_mechanism | primary_actor_function | meaning_shift_to | behavior_change`

産業名だけが違っても、この4要素が同じなら意味重複の可能性が高い。逆に同じ産業でもActor、意味変化、行動変化が異なれば別候補とする。

### 9.2 統合規則

- 重複候補は黙って削除しない。強い表現へ統合し、`merged_candidate_ids` に元IDを残す。
- 既存用途の単なる言い換えは `existing_use_restatement=true` とし、新規候補数へ数えない。
- 候補数不足は、最も被覆不足のbucket/group/familyから再生成する。

## 10. 出力スキーマ

最初にCapability CardとCoverage AuditをMarkdownで示し、その後に次の列順でCSVコードブロックを出す。

1. `candidate_id`
2. `situation_anchor_id`
3. `situation_anchor_name`
4. `situation_detail`
5. `distance_bucket`
6. `frontier_overlay_id`
7. `primary_actor_function`
8. `organization_archetype`
9. `counterparty_or_affected_actor`
10. `meaning_lens_id`
11. `meaning_lens_name`
12. `tension_or_trigger`
13. `technical_bridge`
14. `reinterpretation`
15. `semantic_value_hypothesis`
16. `behavior_change`
17. `wildcard`
18. `evidence_status`
19. `fact_basis`
20. `assumptions`
21. `unknowns_for_req3`
22. `cluster_key`
23. `merged_candidate_ids`

`evidence_status` は次から選ぶ。

- `FACT`: 入力または明示された出典に直接書かれている。
- `INFERENCE`: 事実から論理的に導いたが、利用実績として確認されていない。
- `ASSUMPTION`: 技術適用条件・主体・制度など未確認の前提を含む。

## 11. Coverage Audit

出力前に内部監査し、出力冒頭に次を報告する。

- final_candidate_count
- distance counts: near / adjacent / far / frontier
- stakeholder primary counts: S1〜S5
- lens family counts: F1〜F4
- unique lens count
- wildcard count
- duplicates merged count
- existing-use restatements excluded count
- unmet constraints and reasons

制約未達でも候補を水増ししない。未達理由を明示する。

## 12. Req③への境界

Req②で行う：状況、組織類型、意味仮説、行動変化、技術橋渡し、前提、未検証点の生成。

Req③へ送る：具体的Roleの詳細化、企業固有性、顧客数・市場規模、競合、収益モデル、導入費、法規適合、TRL、実証計画、新規性・有用性・事業性・技術適合性・意外性の採点。

