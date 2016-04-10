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

    rule_110 = rule_n.RuleN(110)
    rule_30 = rule_n.RuleN(30)

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


def _process_cell(i, state):
    """Process 3 cells and return a value from 0 to 7. """
    if i == 0:
        op_1 = 0
    else:
        op_1 = state[i - 1]
    op_2 = state[i]
    if i == len(state) - 1:
        op_3 = 0
    else:
        op_3 = state[i + 1]
    result = 0
    op_list = [op_3, op_2, op_1]
    for i, val in enumerate(op_list):
        if val:
            result += 2**i
    return result

def _remove_lead_trail_false(bool_list):
    """Remove leading and trailing false's from a list"""
    for i in (0, -1):
        while bool_list and not bool_list[i]:
            bool_list.pop(i)
    return bool_list


class RuleN(object):
    """Rule 110, Rule 30, Rule 90 and Rule 184 interpreter. Usage:

    rule_110 = rule_n.RuleN(110) # Create Rule 110 interpreter

Default rule is 110, so the example could be shortened to:

    rule_110 = rule_n.RuleN()

    This works with any numbered rule numbered in this manner, see the
    "Definition" section on the Wikipedia page on "Rule 110" to learn more.
"""
    def __init__(self, rule_descriptor=110):
        if type(rule_descriptor) is not int:
            raise TypeError("rule descriptor must be integer")
        elif rule_descriptor < 1:
            raise TypeError("rule descriptor must be more than 0")
        elif rule_descriptor > 255:
            raise TypeError("rule descriptor must be less than 256")
        elif rule_descriptor % 2 == 1:
            raise TypeError("rule descriptor must be odd (TODO: make "
                            "this not exist)")

        self.rules = _get_rules(rule_descriptor)

    def process(self, state):
        """Process a state and return the next state
Usage:

    out = rule_110.process([True, False, True])
    len(out) # 5, because a False is added to either side
    out # [True, True, True, True, False]
    out = rule_110.process([False, True, False, True])
    len(out) # still 5, because leading / trailing False's are removed
"""
        if type(state) is not list:
            raise TypeError("state must be list")
        state = _remove_lead_trail_false(state)
        state.insert(0, False)
        state.append(False)
        new_state = []
        for i in range(0, len(state)):
            result = _process_cell(i, state)
            new_state.append(self.rules[result])
        return new_state

    def iterate(self, state):
        """Process a starting state over and over again. Example:

        for x in rule_110(state):
            # Do something with the current state here
            # Note: You MUST break this yourself, or deal with the consequences

"""
        if type(state) is not list:
            raise TypeError("state must be list")
        cur_state = state
        while True:
            cur_state = self.process(cur_state)
            yield cur_state
