#!/usr/bin/python3

import unittest
import rule_n

class TestBasicStuff(unittest.TestCase):

    def test_init_size_nonint(self):
        self.assertRaises(TypeError, rule_n.RuleN, 110, "hello")

    def test_init_ruledesc_nonint(self):
        self.assertRaises(TypeError, rule_n.RuleN, "Hello", 100)

    def test_init_size_lessthan_0(self):
        self.assertRaises(TypeError, rule_n.RuleN, 110, -1)

    def test_init_ruldedesc_lessthan_1(self):
        self.assertRaises(TypeError, rule_n.RuleN, 0, 100)

    def test_init_ruledesc_morethan_255(self):
        self.assertRaises(TypeError, rule_n.RuleN, 256, 100)

    def test_init_working(self):
        rule_110 = rule_n.RuleN(110, size=100)
        correct_rules = [False, True, True, True, False, True, True, False]
        self.assertEqual(rule_110.rules, correct_rules)
        self.assertEqual(rule_110.size, 100)

    def test_process(self):
        rule_110 = rule_n.RuleN()
        expected_out = [False] * 96 + [True] * 4
        inp = [True, False, True]
        out = rule_110.process(inp)
        self.assertEqual(out, expected_out)

    def test_iter(self):
        rule_110 = rule_n.RuleN(size=5)
        start = [False, False, False, False, True]
        i = 0
        outs = []
        for x in rule_110.iterate(start):
            outs.append(x)
            i += 1
            if i == 3:
                break
        expected_outs = [
            [False, False, False, True , True],
            [False, False, True , True , True],
            [False, True , True , False, True]
        ]
        self.assertEqual(outs, expected_outs)
if __name__ == '__main__':
    unittest.main()
