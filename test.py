#!/usr/bin/python3

import unittest
import rule_n


class TestBasicStuff(unittest.TestCase):

    def test_init_invalid_ruledesc_type(self):
        self.assertRaises(TypeError, rule_n.RuleN, {'a': 'b'})

    def test_init_list(self):
        rule_110 = rule_n.RuleN()
        rule_110_2 = rule_n.RuleN([False, True, True, False, True, True, True,
            False])
        self.assertEqual(rule_110.rules, rule_110_2.rules)

    def test_init_tuple(self):
        rule_110 = rule_n.RuleN()
        rules = (False, True, True, False, True, True, True, False)
        rule_110_2 = rule_n.RuleN(rules)
        self.assertEqual(rule_110.rules, rule_110_2.rules)

    def test_init_str(self):
        rule_110 = rule_n.RuleN()
        rule_110_2 = rule_n.RuleN("01101110")
        self.assertEqual(rule_110.rules, rule_110_2.rules)

    def test_init_str_len_not8(self):
        rule_110 = rule_n.RuleN()
        rule_110_2 = rule_n.RuleN("0110111") # missing last 0
        self.assertEqual(rule_110.rules, rule_110_2.rules)

    def test_init_list_len_not8(self):
        rule_110 = rule_n.RuleN()
        rules = (False, True, True, False, True, True, True)
        rule_110_2 = rule_n.RuleN(rules)
        self.assertEqual(rule_110.rules, rule_110_2.rules)

    def test_init_ruledesc_loop_thing(self):
        # 111 has bit 0 but not bit 7
        self.assertRaises(ValueError, rule_n.RuleN, 111)

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

    def test_call(self):
        rule_110 = rule_n.RuleN()
        out1 = rule_110.process([True, False, True])
        out2 = rule_110([True, False, True])
        self.assertEqual(out1, out2)

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
            [False, True, True, False],
            [False, True, True, True, False],
            [True, True, False, True, False]
        ]
        self.assertEqual(outs, expected_outs)

if __name__ == '__main__':
    unittest.main()
