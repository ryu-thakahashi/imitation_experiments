# 要件定義書：成功者模倣実験

---

## 1. 実験概要

**目的**

* 人々は「成功者模倣」を行うのかを検証する。

  * 成功者模倣：近傍ノードの利得情報を参照し、最も利得の高いノードの行動を真似する行動パターン。

**仮説**

* 近傍の利得情報を制限しても、参加者の模倣行動には変化が生じない。

---

## 2. 参加者 & グループ設定

| 項目       | 内容                |
| -------- | ----------------- |
| 参加者数     | 約1000名            |
| グループサイズ  | 20名／グループ          |
| ネットワーク構造 | サークル型ネットワーク (k=4) |

* **補足**：20名が輪状につながり、各ノードは左右2名ずつ、計4名と直接接続。

---

## 3. 実験フロー

1. **ラウンド数**

   * 全15ラウンド実施

2. **条件設定**

   * 2条件の between‐subjects

     1. 利得提示群：近傍ノードの利得を数字で表示
     2. 利得非提示群：近傍ノードの利得を隠蔽

3. **ラウンド毎の手順**

   4. 意思決定ページ（ボタン選択）
   5. ResultsWaitPage：他ノードの入力待ち
   6. 結果フィードバックページ

---

## 4. UI／入力形式

* **意思決定**

  * 選択肢：ボタン形式（例：「A行動」「B行動」など）
* **フィードバック表示**

  * 自分と近傍ノードの関係図
  * ノードの色分け：近傍の行動（色）
  * 近傍ノードの利得（数字）

---

## 5. フィードバックのタイミング & 内容

| 表示タイミング  | 表示内容                                                         |
| -------- | ------------------------------------------------------------ |
| 各ラウンド終了後 | 1. 参加者自身と近傍ノードのつながりを可視化<br>2. 近傍ノードの行動（色）<br>3. 近傍ノードの利得（数字） |

* **ネットワーク図**

  * ノード（丸）＋エッジ（線）で構築
  * カラーで行動、吹き出し or 数字ラベルで利得を表示

---

## 6. 報酬構造

* 特に指定なし（ポイント制 or 固定報酬は後日調整可能）

---

## 7. 動作環境

* **プラットフォーム**：Webブラウザ（PC前提）
* **対応ブラウザ**：Chrome、Firefox、Edge などモダンブラウザ

---

## 8. oTree 実装イメージ

### models.py

```python
class Constants(BaseConstants):
    NAME_IN_URL = 'imitator_experiment'
    PLAYERS_PER_GROUP = 20
    NUM_ROUNDS = 15
    K = 4  # サークル型ケネクト数

class Player(BasePlayer):
    choice = models.StringField(choices=['A','B'], widget=widgets.RadioSelect)
    payoff = models.CurrencyField()
```

### pages.py

```python
class DecisionPage(Page):
    form_model = 'player'
    form_fields = ['choice']

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs_and_info'

class ResultsPage(Page):
    def vars_for_template(self):
        return {
            'neighbors': self.group.get_neighbors(self.player),
            'show_payoff': self.group.condition == '提示群',
        }
```

