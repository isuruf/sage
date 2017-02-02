import os
import sys
import subprocess

from conda_pkg import conda_pkgs, sagelib_deps, sageruntime_deps

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


def get_deps(pkg):
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
        return deps
    return []


def get_version(pkg):
    ver_file = os.path.join(pkg_dir, pkg, "package-version.txt")
    with open(ver_file) as f:
        return f.readlines()[0].strip()
    return ""

def build_conda_pkg(pkg, file_list):
    deps = get_deps(pkg)
    reqs = ""
    for dep in deps:
        reqs += "    - %s \n" % dep
    
    if reqs != "":
        reqs_str = """
requirements:
  build:
%s
  run:
%s
"""
        reqs = reqs_str % (reqs, reqs)
    
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
    - for file in $(cat {{ sage_root }}/{{ name }}.txt); do mkdir -p `dirname "$PREFIX/$file"` && cp "{{ sage_root }}/local/$file" "$PREFIX/$file"; done

%s
""";
    
    subprocess.call("mkdir -p %s" % os.path.join(sage_root, "recipes", pkg), shell=True)

    with open(os.path.join(sage_root, "recipes", pkg, "meta.yaml"), "w") as f:
        f.write(meta_yaml % (pkg, get_version(pkg), sage_root, reqs))

    shell_cmd = "cd %s && conda build %s --python 2.7 && conda install %s --use-local -p %s"
    shell_cmd = shell_cmd % (os.path.join(sage_root, "recipes"), pkg, pkg, sage_local) 
    subprocess.call(shell_cmd, shell=True)

    with open(os.path.join(pkg_dir, pkg, "conda-name"), "w") as f:
        f.write("%s\n" % pkg)

def main():
    pkg = sys.argv[1]
    before = sys.argv[2] == "before"
    file_list = get_files()
    file_name = os.path.join(sage_root, "before.txt")
    if before:
        save_file_list(pkg, file_list, file_name)
    else:
        before_list = set(load_file_list(pkg, file_name))
        file_list = [os.path.join(prefix, f) for f in (set(file_list) - before_list)]
        save_file_list(pkg, file_list, os.path.join(sage_root, "%s.txt" % pkg))
        build_conda_pkg(pkg, file_list)

if __name__ == "__main__":
    main()
