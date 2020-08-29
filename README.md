fepl
====

基本情報の疑似言語のマークアップ

## インストール

```sh
python3 -m pip install git+https://github.com/tos-kamiya/fepl
```

## 実行

```sh
fepl 入力ファイル
```

### 実行例

```sh
$ cat sampleinput.txt
D 手続き： fibo(n)
/ この手続きは引数として、1から始まる整数で、フィボナッチ数の何番目の数字を出力するかを受け取ります。
A n <= 2
 - print(1)
+
 - a <- 1
 - b <- 1
 T n > 2
  - c <- a /ADD b
  - a <- b
  - b <- c
  - n <- n /SUB 1
 L
 - print(c)
V
$ fepl sampleinput.txt
◯ 手続き： fibo(n)
/* この手続きは引数として、1から始まる整数で、フィボナッチ数の何番目の数字を
   出力するかを受け取ります。 */
▲ n ≦ 2
│ ・ print(1)
┼────────────────────────────────────────────────────────────────────────────
│ ・ a ← 1
│ ・ b ← 1
│ █ n ＞ 2
│ │ ・ c ← a ＋ b
│ │ ・ a ← b
│ │ ・ b ← c
│ │ ・ n ← n ー 1
│ █
│ ・ print(c)
▼
```

## 文法

それぞれの行の行頭に、制御構造を表す次の文字のいずれかを置きます。
ただし、これらの前にスペースを複数置いてインデントすることができます。

```
D   宣言
-   文
/   コメント
A   分岐文の開始
+   分岐の真の場合と偽の場合の分かれ目
V   分岐文の終了
T   ループ文の開始
L   ループ文の終了
```

行頭以外の場所に、次のいずれかの文字列を置くと置換されます。

```
<-  ←
<   ＜
<=  ≦
>   ＞
>=  ≧
!=  ≠
=   ＝
/MOD  ％
/ADD  ＋
/SUB  ー
/DIV  ÷
/MUL  ✕
```

## 入力サンプル

ディレクトリ`test`にある、`input1.txt`〜`input4.txt`を参照してください。

## ライセンス

Public Domain/Unlicense

## requirements.txtを取り出す

```sh
sed -e '1,/install_requires =/ d' < setup.cfg
```
