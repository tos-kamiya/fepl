import unittest
import io
import os

import fepl
from fepl import process_fe_pseudo_lang


script_dir = os.path.dirname(os.path.realpath(__file__))


def do_process_fe_pseudo_lang(outp, input_lines, line_width):
    output_lines = process_fe_pseudo_lang(input_lines, line_width)
    print('\n'.join(output_lines), file=outp)


def read_resource_file(fn):
    fp = os.path.join(script_dir, fn)
    with open(fp) as inp:
        return inp.read()


def replace_punct_chars(s):
    return s.replace(' ', '␣').replace('\n', '⏎\n')


R = replace_punct_chars


class FeplTest(unittest.TestCase):
    def test_input1(self):
        inp = io.StringIO(read_resource_file('input1.txt'))
        outp = io.StringIO('')
        do_process_fe_pseudo_lang(outp, inp, 78)
        self.assertEqual(R(outp.getvalue()), R(read_resource_file('expected1.txt')))

    def test_input2(self):
        inp = io.StringIO(read_resource_file('input2.txt'))
        outp = io.StringIO('')
        do_process_fe_pseudo_lang(outp, inp, 78)
        self.assertEqual(R(outp.getvalue()), R(read_resource_file('expected2.txt')))

    def test_input3(self):
        inp = io.StringIO(read_resource_file('input3.txt'))
        outp = io.StringIO('')
        do_process_fe_pseudo_lang(outp, inp, 78)
        self.assertEqual(R(outp.getvalue()), R(read_resource_file('expected3.txt')))

    def test_input4(self):
        inp = io.StringIO(read_resource_file('input4.txt'))
        outp = io.StringIO('')
        do_process_fe_pseudo_lang(outp, inp, 78)
        self.assertEqual(R(outp.getvalue()), R(read_resource_file('expected4.txt')))

    def test_syntaxerr1(self):
        inp = io.StringIO(read_resource_file('syntaxerr1.txt'))
        with self.assertRaises(fepl.FeplSyntaxError) as cm:
            do_process_fe_pseudo_lang(io.StringIO(''), inp, 78)
        self.assertIsInstance(cm.exception, fepl.FeplSyntaxError)

    def test_syntaxerr2(self):
        inp = io.StringIO(read_resource_file('syntaxerr2.txt'))
        with self.assertRaises(fepl.FeplSyntaxError) as cm:
            do_process_fe_pseudo_lang(io.StringIO(''), inp, 78)
        self.assertIsInstance(cm.exception, fepl.FeplSyntaxError)

    def test_syntaxerr3(self):
        inp = io.StringIO(read_resource_file('syntaxerr3.txt'))
        with self.assertRaises(fepl.FeplSyntaxError) as cm:
            do_process_fe_pseudo_lang(io.StringIO(''), inp, 78)
        self.assertIsInstance(cm.exception, fepl.FeplSyntaxError)

    def test_syntaxerr4(self):
        inp = io.StringIO(read_resource_file('syntaxerr4.txt'))
        with self.assertRaises(fepl.FeplSyntaxError) as cm:
            do_process_fe_pseudo_lang(io.StringIO(''), inp, 78)
        self.assertIsInstance(cm.exception, fepl.FeplSyntaxError)

    def test_syntaxerr5(self):
        inp = io.StringIO(read_resource_file('syntaxerr5.txt'))
        with self.assertRaises(fepl.FeplSyntaxError) as cm:
            do_process_fe_pseudo_lang(io.StringIO(''), inp, 78)
        self.assertIsInstance(cm.exception, fepl.FeplSyntaxError)

    def test_input_looseindent1(self):
        inp = io.StringIO(read_resource_file('input_looseindent1.txt'))
        outp = io.StringIO('')
        do_process_fe_pseudo_lang(outp, inp, 78)
        self.assertEqual(R(outp.getvalue()), R(read_resource_file('expected_looseindent1.txt')))

    def test_input_looseindent2(self):
        inp = io.StringIO(read_resource_file('input_looseindent2.txt'))
        outp = io.StringIO('')
        do_process_fe_pseudo_lang(outp, inp, 78)
        self.assertEqual(R(outp.getvalue()), R(read_resource_file('expected_looseindent2.txt')))

    def test_input5(self):
        inp = io.StringIO(read_resource_file('input5.txt'))
        outp = io.StringIO('')
        do_process_fe_pseudo_lang(outp, inp, 78)
        self.assertEqual(R(outp.getvalue()), R(read_resource_file('expected5.txt')))

    def test_input6(self):
        inp = io.StringIO(read_resource_file('input6.txt'))
        outp = io.StringIO('')
        do_process_fe_pseudo_lang(outp, inp, 40)
        self.assertEqual(R(outp.getvalue()), R(read_resource_file('expected6.txt')))

    def test_input7(self):
        inp = io.StringIO(read_resource_file('input7.txt'))
        outp = io.StringIO('')
        do_process_fe_pseudo_lang(outp, inp, 40)
        self.assertEqual(R(outp.getvalue()), R(read_resource_file('expected7.txt')))

    def test_syntaxerr_writeinbox_unmatch(self):
        inp = io.StringIO(read_resource_file('syntaxerr_writeinbox_unmatch.txt'))
        with self.assertRaises(fepl.FeplSyntaxError) as cm:
            do_process_fe_pseudo_lang(io.StringIO(''), inp, 78)
        self.assertIsInstance(cm.exception, fepl.FeplSyntaxError)

    def test_syntaxerr_writeinbox_unmatch2(self):
        inp = io.StringIO(read_resource_file('syntaxerr_writeinbox_unmatch2.txt'))
        with self.assertRaises(fepl.FeplSyntaxError) as cm:
            do_process_fe_pseudo_lang(io.StringIO(''), inp, 78)
        self.assertIsInstance(cm.exception, fepl.FeplSyntaxError)
