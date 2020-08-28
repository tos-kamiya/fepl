import unittest
import io
import os

import fepl
from fepl import do_process_fe_pseudo_lang


script_dir = os.path.basename(os.path.dirname(os.path.realpath(__file__)))


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
