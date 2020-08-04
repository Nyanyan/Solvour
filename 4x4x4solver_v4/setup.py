from distutils.core import setup, Extension
from Cython.Build import cythonize
from numpy import get_include # cimport numpy を使うため

ext = Extension("cube_class_c_4", sources=["cube_class_c.pyx"], include_dirs=['.', get_include()])
setup(name="cube_class_c_4", ext_modules=cythonize([ext]))