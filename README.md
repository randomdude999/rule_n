# rule\_n

[![Build Status](https://travis-ci.org/randomdude999/rule_n.svg?branch=master)](https://travis-ci.org/randomdude999/rule_n)
[![Coverage Status](https://coveralls.io/repos/github/randomdude999/rule_n/badge.svg?branch=master)](https://coveralls.io/github/randomdude999/rule_n?branch=master)
[![Code Climate](https://codeclimate.com/github/randomdude999/rule_n/badges/gpa.svg)](https://codeclimate.com/github/randomdude999/rule_n)

This is a Python implemetation of Rule 110, Rule 30, Rule 90, Rule 184 and any other rule which follows this scheme.

## Usage

Download and put [`rule_n.py`](https://raw.githubusercontent.com/randomdude999/rule_n/master/rule_n.py) somewhere in your Python path. Then:

```python

import rule_n

rule_110 = rule_n.RuleN(110, size=100) # The size is the size of the imaginary
                                       # 'canvas' on which the stuff happens
rule_30 = rule_n.RuleN(30)  # Default size is 100, so that can be omitted
rule_184 = rule_n.RuleN(184)  # Works with anything from 1 to 255
rule_110 = rule_n.RuleN()  # Default rule is 110, as that is the most common

data = rule_110.process([True, False, True]) # If your provided input is not 
                                             # the width of the 'canvas', it
                                             # is left-padded with False's
len(data) # 100
data[96:100] # [True, True, True, True]
data[0:96] # [False] * 96

data_2 = rule_110.process([1, 0, 1]) # You can use any data type, as long as
                                     # the boolean values of these are correct
data == data_2 # True

i = 0
for x in rule_110.iterate([1, 0, 1]): # Repeatedly process a state
    print x
    i += 1
    if i == 10:
        break
```

More details on Rule 110 are on [Wikipedia](https://en.wikipedia.org/wiki/Rule_110).
