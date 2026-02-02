# SQL*Plus 大量データ出力のパフォーマンスチューニング

## 背景・課題

- SQL*Plusで40万件をクライアントに返してCSV出力する月初作業
- 固定IP制限があり、WARPサービスでIP固定
- 社内LANでは接続不可 → 社用携帯のテザリング利用
- テザリング環境が不安定で、処理途中でネットが切れると処理終了

## 解決策

### 1. 画面出力OFF

```sql
SET TERMOUT OFF
```

画面への出力を抑制し、I/O負荷を軽減。

### 2. フェッチサイズ増加

```sql
SET ARRAYSIZE 5000
```

デフォルト: 15 → 変更後: 5000

## なぜ速くなるか

SELECT で40万件を返す場合、クライアントは内部で以下を繰り返す：

1. DBに「次の結果ください」と要求（fetch）
2. DBが結果を返す
3. それをファイルに書く（spool）
4. また次を要求…

| ARRAYSIZE | fetch往復回数 |
|-----------|---------------|
| 15（デフォルト） | 約26,667回 |
| 5000 | 約80回 |

**ネットワーク遅延が大きい環境（テザリング等）では、往復回数削減の効果が顕著。**

## 参考設定例

```sql
SET TERMOUT OFF
SET ARRAYSIZE 5000
SET PAGESIZE 0
SET LINESIZE 32767
SET TRIMSPOOL ON
SET FEEDBACK OFF

SPOOL output.csv
SELECT ...
SPOOL OFF
```

## 学んだ日
2026-02-02
