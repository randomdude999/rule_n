#!/usr/bin/python3
# -*- coding: utf-8 -*-

# rule_n - Elementary cellular automata in Python
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

"""Elementary cellular automata in Python. (See
<http://en.wikipedia.org/wiki/Elementary_cellular_automaton>)

Usage:

    import rule_n

    rule_110 = rule_n.RuleN(110)
    rule_30 = rule_n.RuleN(30)
    rule_184 = rule_n.RuleN(184)  # Works with anything from 1 to 255
    rule_110 = rule_n.RuleN()  # Default rule is 110
    from rule_n import rule_90   # Shorthand for rule_90 = rule_n.RuleN(90)
                                 # Works with 110, 30, 90, 184
    # You can also specify a list of rules
    rule_110 = rule_n.RuleN([False, True, True, False] + [True] * 3 + [False])
    # Or a string that summarizes the rule
    rule_110 = rule_n.RuleN("01101110")
    # See <https://en.wikipedia.org/wiki/Rule_110#Definition>
    # You can also have a finite canvas
    rule_110_finite_canvas = rule_n.RuleN(110, canvas_size=5)
    # A canvas is finite if its size is over 0

    data = rule_110.process([True, False, True])
    len(data) == 5  # because a False is added to both sides
    data == [True, True, True, True, False]

    data_2 = rule_110.process([1, 0, 1])  # You can use any data type, as long
    data == data_2                        # as the boolean values of these are
                                          # correct
                                          # Return values are always in boolean

    # With a finite canvas, the output is always as big as the canvas
    data = rule_110_finite_canvas.process([0, 0, 0, 0, 1])
    data == [False, False, False, True, True]

    data_3 = rule_110([True, False, True])  # Shorthand for
                                            # rule_110.process(state)
    data == data_3

    i = 0
    for x in rule_110.iterate([1, 0, 1]):  # Repeatedly process a state
        print x
        i += 1
        if i == 10:
            break  # Please do this
    # Note: Iteration on an infinte canvas seems to have some problems
    # I recommend using a finite canvas
    for x in rule_110_finite_canvas.iterate([0, 0, 0, 0, 1]):
        print x
        # This breaks automatically if the current state is equal to the
        # previous, which will probably happen at some point on a finite canvas
"""


def _process_cell(i, state, finite=False):
    """Process 3 cells and return a value from 0 to 7. """
    op_1 = state[i - 1]
    op_2 = state[i]
    if i == len(state) - 1:
        if finite:
            op_3 = state[0]
        else:
            op_3 = 0
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


def _crop_list_to_size(l, size):
    """Make a list a certain size"""
    for x in range(size - len(l)):
        l.append(False)
    for x in range(len(l) - size):
        l.pop()
    return l


def _rules_from_int(inp):
    rules = []
    for i in range(8):
        rules.append(bool(inp & 2**i))
    return rules


def _rules_from_list(l):
    rules = _crop_list_to_size(list(l), 8)
    rules.reverse()
    return rules


def _rules_from_str(s):
    rules = []
    if len(s) < 8:
        s += "0" * (8 - len(s))
    null_chars = " 0"
    for x in range(8):
        if s[x] in null_chars:
            rules.append(False)
        else:
            rules.append(True)
    rules.reverse()
    return rules


def _proc_rules(rule_descriptor):
    if type(rule_descriptor) is int:
        return _rules_from_int(rule_descriptor)
    elif type(rule_descriptor) is list or type(rule_descriptor) is tuple:
        return _rules_from_list(rule_descriptor)
    elif type(rule_descriptor) is str:
        return _rules_from_str(rule_descriptor)
    else:
        raise TypeError("Invalid rule_descriptor type (must be int, list, "
                        "str or tuple)")


class RuleN(object):
    """Elementary cellular automata "interpreter". Usage:

    rule_110 = rule_n.RuleN(110) # Create Rule 110 interpreter

Default rule is 110, so the example could be shortened to:

    rule_110 = rule_n.RuleN()

This works with any numbered rule numbered in this manner, see
<http://en.wikipedia.org/wiki/Rule_110#Definition> to learn more.

You can also specify a list of actions directly. In this case, 110 would become
[False, True, True, False, True, True, True, False]. See the abovementioned
link for explanation.

You can also specify the list of actions as a string of 0's and 1's. 110 would
be "01101110".

    rule_110 = rule_n.RuleN("01101110")

You can also have a finite canvas:

    rule_110 = rule_n.RuleN(110, canvas_size=5)

A canvas is finite if its size is more than 0.
"""
    def __init__(self, rule_descriptor=110, canvas_size=0):
        self.rules = _proc_rules(rule_descriptor)
        if canvas_size <= 0:
            if bool(self.rules[0]) and not bool(self.rules[7]):
                raise ValueError("111 can't turn to 0 when 000 turns to 1")
            self.default_val = self.rules[7]
            self.finite_canvas = False
            self.canvas_size = 0
        else:
            self.canvas_size = canvas_size
            self.finite_canvas = True

    def __call__(self, state):
        return self.process(state)

    def __repr__(self):
        descriptor = 0
        for i, x in enumerate(self.rules):
            descriptor += 2**i if x else 0
        return "%s.%s(%s)" % (self.__class__.__module__,
                              self.__class__.__name__, descriptor)

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return (self.rules == other.rules and
                    self.canvas_size == other.canvas_size)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

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
        if self.finite_canvas:
            state = _crop_list_to_size(state, self.canvas_size)
        else:
            state = _remove_lead_trail_false(state)
            state.insert(0, self.default_val)
            state.append(self.default_val)
        new_state = []
        for i in range(0, len(state)):
            result = _process_cell(i, state, finite=self.finite_canvas)
            new_state.append(self.rules[result])
        return new_state

    def iterate(self, state):
        """Process a starting state over and over again. Example:

        for x in rule_110.iterate(state):
            # Do something with the current state here
            # Note: You should break this yourself
        # This breaks automatically if the previous state was the same as the
        # current one, but that's not gonna happen on an infinite canvas
"""
        cur_state = state
        old_state = cur_state
        while True:
            cur_state = self.process(cur_state)
            if old_state == cur_state:
                break
            old_state = cur_state
            yield cur_state

# 4 most common ones get shorthands
rule_110 = RuleN(110)
rule_30 = RuleN(30)
rule_90 = RuleN(90)
rule_184 = RuleN(184)
