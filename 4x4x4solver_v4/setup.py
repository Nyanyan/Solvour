from distutils.core import setup, Extension
from Cython.Build import cythonize
from numpy import get_include # cimport numpy を使うため

ext = Extension("cube_class_c", sources=["cube_class.pyx"], include_dirs=['.', get_include()])
setup(name="cube_class_c", ext_modules=cythonize([ext]))