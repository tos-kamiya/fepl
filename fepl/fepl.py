import re
import os
import sys

import wcwidth
import docopt


_script_dir = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
with open(os.path.join(_script_dir, 'VERSION.txt')) as _inp:
    __version__ = _inp.readline().rstrip()


FE_PSEUDO_LANG_NOTATION = """
[Control structure (head of line)]
D   declaration
-   some statement
/   comment
    indent (space char)
A   begin of branch statement
+   separator of true/false branch (i.e. `else`)
V   end of branch statement
T   begin of loop statement
L   end of loop statement

[Operators (anywhere)]
<-  ←
<   ＜
<=  ≦
>   ＞
>=  ≧
!=  ≠
=   ＝
/MOD   ％
/ADD  ＋
/SUB  ー
/DIV  ÷
/MUL  ✕
"""[1:]


FE_PSEUDO_EXAMPLE = """
[Example]
D 手続き： fibo（n）
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
"""


def do_process_fe_pseudo_lang(outp, inp, line_width, input_file=None):
    hc_expand = {'D': '◯', '-': '・', 'A': '▲', 'V': '▼', 'T': '█', 'L': '█', ' ': '│'}
    hc_expand2 = {'D': '　', '-': '　', 'A': '│', 'V': '　', 'T': '│', 'L': '　', ' ': '│'}
    bc_expand = {'/MOD': '％', '/ADD': '＋', '/SUB': 'ー', '/DIV': '÷', '/MUL': '✕',
            '<-': '←', '<=': '≦', '>=': '≧', '!=': '≠',
            '<': '＜', '>': '＞', '=': '＝' }
    bc_keys = list(bc_expand.keys())
    bc_keys.sort(key=len, reverse=True)

    empty_lines = 0
    for li, L in enumerate(inp):
        line_number = li + 1
        L = L.rstrip()

        if not L:
            empty_lines += 1
            continue  # for li, L
        if empty_lines > 0:
            print('\n'.join([''] * empty_lines), file=outp)
            empty_lines = 0

        # split line into head and body
        m = re.match(r'( *[-D/+AVTL]|)(.*)', L)
        if not m:
            raise ValueError("line %d: invalid syntax" % line_number)

        h, b = m.group(1), m.group(2)
        h = h.rstrip()
        b = b.lstrip()

        # make picture of header
        fsth = []
        sndh = []
        for hci, hc in enumerate(h):
            if hc == '/':
                fsth.append('/*')
                sndh.append('  ')
                b = h[hci+1:] + b + ' */'
            elif hc == '+':
                fsth.append('┼')
                sndh.append('　')
                assert b == ''
                curlen = wcwidth.wcswidth(' '.join(fsth))
                while curlen + wcwidth.wcswidth(b + '─') < line_width:
                    b = b + '─'
                fsth[-1] = fsth[-1] + b
                b = ''
            else:
                fsth.append(hc_expand[hc])
                sndh.append(hc_expand2[hc])

        fh = ' '.join(fsth)
        sh = ' '.join(sndh)

        # format and print header and body
        if not b:
            print(fh, file=outp)
        else:
            for bc in bc_keys:
                if b.find(bc) >= 0:
                    b = b.replace(bc, bc_expand[bc])
            r = fh + ' '
            while b:
                while b and wcwidth.wcswidth(r + b[0]) < line_width:
                    r = r + b[0]
                    b = b[1:]
                print(r, file=outp)
                r = sh + ' '


def do_show_notation():
    print(FE_PSEUDO_LANG_NOTATION)
    print(FE_PSEUDO_EXAMPLE)


__doc__ = """Processor for FE-test's pseudo code.

Usage:
  {argv0} --show-notation
  {argv0} [<input>] [-o OUTPUT] [-w WIDTH]

Options:
  -o OUTPUT     Output.
  -w WIDTH      Line width [default: 78]
  --show-notation
""".format(argv0=os.path.split(__file__)[1])


def main():
    args = docopt.docopt(__doc__, version=__version__)
    if args['--show-notation']:
        do_show_notation()
        return

    input_file = args['<input>']
    output_file = args['-o']
    line_width = int(args['-w'])

    inp = open(input_file, 'r') if input_file is not None else sys.stdin
    outp = open(output_file, 'w') if output_file is not None else sys.stdout
    
    do_process_fe_pseudo_lang(outp, inp, line_width, input_file=input_file)

    if input_file is not None:
        inp.close()
    if output_file is not None:
        outp.close()


if __name__ == '__main__':
    main()