========
 rule_n
========

.. image:: https://travis-ci.org/randomdude999/rule_n.svg
   :target: https://travis-ci.org/randomdude999/rule_n
   :alt: Travis CI
.. image:: https://coveralls.io/repos/github/randomdude999/rule_n/badge.svg 
   :target: https://coveralls.io/github/randomdude999/rule_n
   :alt: Coveralls
.. image:: https://codeclimate.com/github/randomdude999/rule_n/badges/gpa.svg
   :target: https://codeclimate.com/github/randomdude999/rule_n
   :alt: Code Climate
.. image:: https://img.shields.io/pypi/v/rule_n.svg
   :target: https://pypi.python.org/pypi/rule_n
   :alt: PyPI
.. image:: https://img.shields.io/pypi/dm/rule_n.svg
   :target: https://pypi.python.org/pypi/rule_n#downloads
   :alt: Downloads
.. image:: https://img.shields.io/pypi/l/rule_n.svg
   :target: https://raw.githubusercontent.com/randomdude999/rule_n/master/LICENSE
   :alt: License
.. image:: https://img.shields.io/github/issues-raw/randomdude999/rule_n.svg
   :target: https://github.com/randomdude999/rule_n/issues
   :alt: Issues

This is a Python implementation of elementary cellular automata. <https://en.wikipedia.org/wiki/Elementary_cellular_automata>

Installation
============

Pip
---

::

  pip install rule_n

Manual
------

Download |rule_n.py|_ and put it somewhere in your Python path.

.. |rule_n.py| replace:: ``rule_n.py``
.. _rule_n.py: https://raw.githubusercontent.com/randomdude999/rule_n/master/rule_n.py

Usage
=====

::

 import rule_n

 rule_110 = rule_n.RuleN(110)
 rule_30 = rule_n.RuleN(30)
 rule_184 = rule_n.RuleN(184)  # Works with anything from 1 to 255
 rule_110 = rule_n.RuleN()  # Default rule is 110, as that is the most common
 from rule_n import rule_90   # Shorthand for rule_90 = rule_n.RuleN(90)
                              # Works with 110, 30, 90, 184
 # You can also specify a list of rules
 rule_110 = rule_n.RuleN([False, True, True, False, True, True, True, False])
 # Or a string that summarizes the rule
 rule_110 = rule_n.RuleN("01101110")
 # See <https://en.wikipedia.org/wiki/Rule_110#Definition>

 data = rule_110.process([True, False, True]) 
 len(data) == 5  # because a False is added to both sides
 data == [True, True, True, True, False]

 data_2 = rule_110.process([1, 0, 1])  # You can use any data type, as long
 data == data_2                        # as the boolean values of these are
                                       # correct
                                       # Return values are always in boolean

 data_3 = rule_110([True, False, True])  # Shorthand for
                                         # rule_110.process(state)
 data == data_3

 i = 0
 for x in rule_110.iterate([1, 0, 1]):  # Repeatedly process a state
     print x
     i += 1
     if i == 10:
         break  # Please do this
