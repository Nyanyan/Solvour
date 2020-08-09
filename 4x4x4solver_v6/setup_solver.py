'''
4x4x4 Solver Cython Setup Part Written by Nyanyan
Copyright 2020 Nyanyan
'''

from distutils.core import setup, Extension
from Cython.Build import cythonize
from numpy import get_include # cimport numpy を使うため

ext = Extension("solver_c_14", sources=["solver_c.pyx"], include_dirs=['.', get_include()])
setup(name="solver_c_14", ext_modules=cythonize([ext]))