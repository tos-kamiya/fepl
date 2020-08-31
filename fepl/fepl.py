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
[Control structure] line starts either of the following chars after some space chars:
D   declaration
-   some statement
/   comment
A   begin of branch statement
+   separator of true/false branch (i.e. `else`)
V   end of branch statement
T   begin of loop statement
L   end of loop statement

[Special symbols] the following patterns will be replaced.
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
/[<sometext>/]     wrte-in box. 
/;<|-              (right-aligned) ⬅
"""[1:]


FE_PSEUDO_EXAMPLE = """
[Input example]
D integer-returning-function: fibo(integer: n)
D integer: t, u, v
A n <= 2
  - return (1)
+
  - t <- 1
  - u <- 1
  T n > 2
    - v <- t /ADD u
    - t <- u
    - u <- v
    - n <- /[a/]
  L
  - return (v)
V
"""


def do_process_fe_pseudo_lang(outp, inp, line_width, input_file=None):
    vbar = '│'
    hc_expand = {'D': '◯', '-': '・', 'A': '▲', 'V': '▼', '+': '┼', 'T': '█', 'L': '█', '/': '/*'}
    hc_expand2 = {'D': '　', '-': '　', 'A': '│', 'V': '　', '+': '　', 'T': '│', 'L': '　', '/': '  '}
    bc_expand = {'/MOD': '％', '/ADD': '＋', '/SUB': 'ー', '/DIV': '÷', '/MUL': '✕',
            '<-': '←', '<=': '≦', '>=': '≧', '!=': '≠', '<': '＜', '>': '＞', '=': '＝', '<|-': '⬅'}
    bc_writein_box = ('/[', '/]')
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
            # special symbols
            for bc in bc_keys:
                if b.find(bc) >= 0:
                    b = b.replace(bc, bc_expand[bc])

            # write-in box
            i = 0
            while True:
                i = b.find(bc_writein_box[0])
                j = b.find(bc_writein_box[1], i + 1)
                if i >= 0:
                    if j < 0:
                        raise FeplSyntaxError("line %d: unmatching /[.../]" % line_number)
                    enclosed_text = b[i + len(bc_writein_box[0]):j]
                    b = b[:i] + '\u0332\u0305'.join('[' + enclosed_text + ']') + b[j + len(bc_writein_box[1]):]
                    i = j + 1
                else:
                    if j >= 0:
                        raise FeplSyntaxError("line %d: unmatching /[.../]" % line_number)
                    break  # while True
            
            # right alignment
            i = b.find('/;')
            if i >= 0:
                b, t = b[:i], b[i + len('/;'):]
            else:
                t = ''
            r = fh + ' '

            while b:
                while b and wcwidth.wcswidth(r + b[0]) < line_width:
                    r = r + b[0]
                    b = b[1:]
                if t:
                    w = wcwidth.wcswidth(r + t)
                    if w < line_width:
                        r += ' ' * (line_width - w)
                    r += t
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
