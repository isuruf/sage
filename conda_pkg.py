import os
import subprocess

sage_root = os.path.dirname(os.path.realpath(__file__))
sage_local = os.path.join(sage_root, "local")
pkg_dir=os.path.join(sage_root, "build/pkgs")

conda_pkgs = {
'alabaster' : 'alabaster',
#'arb' : 'arb',
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
#'flint' : 'libflint',
'freetype' : 'freetype',
'functools32' : 'functools32',
'future' : 'future',
'gc' : 'bdw-gc',
'gcc' : 'gmp',
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
'markupsafe' : 'markupsafe',
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

features = { "openblas" : "blas_openblas" }

# copied from https://github.com/conda-forge/conda-forge.github.io/blob/master/scripts/pin_the_slow_way.py
pinnings = {
'boost': 'boost 1.63.*',
'boost-cpp': 'boost-cpp 1.63.*',
'bzip2': 'bzip2 1.0.*',
'cairo': 'cairo 1.14.*',
'ffmpeg': 'ffmpeg 2.8.*',
'fontconfig': 'fontconfig 2.12.*',
'freetype': 'freetype 2.7|2.7.*',
'geos': 'geos 3.5.*',
'giflib': 'giflib 5.1.*',
'glib': 'glib 2.51.*',
'harfbuzz': 'harfbuzz 1.3.*',
'hdf5': 'hdf5 1.8.17|1.8.17.*',
'icu': 'icu 58.*',
'jpeg': 'jpeg 9*',
'libblitz': 'libblitz 0.10|0.10.*',
'libevent': 'libevent 2.0.*',
'libmatio': 'libmatio 1.5.*',
'libnetcdf': 'libnetcdf 4.4.*',
'libpng': 'libpng >=1.6.28,<1.7',
'libsvm': 'libsvm 3.21|3.21.*',
'libtiff': 'libtiff 4.0.*',
'libxml2': 'libxml2 2.9.*',
'metis': 'metis 5.1.*',
'ncurses': 'ncurses 5.9*',
'netcdf-cxx4': 'netcdf-cxx4 4.3.*',
'netcdf-fortran': 'netcdf-fortran 4.4.*',
'openblas': 'openblas 0.2.19|0.2.19.*',
'openssl': 'openssl 1.0.*',
'pango': 'pango 1.40.*',
'pixman': 'pixman 0.34.*',
'proj4': 'proj4 4.9.3',
'pyqt': 'pyqt 4.11.*',
'qt': 'qt 4.8.*',
'readline': 'readline 6.2*',
'sox': 'sox 14.4.2',
'sqlite': 'sqlite 3.13.*',
'tk': 'tk 8.5.*',
'vlfeat': 'vlfeat 0.9.20',
'xz': 'xz 5.2.*',
'zlib': 'zlib 1.2.*',
}

pinnings["numpy"] = "numpy 1.11"
pinnings["blas"] = "blas 1.11 openblas"

sagelib_deps = ['arb', 'openblas', 'brial', 'cephes', 'cliquer', 'cysignals', 'cython', 'ecl', 'eclib', 'ecm', 'flint', 'libgd', 'givaro', 'glpk', 'gsl', 'iml', 'jinja2', 'jupyter_core', 'lcalc', 'lrcalc', 'libgap', 'libpng', 'linbox', 'm4ri', 'm4rie', 'mpc', 'mpfi', 'mpfr', 'gmp', 'ntl', 'numpy', 'pari', 'pip', 'pkgconfig', 'planarity', 'ppl', 'pynac', 'python', 'ratpoints', 'readline', 'rw', 'singular', 'six', 'symmetrica', 'zn_poly']

sageruntime_deps = ['sagelib', 'ipython', 'pexpect', 'psutil']

deps_dict = {
'sageruntime' : sageruntime_deps,
}

def main():
    pkg_dir="build/pkgs"
    dirs = sorted([d for d in os.listdir(pkg_dir) if os.path.isdir(os.path.join(pkg_dir, d))])
    for pkg in dirs:
        if not pkg in conda_pkgs:
            continue
        conda_file = os.path.join(pkg_dir, pkg, "conda-name")    
        with open(conda_file, 'w') as f:
            f.write(conda_pkgs[pkg].split("=")[0])

    subprocess.call("mkdir -p %s" % sage_local, shell=True)
    subprocess.call("conda install %s autoconf automake -c conda-forge -c r -p %s" % (' '.join(conda_pkgs.values()), sage_local), shell=True)
    # create pc files for openblas
    subprocess.call("export SAGE_LOCAL=%s && cd %s/build/pkgs/openblas && ./write_pc_file.py" % (sage_local, sage_root), shell=True)

if __name__ == "__main__":
    main()

