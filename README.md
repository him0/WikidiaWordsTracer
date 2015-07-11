# WikidiaWordsTracer

Wikipediaの任意のワードから任意のワードへリンクのみをたどって辿り着く経路を導き出します。

ダイクストラのアルゴリズムを応用した何かを作れという課題のために作成しました。

任意のワードから任意のワードまでの距離は（Wikipediaのリンクの出現順 + 1）となっています。

実行環境
---

Python 3.4.3

環境構築
---

```
pip install -r requirements.txt
```

使い方
---

```
python main.py
```
