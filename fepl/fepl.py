import os
import sys

import docopt

try:
    from . import do_process_fe_pseudo_lang
except:
    from fepl_core import do_process_fe_pseudo_lang


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
    
    do_process_fe_pseudo_lang(outp, inp, line_width)

    if input_file is not None:
        inp.close()
    if output_file is not None:
        outp.close()


if __name__ == '__main__':
    main()
