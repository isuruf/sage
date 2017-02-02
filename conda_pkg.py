#!/usr/bin/env python

import os

conda_pkgs = {
'alabaster' : 'alabaster',
'arb' : 'arb',
'babel' : 'babel',
'backports_abc' : 'backports_abc',
'backports_shutil_get_terminal_size' : 'backports.shutil_get_terminal_size',
'boost_cropped' : 'boost-cpp',
'bzip2' : 'bzip2',
'configparser' : 'configparser',
'cvxopt' : 'cvxopt',
'cycler' : 'cycler',
'cython' : 'cython',
'dateutil' : 'dateutil',
'decorator' : 'decorator',
'ecm' : 'ecm',
'entrypoints' : 'entrypoints',
'flask' : 'flask',
'flask_babel' : 'flask-babel',
'flask_openid' : 'flask-openid',
'flint' : 'libflint',
'freetype' : 'freetype',
'functools32' : 'functools32',
'future' : 'future',
'gc' : 'bdw-gc',
'gcc' : 'gcc',
'git' : 'git',
'glpk' : 'glpk',
'gsl' : 'gsl',
'iconv' : 'libiconv',
'imagesize' : 'imagesize',
'ipykernel' : 'ipykernel',
'ipython' : 'ipython',
'ipython_genutils' : 'ipython_genutils',
'ipywidgets' : 'ipywidgets',
'itsdangerous' : 'itsdangerous',
'jinja2' : 'jinja2',
'jupyter_client' : 'jupyter_client',
'jupyter_core' : 'jupyter_core',
'libgd' : 'libgd',
'libpng' : 'libpng',
'matplotlib' : 'matplotlib',
'mistune' : 'mistune',
'mpc' : 'mpc',
'mpfr' : 'mpfr',
'mpir' : 'gmp',
'mpmath' : 'mpmath',
'nbconvert' : 'nbconvert',
'nbformat' : 'nbformat',
'ncurses' : 'ncurses',
'networkx' : 'networkx',
'notebook' : 'notebook',
'numpy' : 'numpy=1.11',
'openblas' : 'openblas',
'pathlib2' : 'pathlib2',
'pexpect' : 'pexpect',
'pickleshare' : 'pickleshare',
'pillow' : 'pillow',
'pip' : 'pip',
'pkgconfig' : 'pkgconfig',
'prompt_toolkit' : 'prompt_toolkit',
'psutil' : 'psutil',
'ptyprocess' : 'ptyprocess',
'pycrypto' : 'pycrypto',
'pygments' : 'pygments',
'pyparsing' : 'pyparsing',
'python2' : 'python=2.7',
'python_openid' : 'python-openid',
'pytz' : 'pytz',
'pyzmq' : 'pyzmq',
'r' : 'r',
'readline' : 'readline',
'scipy' : 'scipy',
'setuptools' : 'setuptools',
'setuptools_scm' : 'setuptools_scm',
'simplegeneric' : 'simplegeneric',
'singledispatch' : 'singledispatch',
'six' : 'six',
'snowballstemmer' : 'snowballstemmer',
'sphinx' : 'sphinx',
'sqlite' : 'sqlite',
'sympy' : 'sympy',
'terminado' : 'terminado',
'tornado' : 'tornado',
'traitlets' : 'traitlets',
'vcversioner' : 'vcversioner',
'wcwidth' : 'wcwidth',
'werkzeug' : 'werkzeug',
'zeromq' : 'zeromq',
'zlib' : 'zlib'
}

sagelib_deps = ['arb', 'openblas', 'brial', 'cephes', 'cliquer', 'cysignals', 'cython', 'ecl', 'eclib', 'ecm', 'flint', 'libgd', 'givaro', 'glpk', 'gsl', 'iml', 'jinja2', 'jupyter_core', 'lcalc', 'lrcalc', 'libgap', 'libpng', 'linbox', 'm4ri', 'm4rie', 'mpc', 'mpfi', 'mpfr', 'gmp', 'ntl', 'numpy', 'pari', 'pip', 'pkgconfig', 'planarity', 'ppl', 'pynac', 'python', 'ratpoints', 'readline', 'rw', 'singular', 'six', 'symmetrica', 'zn_poly']

sageruntime_deps = sagelib_deps + ['ipython', 'pexpect', 'psutil']

deps_dict = {
'sageruntime' : sageruntime_deps,
}

def main()
    pkg_dir="build/pkgs"
    dirs = sorted([d for d in os.listdir(pkg_dir) if os.path.isdir(os.path.join(pkg_dir, d))])
    for pkg in dirs:
        if not pkg in conda_pkgs:
            continue
        conda_file = os.path.join(pkg_dir, pkg, "conda-name")    
        with open(conda_file, 'w') as f:
            f.write(conda_pkgs[pkg])

if __name__ == "__main__"
    main()

