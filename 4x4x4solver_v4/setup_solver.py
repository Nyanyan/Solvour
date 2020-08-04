from distutils.core import setup, Extension
from Cython.Build import cythonize
from numpy import get_include # cimport numpy を使うため

ext = Extension("solver_par_c_24", sources=["solver_par_c.pyx"], include_dirs=['.', get_include()])
setup(name="solver_par_c_24", ext_modules=cythonize([ext]))