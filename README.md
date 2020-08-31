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
$ cat sample-input.txt
D 整数型関数: fibo(整数型: n)
D 整数型: t, u, v

A n <= 2 /;<|- α
  - return (1)
+
  - t <- 1
  - u <- 1
  T /[    a    /]
    - v <- t /ADD u
    - t <- u
    - u <- v
    - n <- n /SUB 1
   L
   - return (v)
V

$ fepl sample-input.txt
◯ 整数型関数: fibo(整数型: n)
◯ 整数型: t, u, v

▲ n ≦ 2                                                                    ⬅ α
│ ・ return (1)
┼────────────────────────────────────────────────────────────────────────────
│ ・ t ← 1
│ ・ u ← 1
│ █ [ ̲̅ ̲̅ ̲̅ ̲̅a ̲̅ ̲̅ ̲̅ ̲̅]
│ │ ・ v ← t ＋ u
│ │ ・ t ← u
│ │ ・ u ← v
│ │ ・ n ← n ー 1
│ █
│ ・ return (v)
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
/[テキスト/]    解答欄
/;<|-          (右寄せ)⬅
```

## 入力サンプル

`sample-input.txt`、および、ディレクトリ`test`にある`input*.txt`を参照してください。

## ライセンス

Public Domain/Unlicense

## requirements.txtを取り出す

```sh
sed -e '1,/install_requires =/ d' < setup.cfg
```
