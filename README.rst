========
 rule_n
========

.. image:: https://travis-ci.org/randomdude999/rule_n.svg
   :target: https://travis-ci.org/randomdude999/rule_n
   :title: Travis CI
.. image:: https://coveralls.io/repos/github/randomdude999/rule_n/badge.svg 
   :target: https://coveralls.io/github/randomdude999/rule_n
   :title: Coveralls
.. image:: https://codeclimate.com/github/randomdude999/rule_n/badges/gpa.svg
   :target: https://codeclimate.com/github/randomdude999/rule_n
   :title: Code Climate

This is a Python implementation of Rule 110, Rule 30, Rule 90, Rule 184 and any other rule which follows this scheme.

Installation
============

Pip
---

``pip install rule_n``

Manual
------

Download ``rule_n.py`` and put it somewhere in your Python path.

Usage
=====

..code-block: python

  import rule_n

  rule_110 = rule_n.RuleN(110)
  rule_30 = rule_n.RuleN(30)
  rule_184 = rule_n.RuleN(184)  # Works with anything from 1 to 255
  rule_110 = rule_n.RuleN()  # Default rule is 110, as that is the most common

  data = rule_110.process([True, False, True]) 
  len(data) == 5  # because a False is addad to both sides
  data == [True, True, True, True, False]

  data_2 = rule_110.process([1, 0, 1])  # You can use any data type, as long as
  data == data_2                        # the boolean values of these are correct
                                        # Return values are always in boolean

  data_3 = rule_110([True, False, True])  # Shorthand for rule_110.process(state)
  data == data_3

  i = 0
  for x in rule_110.iterate([1, 0, 1]):  # Repeatedly process a state
      print x
      i += 1
      if i == 10:
          break  # Please do this

  from rule_n import rule_90  # Shorthand for rule_90 = rule_n.RuleN(90)
                              # Works with 110, 30, 90, 184
