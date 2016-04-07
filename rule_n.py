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

class RuleN:
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
    def _get_rules_from_descriptor(desc):
        rules = []
        for x in range(0, 8):
            rules.append(bool(desc & 2**x))
        return rules
        
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
        
        self.rules = _get_rules_from_descriptor(rule_descriptor)
        self.size = size

    def _process_bin_ints(op1, op2, op3):
        result = 0
        if op1:
            result += 4
        if op2:
            result += 2
        if op3:
            result += 1
        return result

    def process(self, state):
        """Process a state and return the next state"""
        if len(state) < self.size:
            state = [False] * (self.size - len(state)) + state
        new_state = []
        for x in range(0, self.size):
            if x == 0:
                op_1 = 0
            else:
                op_1 = state[x - 1]
            op_2 = state[x]
            if x == self.size - 1:
                op_3 = 0
            else:
                op_3 = state[x + 1]
            result = _process_bin_ints(op1, op2, op3)
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
