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

"""Python Rule 110 (and 30, 90 and 184) implementation. (See
<http://en.wikipedia.org/wiki/Rule_110>)

Usage:

    import rule_n

    rule_110 = rule_n.RuleN(110)
    rule_30 = rule_n.RuleN(30)
    rule_184 = rule_n.RuleN(184)  # Works with anything from 1 to 255
    rule_110 = rule_n.RuleN()  # Default rule is 110

    data = rule_110.process([True, False, True])
    len(data) == 5  # because a False is added to both sides
    data == [True, True, True, True, False]

    data_2 = rule_110.process([1, 0, 1]) # You can use any data type, as long
    data == data_2                       # as the boolean values of these are
                                         # correct
                                         # Return values are always in boolean

    data_3 = rule_110([True, False, True])  # Shorthand for
                                            # rule_110.process(state)
    data == data_3

    i = 0
    for x in rule_110.iterate([1, 0, 1]): # Repeatedly process a state
        print x
        i += 1
        if i == 10:
            break

    from rule_n import rule_90  # Shorthand for rule_90 = rule_n.RuleN(90)
                                # Works with 110, 30, 90, 184

"""


def _get_rules(desc):
    """get a list of true/false from a rule descriptor, such as 110"""
    rules = []
    for i in range(0, 8):
        rules.append(bool(desc & 2**i))  # bool(desc & 2**i) gets if that bit
    return rules                         # is set


def _process_cell(i, state):
    """Process 3 cells and return a value from 0 to 7. """
    if i == 0:
        op_1 = 0  # All 0's before the beginning
    else:
        op_1 = state[i - 1]
    op_2 = state[i]
    if i == len(state) - 1:
        op_3 = 0  # All 0's after the end
    else:
        op_3 = state[i + 1]
    result = 0
    for i, val in enumerate([op_3, op_2, op_1]):
        if val:
            result += 2**i
    return result


def _remove_lead_trail_false(bool_list):
    """Remove leading and trailing false's from a list"""
    # The internet can be a wonderful place...
    for i in (0, -1):
        while bool_list and not bool_list[i]:
            bool_list.pop(i)
    return bool_list


class RuleN(object):
    """Rule 110, Rule 30, Rule 90 and Rule 184 interpreter. Usage:

    rule_110 = rule_n.RuleN(110) # Create Rule 110 interpreter

Default rule is 110, so the example could be shortened to:

    rule_110 = rule_n.RuleN()

    This works with any numbered rule numbered in this manner, see
    <http://en.wikipedia.org/wiki/Rule_110#Definition> to learn more.
"""
    def __init__(self, rule_descriptor=110):
        if not isinstance(rule_descriptor, int):
            raise TypeError("rule descriptor must be integer")
        elif rule_descriptor < 0:
            raise TypeError("rule descriptor must be more than or equal to 0")
        elif rule_descriptor >= 256:
            raise TypeError("rule descriptor must be less than 256")
        elif bool(rule_descriptor & 2**0) and not bool(rule_descriptor & 2**7):
            raise TypeError("rule_descriptor bit 0 can't be true if bit 7"
                            " is false")
        self.default_val = bool(rule_descriptor % 2)   # What to expand with in
        self.rules = _get_rules(rule_descriptor)       # both directions

    def __call__(self, state):
        return self.process(state)

    def process(self, state):
        """Process a state and return the next state
Usage:

    out = rule_110.process([True, False, True])
    len(out)  # 5, because a False is added to either side
    out == [True, True, True, True, False]
    out = rule_110.process([False, True, False, True])
    len(out)  # still 5, because leading / trailing False's are removed
    out2 = rule_110.process([1, 0, 1])  # Any data type in the list is okay, as
                                        # long as it's boolean value is correct
    out == out2
"""
        if not isinstance(state, list):
            raise TypeError("state must be list")
        state = _remove_lead_trail_false(state)
        state.insert(0, self.default_val)
        state.append(self.default_val)
        new_state = []
        for i in range(0, len(state)):
            result = _process_cell(i, state)
            new_state.append(self.rules[result])
        return new_state

    def iterate(self, state):
        """Process a starting state over and over again. Example:

        for x in rule_110.iterate(state):
            # Do something with the current state here
            # Note: You MUST break this yourself, or deal with the consequences

"""
        cur_state = state
        while True:
            cur_state = self.process(cur_state)
            yield cur_state

# 4 most common ones get shorthands
rule_110 = RuleN(110)
rule_30 = RuleN(30)
rule_90 = RuleN(90)
rule_184 = RuleN(184)
