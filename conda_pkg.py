import os
import subprocess
from sys import platform

sage_root = os.path.dirname(os.path.realpath(__file__))
sage_local = os.path.join(sage_root, "local")
pkg_dir=os.path.join(sage_root, "build/pkgs")
sage_version="7.5.1"

conda_pkgs = {
'alabaster' : 'alabaster',
'appnope' : '',
'arb' : 'arb',
'autotools' : 'automake libtool',
'babel' : 'babel',
'backports_abc' : 'backports_abc',
'backports_shutil_get_terminal_size' : 'backports.shutil_get_terminal_size',
'backports_ssl_match_hostname' : 'ssl_match_hostname',
'boost_cropped' : 'boost-cpp',
'brial':'brial',
'bzip2' : 'bzip2',
'cddlib':'cddlib',
'cliquer':'cliquer',
'combinatorial_designs':'sagemath-db-combinatorial-designs',
'configparser' : 'configparser',
'conway_polynomials':'sagemath-db-conway-polynomials',
'cvxopt' : 'cvxopt',
'cycler' : 'cycler',
'cysignals' : 'cysignals',
'cython' : 'cython',
'dateutil' : 'dateutil',
'decorator' : 'decorator',
'docutils' : 'docutils',
'ecl':'ecl',
'eclib':'eclib',
'ecm' : 'ecm',
'elliptic_curves':'sagemath-db-elliptic-curves',
'entrypoints' : 'entrypoints',
'fflas_ffpack':'fflas-ffpack',
'flask_babel' : 'flask-babel',
'flask' : 'flask',
'flask_openid' : 'flask-openid',
'flint' : 'libflint',
'flintqs':'flintqs',
'fpylll':'fpylll',
'freetype' : 'freetype',
'functools32' : 'functools32',
'future' : 'future',
'gap':'gap=4.8.3',
'gc' : 'bdw-gc',
'gcc' : 'gcc',
'gf2x':'gf2x',
'gfan':'gfan',
'giac' : 'giac',
'git' : 'git',
'givaro':'givaro',
'glpk' : 'glpk',
'graphs':'sagemath-db-graphs',
'gsl' : 'gsl',
'iconv' : 'libiconv',
'imagesize' : 'imagesize',
'iml':'iml',
'ipykernel' : 'ipykernel',
'ipython_genutils' : 'ipython_genutils',
'ipython' : 'ipython',
'ipywidgets' : 'ipywidgets',
'itsdangerous' : 'itsdangerous',
'jinja2' : 'jinja2',
'jsonschema' : 'jsonschema',
'jupyter_client' : 'jupyter_client',
'jupyter_core' : 'jupyter_core',
'lcalc':'lcalc',
'libfplll':'fplll',
'libgap':'libgap',
'libgd' : 'libgd',
'libpng' : 'libpng',
'linbox':'linbox',
'lrcalc':'lrcalc',
'm4rie':'m4rie',
'm4ri':'m4ri',
'markupsafe' : 'markupsafe',
'matplotlib' : 'matplotlib',
'mistune' : 'mistune',
'mpc' : 'mpc',
'mpfi':'mpfi',
'mpfr' : 'mpfr',
'mpir' : 'gmp',
'mpmath' : 'mpmath',
'nauty' : 'nauty',
'nbconvert' : 'nbconvert',
'nbformat' : 'nbformat',
'ncurses' : 'ncurses',
'networkx' : 'networkx',
'notebook' : 'notebook',
'ntl':'ntl',
'numpy' : 'numpy=1.11',
'openblas' : 'openblas',
'palp':'palp',
'pari_galdata':'pari',
'pari':'pari',
'pari_seadata_small':'pari',
'pathlib2' : 'pathlib2',
'pathpy' : 'path.py',
'pexpect' : 'pexpect',
'pickleshare' : 'pickleshare',
'pillow' : 'pillow',
'pip' : 'pip',
'pkgconfig' : 'pkgconfig',
'planarity':'planarity',
'polytopes_db':'sagemath-db-polytopes',
'ppl':'ppl',
'prompt_toolkit' : 'prompt_toolkit',
'psutil' : 'psutil',
'ptyprocess' : 'ptyprocess',
'pycrypto' : 'pycrypto',
'pygments' : 'pygments',
'pynac':'pynac',
'pyparsing' : 'pyparsing',
'python2' : 'python=2.7',
'python_openid' : 'python-openid',
'pytz' : 'pytz',
'pyzmq' : 'pyzmq',
'r' : 'r-base',
'ratpoints':'ratpoints',
'readline' : 'readline',
'rubiks':'rubiks',
'rw':'rw',
'scipy' : 'scipy',
'setuptools_scm' : 'setuptools_scm',
'setuptools' : 'setuptools',
'simplegeneric' : 'simplegeneric',
'singledispatch' : 'singledispatch',
'singular':'singular',
'six' : 'six',
'snowballstemmer' : 'snowballstemmer',
'speaklater' : 'speaklater',
'sphinx' : 'sphinx',
'sqlite' : 'sqlite',
'symmetrica':'symmetrica',
'sympy' : 'sympy',
'terminado' : 'terminado',
'tornado' : 'tornado',
'traitlets' : 'traitlets',
'vcversioner' : 'vcversioner',
'wcwidth' : 'wcwidth',
'werkzeug' : 'werkzeug',
'widgetsnbextension' : 'widgetsnbextension',
'zeromq' : 'zeromq',
'zlib' : 'zlib',
'zn_poly':'zn_poly',
}

