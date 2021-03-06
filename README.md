![CI](https://github.com/RobertWilbrandt/bm257s/workflows/CI/badge.svg?branch=main)

Brymen BM257s Serial Library
============================

Small python 3 library to access the serial interface of brymen BM257s multimeters. It is developed with the brymen BRUA-20X USB kit and uses the brymen 6000-count digital multimeter communication protocol, meaning it will probably work with similar enough multimeters too.

Installation
------------

The easiest way to install this library is to use pip:

```console
$ git clone git@github.com:RobertWilbrandt/bm257s.git && cd bm257s  # Clone library
$ pip3 install --user -r requirements.txt  # Install requirements
$ pip3 install --user .  # Install library
```

Features
--------

The library currently does currently not support too many measuring modes. For supported modes, i distinguish between semi-complete support (meaning it will give you the correct values if you have the mode selected) and complete support (meaning it will additionally correctly detect when you are not in the mode).

| Measuring mode   | Semi-Complete | Complete|
|------------------|:-------------:|---------|
| Temperature (°C) | X             |         |
| Temperature (F)  | X             |         |
| Resistance (Ω)   | X             |         |
| Resistance (kΩ)  | X             |         |
| Resistance (MΩ)  | X             |         |
| Voltage DC (V)   | X             |         |
| Voltage AC (V)   | X             |         |

Code Style
----------

This project uses various linters to enforce its code style:
- The [black](https://black.readthedocs.io/en/stable/) code formatter
- [isort](https://pycqa.github.io/isort/) for nicely sorted imports
- The [flake8](https://flake8.pycqa.org/en/latest/) linter
- The [pylint](https://www.pylint.org/) linter

They are integrated into automatic testing and run automatically in ci.

Testing
-------

This project uses [tox](https://tox.readthedocs.io/en/latest/) for testing automation. It runs the included [unittest](https://docs.python.org/3/library/unittest.html) tests and checks the linters discussed in [Code Style](#code-style).

If you want to run the tests locally you first need to install ```tox``` using ```pip3 install --user tox```. Then you should be able to start testing:

```console
$ tox
```
