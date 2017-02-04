import os
import sys
import subprocess

from conda_pkg import conda_pkgs, sagelib_deps, sageruntime_deps, pinnings

sage_root = os.path.dirname(os.path.realpath(__file__))
sage_local = os.path.join(sage_root, "local")
pkg_dir=os.path.join(sage_root, "build/pkgs")
prefix = os.getenv('PREFIX', "")

def get_files():
    file_list = []
    dir_path = sage_local
    for path, subdirs, files in os.walk(dir_path):
        for name in files:
            file_name = os.path.relpath(os.path.join(path, name), dir_path)
            if not (file_name.startswith("var/tmp/sage/build/") or file_name.startswith("var/lib/sage/installed/") or
                    file_name.endswith(".pyc") or file_name.endswith(".pyo") or file_name.startswith("lib/sage-force-relocate.txt")):
                file_list.append(file_name)
    return file_list

def save_file_list(pkg, file_list, file_name):
    with open(file_name, "w") as f:
        for i in file_list:
            f.write("%s\n" % i)

def load_file_list(pkg, file_name):
    with open(file_name) as f:
        return [i.strip() for i in f.readlines()]

def convert_deps(dep_list):
    run_deps = []
    for i in range(len(dep_list)):
        d = dep_list[i]
        d = conda_pkgs.get(d, d)
        if '=' in d:
            d = d.split("=")[0]
        if d not in ["pkgconf", "m4", "perl", "patch", "pkgconfig", "automake", "pip", "setuptools", "cython"]:
            run_deps.append(d)
    return run_deps

def get_deps(pkg):
    if pkg == "sagelib":
        return convert_deps(sagelib_deps) + ["pip", "setuptools", "cython"]
    if pkg == "sageruntime":
        return convert_deps(sageruntime_deps)
    deps_file = os.path.join(pkg_dir, pkg, "dependencies")
    if not os.path.exists(deps_file):
        return []
    with open(deps_file) as f:
        content = f.readlines()[0]
        if content[0] == "#":
            return []
        deps = content.strip()
        deps = deps.replace("$(PYTHON)", "python2")
        deps = deps.replace("| ", "")
        deps = deps.replace("$(MP_LIBRARY)", "gmp")
        deps = deps.replace("$(SAGE_MP_LIBRARY)", "gmp")
        deps = deps.replace("$(BLAS)", "openblas blas")
        deps = deps.replace("$(SAGERUNTIME)", "sageruntime")
        deps = deps.replace("$(INST)/", "")
        deps = deps.split()
        return convert_deps(deps)
    return []


def get_version(pkg):
    if pkg == "sagelib" or pkg =="sageruntime":
        return "7.5.1"
    ver_file = os.path.join(pkg_dir, pkg, "package-version.txt")
    with open(ver_file) as f:
        return f.readlines()[0].strip()
    return ""

def build_conda_pkg(pkg, file_list):
    deps = get_deps(pkg)
    reqs = ""
    for dep in deps:
        reqs += "    - %s \n" % pinnings.get(dep, dep)

    if reqs != "":
        reqs_str = """
requirements:
  run:
%s
"""
        reqs = reqs_str % (reqs)

    if "openblas" in deps:
        features = """
  features:
    - blas_openblas
"""
        reqs = features + reqs
    
    meta_yaml = """
{%% set name = "%s" %%}
{%% set version = "%s" %%}
{%% set sage_root = "%s" %%}

package:
  name: {{ name }}
  version: {{ version }}

build:
  number: 0
  script:
    - python conda_build_script.py {{ sage_root }} {{ name }}
%s

about:
  description: |
    {{ name }} packaged for sagemath. Download sage-spkg-sources for the source
""";
    
    subprocess.call("mkdir -p %s" % os.path.join(sage_root, "recipes", pkg), shell=True)

    with open(os.path.join(sage_root, "recipes", pkg, "meta.yaml"), "w") as f:
        f.write(meta_yaml % (pkg, get_version(pkg), sage_root, reqs))

    shell_cmd = "cd %s && conda build %s --python 2.7"
    shell_cmd = shell_cmd % (os.path.join(sage_root, "recipes"), pkg) 
    subprocess.call(shell_cmd, shell=True)

    with open(os.path.join(pkg_dir, pkg, "conda-name"), "w") as f:
        f.write("%s\n" % pkg)

def main():
    pkg = sys.argv[1]
    before = sys.argv[2] == "before"
    file_list = get_files()
    file_name = os.path.join(sage_root, "before.txt")
    if before:
        #pass
        save_file_list(pkg, file_list, file_name)
    else:
        before_list = set(load_file_list(pkg, file_name))
        file_list = [os.path.join(prefix, f) for f in (set(file_list) - before_list)]
        save_file_list(pkg, file_list, os.path.join(sage_root, "%s.txt" % pkg))
        #file_list = load_file_list(pkg, os.path.join(sage_root, "%s.txt" % pkg))
        build_conda_pkg(pkg, file_list)

if __name__ == "__main__":
    main()
