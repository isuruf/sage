#!/usr/bin/env python

import os

pkg_dir="build/pkgs"
dirs = sorted([d for d in os.listdir(pkg_dir) if os.path.isdir(os.path.join(pkg_dir, d))])

conda_pkgs = {
'alabaster' : 'alabaster',
'arb' : 'arb',
'autotools' : 'autotools',
'babel' : 'babel',
'backports_abc' : 'backports_abc',
'backports_shutil_get_terminal_size' : 'backports_shutil_get_terminal_size',
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
'flask_babel' : 'flask_babel',
'flask_openid' : 'flask_openid',
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
'python_openid' : 'python_openid',
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

all_pkgs = []

outputs = ""

for pkg in dirs:

    if pkg in conda_pkgs:
        print("%s already in conda-forge" %pkg)
        conda_file = os.path.join(pkg_dir, pkg, "conda-name")    
        with open(conda_file, 'w') as f:
            f.write(conda_pkgs[pkg])
        all_pkgs.append(conda_pkgs[pkg])
        continue

    type_file = os.path.join(pkg_dir, pkg, "type")    
    with open(type_file) as f:
        pkg_type = f.readlines()[0].strip()
        if (pkg_type != "standard") & (pkg not in ['patch', 'pkgconf']):
            print("%s is not standard" %pkg)
            continue

    deps_file = os.path.join(pkg_dir, pkg, "dependencies")
    if not os.path.exists(deps_file):
        deps_dict[pkg]=[]
        all_pkgs.append(pkg)
        continue
    with open(deps_file) as f:
        content = f.readlines()[0]
        if content[0] == "#":
            continue
        deps = content.strip()
        deps = deps.replace("$(PYTHON)", "python2")
        deps = deps.replace("| ", "")
        deps = deps.replace("$(MP_LIBRARY)", "gmp")
        deps = deps.replace("$(SAGE_MP_LIBRARY)", "gmp")
        deps = deps.replace("$(BLAS)", "openblas")
        deps = deps.replace("$(SAGERUNTIME)", "sageruntime")
        deps = deps.replace("$(INST)/", "")
        deps = deps.split()
        for i in range(len(deps)):
            d = deps[i]
            d = conda_pkgs.get(d, d)
            if '=' in d:
                d = d.split("=")[0]
            deps[i] = d
        deps_dict[pkg] = deps
        all_pkgs.append(pkg)

for pkg, deps in deps_dict.iteritems():
    outputs += "  - name: %s\n" % pkg
    if len(deps) > 0:
        outputs += "    requirements:"
        outputs += "\n      - "
        outputs += "\n      - ".join(deps)
        outputs += "\n"
        if (pkg == "sageruntime"):
            outputs += "    files:\n"
            outputs += "      - bin/**\n"

all_pkgs = "    - " + "\n    - ".join(all_pkgs)
conda_pkgs = "    - " + "\n    - ".join(sorted(conda_pkgs.keys()))

meta_yaml = """
{%% set version = "7.5.1" %%}

package:
  name: sage
  version: {{ version }}

source:
  fn: sage-{{ version }}.tar.gz
  url: http://mirrors-usa.go-parts.com/sage/sagemath/src/sage-{{ version }}.tar.gz

build:
  number: 0
  skip: true        # [win]

requirements:
  build:
    - m4
    - perl
    - pkg-config
%s
  run:
%s

outputs:
%s

""";

meta_yaml

print(meta_yaml % (conda_pkgs, all_pkgs, outputs))

