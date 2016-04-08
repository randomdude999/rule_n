#!/usr/bin/python3
# -*- coding: utf-8 -*-

# rule_n - Python Rule 110 (and more) implementation.
# Copyright (C) 2016  randomdude999
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Python Rule 110 (and 30, 90 and 184) implemetation.

Usage:

    rule_110 = rule_n.RuleN(110, size=100)
    rule_30 = rule_n.RuleN(30, size=100)

    output = rule_110.process([True, False, True])

See documentation on RuleN.process, RuleN and RuleN.iterate for
for more information.

"""


def _get_rules(desc):
    """get a list of true/false from a rule descriptor, such as 110"""
    rules = []
    for i in range(0, 8):
        rules.append(bool(desc & 2**i))
    return rules


def _process_bin_ints(*args):
    """Process binary values into a number (used to index the rules)"""
    result = 0
    l = list(args)
    l.reverse()
    for i, b in enumerate(l):
        if b:
            result += 2**i
    return result


class RuleN(object):
    """Rule 110, Rule 30, Rule 90 and Rule 184 interpreter. Usage:

    rule_110 = rule_n.RuleN(110, size=100) # Create Rule 110 interpreter
                                           # with 100 wide "canvas"

Default rule is 110, so the example could be shortened to:

    rule_110 = rule_n.RuleN(size=100)

Default size is 100, so even shorter:

    rule_110 = rule_n.RuleN()

    This works with any numbered rule numbered in this manner, see the
    "Definition" section on the Wikipedia page on "Rule 110" to learn more.
"""
    def __init__(self, rule_descriptor=110, size=100):
        if type(size) is not int:
            raise TypeError("size must be integer")
        elif type(rule_descriptor) is not int:
            raise TypeError("rule_descriptor must be integer")
        elif size < 1:
            raise TypeError("size must be positive integer")
        elif not 255 > rule_descriptor > 0:
            raise TypeError("rule_descriptor must be integer between 1 and "
                            "255")

        self.rules = _get_rules(rule_descriptor)
        self.size = size

    def process(self, state):
        """Process a state and return the next state
Usage:

    out = rule_110.process([True, False, True]) # If your input is not as
                                                # long as your "canvas", the
                                                # input is left-padded with
    len(out) # 100                              # False's
    out[96:100] # [True, True, True, True]
    out[0:96] # [False] * 96
"""
        if len(state) < self.size:
            state = [False] * (self.size - len(state)) + state
        new_state = []
        for i in range(0, self.size):
            if i == 0:
                op_1 = 0
            else:
                op_1 = state[i - 1]
            op_2 = state[i]
            if i == self.size - 1:
                op_3 = 0
            else:
                op_3 = state[i + 1]
            result = _process_bin_ints(op_1, op_2, op_3)
            new_state.append(self.rules[result])
        return new_state

    def iterate(self, state):
        """Process a starting state over and over again. Example:

        for x in rule_110(state):
            # Do something with the current state here
            # Note: You MUST break this yourself, or deal with the consequences

"""
        cur_state = state
        while True:
            cur_state = self.process(cur_state)
            yield cur_state
