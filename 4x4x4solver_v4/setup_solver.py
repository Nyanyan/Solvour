from distutils.core import setup, Extension
from Cython.Build import cythonize
from numpy import get_include # cimport numpy を使うため

ext = Extension("solver_c_22", sources=["solver_c.pyx"], include_dirs=['.', get_include()])
setup(name="solver_c_22", ext_modules=cythonize([ext]))