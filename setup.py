#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# title:        setup.py
# date:         December 2020
# author:       Manuel Häusler
# email:        manuel.haeusler@hslu.ch
# version:      1.0
#==============================================================================+

from setuptools import find_packages, setup
setup(
    name='modelicaPost',
    packages=find_packages(),
    version='1.0.0',
    description='Library to postprocess modelica simulations (Dymola or OpenModelica)',
    author='Manuel Häusler',
    license='MIT',
    package_data={'modelicaPost':['custom.mplstyle']},
    include_package_data=True,
)