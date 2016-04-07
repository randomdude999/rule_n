#!/usr/bin/python3

class RuleN:
    """Rule 110, Rule 30, Rule 90 and Rule 184 interpreter. Usage:
    
    rule_110 = rule_n.RuleN(110, size=100) # Create Rule 110 interpreter
                                           # with 100 wide "canvas"

Default rule is 110, so the example could be shortened to:

    rule_110 = rule_n.RuleN(size=100)

Default size is 100, so even shorter:
    
    rule_110 = rule_n.RuleN()

    This works with eny numbered rule numbered in this manner, see the
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
        
        rules = []
        for x in range(0, 8):
            rules.append(bool(rule_descriptor & 2**x))
        self.rules = rules
        self.size = size
    
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
            result = 0
            if op_1:
                result += 4
            if op_2:
                result += 2
            if op_3:
                result += 1
            new_state.append(self.rules[result])
        return new_state
    
    def iter(self, state):
        """Process a starting state over and over again. Example:
        
        for x in rule_110(state):
            # Do something with the current state here
            # Note: You MUST break this yourself, or deal with the consequences

        """
        cur_state = state
        while True:
            yield cur_state
            cur_state = self.process(cur_state)
