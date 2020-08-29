import os
import sys

import wcwidth
import docopt


class FeplSyntaxError(ValueError):
    pass


_script_dir = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
with open(os.path.join(_script_dir, 'VERSION.txt')) as _inp:
    __version__ = _inp.readline().rstrip()


FE_PSEUDO_LANG_NOTATION = """
[Control structure (fist char of line)]
D   declaration
-   some statement
/   comment
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
    vbar = '│'
    hc_expand = {'D': '◯', '-': '・', 'A': '▲', 'V': '▼', '+': '┼', 'T': '█', 'L': '█', '/': '/*'}
    hc_expand2 = {'D': '　', '-': '　', 'A': '│', 'V': '　', '+': '　', 'T': '│', 'L': '　', '/': '  '}
    bc_expand = {'/MOD': '％', '/ADD': '＋', '/SUB': 'ー', '/DIV': '÷', '/MUL': '✕',
            '<-': '←', '<=': '≦', '>=': '≧', '!=': '≠',
            '<': '＜', '>': '＞', '=': '＝'}
    bc_keys = list(bc_expand.keys())
    bc_keys.sort(key=len, reverse=True)

    stack = []
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
        ls = L.lstrip()
        if not ls:
            h = b = ''
        else:
            h, b = ls[0], ls[1:].lstrip()

        # make picture of header
        if h == '':
            if b != '':
                raise FeplSyntaxError("line %d: expected one of chars `-+/ADLTV`" % line_number)
            fh = sh = ' '.join([vbar] * len(stack))
        elif h in ('L', 'V'):
            if h == 'V':
                if not stack:
                    raise FeplSyntaxError("line %d: no corresponding `A` found for `V` at line %d" % (line_number, line_number))
                if stack[-1][0] != 'A':
                    mark, atline = stack[-1]
                    raise FeplSyntaxError("line %d: no closing `%s` at line %d" % (line_number, mark, atline))
                stack.pop()
            elif h == 'L':
                if not stack:
                    raise FeplSyntaxError("line %d: no corresponding `T` found for `L` at line %d" % (line_number, line_number))
                if stack[-1][0] != 'T':
                    mark, atline = stack[-1]
                    raise FeplSyntaxError("line %d: no closing `%s` at line %d" % (line_number, mark, atline))
                stack.pop()
            fh = ' '.join([vbar] * len(stack) + [hc_expand[h]])
            sh = ' '.join([vbar] * len(stack) + [hc_expand2[h]])
        elif h == '+':
            if not stack:
                raise FeplSyntaxError("line %d: no corresponding `A` found for `V` at line %d" % (line_number, line_number))
            if stack[-1][0] != 'A':
                mark, atline = stack[-1]
                raise FeplSyntaxError("line %d: no closing `%s` at line %d" % (line_number, mark, atline))
            fh = ' '.join([vbar] * (len(stack) - 1) + [hc_expand[h]])
            sh = ' '.join([vbar] * (len(stack) - 1) + [hc_expand2[h]])
            bw = wcwidth.wcswidth('─')
            curlen = wcwidth.wcswidth(fh) + wcwidth.wcswidth(b)
            while curlen + bw < line_width:
                fh += '─'
                curlen += bw
        else:
            if h not in hc_expand:
                raise FeplSyntaxError("line %d: invalid char" % line_number)
            fh = ' '.join([vbar] * len(stack) + [hc_expand[h]])
            sh = ' '.join([vbar] * len(stack) + [hc_expand2[h]])
            if h in ('A', 'T'):
                stack.append((h, line_number))
            elif h == '/':
                b += ' */'
        
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

    if stack:
        mark, atline = stack[-1]
        raise FeplSyntaxError("line EOF: no closing `%s` at line %d" % (mark, atline))


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