if platform == "darwin":
    conda_pkgs["appnope"] = "appnope"

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

pinnings["numpy"] = "numpy 1.11.*"
pinnings["blas"] = "blas 1.1 openblas"
pinnings["appnope"] = "appnope  # [osx]"

sagelib_deps = ['arb', 'openblas', 'brial', 'cephes', 'cliquer', 'cysignals', 'cython', 'ecl', 'eclib', 'ecm', 'flint', 'libgd', 'givaro', 'glpk', 'gsl', 'iml', 'jinja2', 'jupyter_core', 'lcalc', 'lrcalc', 'libgap', 'libpng', 'linbox', 'm4ri', 'm4rie', 'mpc', 'mpfi', 'mpfr', 'gmp', 'ntl', 'numpy', 'pari', 'pip', 'pkgconfig', 'planarity', 'ppl', 'pynac', 'python', 'ratpoints', 'readline', 'rw', 'singular', 'six', 'symmetrica', 'zn_poly']

sageruntime_deps = ['sagelib', 'ipython', 'pexpect', 'psutil']

sagestandard_deps = ['alabaster ' 'appnope ' 'arb ' 'babel ' 'backports_abc ' 'backports_shutil_get_terminal_size ' 'backports_ssl_match_hostname ' 'boost_cropped ' 'brial ' 'bzip2 ' 'cddlib ' 'cephes ' 'certifi ' 'cliquer ' 'combinatorial_designs ' 'configparser ' 'conway_polynomials ' 'cvxopt ' 'cycler ' 'cysignals ' 'cython ' 'dateutil ' 'decorator ' 'docutils ' 'ecl ' 'eclib ' 'ecm ' 'elliptic_curves ' 'entrypoints ' 'fflas_ffpack ' 'flask ' 'flask_autoindex ' 'flask_babel ' 'flask_oldsessions ' 'flask_openid ' 'flask_silk ' 'flint ' 'flintqs ' 'fpylll ' 'freetype ' 'functools32 ' 'future ' 'gap ' 'gc ' 'gcc ' 'gf2x ' 'gfan ' 'giac ' 'git ' 'givaro ' 'glpk ' 'graphs ' 'gsl ' 'iconv ' 'imagesize ' 'iml ' 'ipykernel ' 'ipython ' 'ipython_genutils ' 'ipywidgets ' 'itsdangerous ' 'jinja2 ' 'jmol ' 'jsonschema ' 'jupyter_client ' 'jupyter_core ' 'lcalc ' 'libfplll ' 'libgap ' 'libgd ' 'libpng ' 'linbox ' 'lrcalc ' 'm4ri ' 'm4rie ' 'markupsafe ' 'mathjax ' 'matplotlib ' 'maxima ' 'mistune ' 'mpc ' 'mpfi ' 'mpfr ' 'mpmath ' 'nauty ' 'nbconvert ' 'nbformat ' 'ncurses ' 'networkx ' 'notebook ' 'ntl ' 'numpy ' 'openblas ' 'palp ' 'pari ' 'pari_galdata ' 'pari_seadata_small ' 'patch ' 'pathlib2 ' 'pathpy ' 'pexpect ' 'pickleshare ' 'pillow ' 'pip ' 'pkgconf ' 'pkgconfig ' 'planarity ' 'polytopes_db ' 'ppl ' 'prompt_toolkit ' 'psutil ' 'ptyprocess ' 'pycrypto ' 'pygments ' 'pynac ' 'pyparsing ' 'python_openid ' 'pytz ' 'pyzmq ' 'r ' 'ratpoints ' 'readline ' 'rpy2 ' 'rubiks ' 'rw ' 'sagenb ' 'sagenb_export ' 'sagetex ' 'scipy ' 'setuptools ' 'setuptools_scm ' 'simplegeneric ' 'singledispatch ' 'singular ' 'six ' 'snowballstemmer ' 'speaklater ' 'sphinx ' 'sqlite ' 'symmetrica ' 'sympow ' 'sympy ' 'tachyon ' 'terminado ' 'thebe ' 'tornado ' 'traitlets ' 'twisted ' 'vcversioner ' 'wcwidth ' 'werkzeug ' 'widgetsnbextension ' 'zeromq ' 'zlib ' 'zn_poly ' 'zope_interface']

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
    subprocess.call("cp sage local/sage", shell=True)
    subprocess.call("conda install %s -c conda-forge -p %s" % (' '.join(conda_pkgs.values()), sage_local), shell=True)

if __name__ == "__main__":
    main()

