import wcwidth


class FeplSyntaxError(ValueError):
    pass


_vbar = '│'
_hc_expand = {'D': '◯', '-': '・', 'A': '▲', 'V': '▼', '+': '┼', 'T': '█', 'L': '█', '/': '/*'}
_hc_expand2 = {'D': '　', '-': '　', 'A': '│', 'V': '　', '+': '　', 'T': '│', 'L': '　', '/': '  '}


def parse_struct_iter(inp, line_width):
    stack = []
    for li, L in enumerate(inp):
        line_number = li + 1
        L = L.rstrip()

        if not L:
            continue  # for li, L

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
            fh = sh = ' '.join([_vbar] * len(stack))
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
            fh = ' '.join([_vbar] * len(stack) + [_hc_expand[h]])
            sh = ' '.join([_vbar] * len(stack) + [_hc_expand2[h]])
        elif h == '+':
            if not stack:
                raise FeplSyntaxError("line %d: no corresponding `A` found for `V` at line %d" % (line_number, line_number))
            if stack[-1][0] != 'A':
                mark, atline = stack[-1]
                raise FeplSyntaxError("line %d: no closing `%s` at line %d" % (line_number, mark, atline))
            fh = ' '.join([_vbar] * (len(stack) - 1) + [_hc_expand[h]])
            sh = ' '.join([_vbar] * (len(stack) - 1) + [_hc_expand2[h]])
            bw = wcwidth.wcswidth('─')
            curlen = wcwidth.wcswidth(fh) + wcwidth.wcswidth(b)
            while curlen + bw < line_width:
                fh += '─'
                curlen += bw
        else:
            if h not in _hc_expand:
                raise FeplSyntaxError("line %d: invalid char: 0x%s" % (line_number, hex(ord(h))))
            fh = ' '.join([_vbar] * len(stack) + [_hc_expand[h]])
            sh = ' '.join([_vbar] * len(stack) + [_hc_expand2[h]])
            if h in ('A', 'T'):
                stack.append((h, line_number))
            elif h == '/':
                b += ' */'

        yield li, fh, sh, b

    if stack:
        mark, atline = stack[-1]
        raise FeplSyntaxError("line EOF: no closing `%s` at line %d" % (mark, atline))


_bc_expand = {'/MOD': '％', '/ADD': '＋', '/SUB': 'ー', '/DIV': '÷', '/MUL': '✕',
        '<-': '←', '<=': '≦', '>=': '≧', '!=': '≠', '<': '＜', '>': '＞', '=': '＝', '<|-': '⬅'}
_bc_writein_box = ('/[', '/]')
_bc_keys = list(_bc_expand.keys())
_bc_keys.sort(key=len, reverse=True)


def expand_special_symbols(li, b):
    line_number = li + 1

    # symbols
    for bc in _bc_keys:
        if b.find(bc) >= 0:
            b = b.replace(bc, _bc_expand[bc])

    # write-in box
    i = 0
    while True:
        i = b.find(_bc_writein_box[0])
        j = b.find(_bc_writein_box[1], i + 1)
        if i >= 0:
            if j < 0:
                raise FeplSyntaxError("line %d: unmatching /[.../]" % line_number)
            enclosed_text = b[i + len(_bc_writein_box[0]):j]
            b = b[:i] + '\u0332\u0305'.join('[' + enclosed_text + ']') + b[j + len(_bc_writein_box[1]):]
            i = j + 1
        else:
            if j >= 0:
                raise FeplSyntaxError("line %d: unmatching /[.../]" % line_number)
            break  # while True
    
    return b


def process_fe_pseudo_lang(input_lines, line_width):
    output_lines = []
    prev_li = -1
    for li, fh, sh, b in parse_struct_iter(input_lines, line_width):
        while prev_li < li - 1:
            output_lines.append('')  # print empty input lines
            prev_li += 1

        b = expand_special_symbols(li, b)

        # right alignment
        i = b.find('/;')
        if i >= 0:
            b, t = b[:i], b[i + len('/;'):]
        else:
            b, t = b, ''

        if b:
            # print line with splitting by line width
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
                output_lines.append(r)
                r = sh + ' '
        else:
            output_lines.append(fh)
        
        prev_li = li
    
    return output_lines

