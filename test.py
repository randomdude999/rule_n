#!/usr/bin/python3

import unittest
import rule_n

class TestBasicStuff(unittest.TestCase):

    def test_init_ruledesc_nonint(self):
        self.assertRaises(TypeError, rule_n.RuleN, "Hello")

    def test_init_ruldedesc_lessthan_1(self):
        self.assertRaises(TypeError, rule_n.RuleN, 0)

    def test_init_ruledesc_morethan_255(self):
        self.assertRaises(TypeError, rule_n.RuleN, 256)

    def test_init_ruledesc_odd(self):
        self.assertRaises(TypeError, rule_n.RuleN, 127)

    def test_init_default_rule(self):
        rule_110 = rule_n.RuleN()
        rule_110_2 = rule_n.RuleN(110)
        self.assertEqual(rule_110.rules, rule_110_2.rules)

    def test_init_working(self):
        rule_110 = rule_n.RuleN(110)
        correct_rules = [False, True, True, True, False, True, True, False]
        self.assertEqual(rule_110.rules, correct_rules)

    def test_process(self):
        rule_110 = rule_n.RuleN()
        expected_out = [True] * 4 + [False]
        inp = [True, False, True]
        out = rule_110.process(inp)
        self.assertEqual(out, expected_out)

    def test_process_nonlist(self):
        rule_110 = rule_n.RuleN()
        self.assertRaises(TypeError, rule_110.process, "Hello!")

    def test_iter(self):
        rule_110 = rule_n.RuleN()
        start = [True]
        i = 0
        outs = []
        for x in rule_110.iterate(start):
            outs.append(x)
            i += 1
            if i == 3:
                break
        expected_outs = [  # XXX: I have no idea either
            [False, True , True , False],
            [False, True , True , True , False],
            [True , True , False, True , False]
        ]
        self.assertEqual(outs, expected_outs)

if __name__ == '__main__':
    unittest.main()
