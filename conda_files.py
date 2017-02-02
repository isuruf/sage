import os
import sys

sage_root = os.path.dirname(os.path.realpath(__file__))
prefix = os.getenv('PREFIX', "")

def get_files():
    file_list = []
    dir_path = os.path.join(sage_root, "local")
    for path, subdirs, files in os.walk(dir_path):
        for name in files:
            file_name = os.path.relpath(os.path.join(path, name), dir_path)
            if not (file_name.startswith("var/tmp/sage/build/") or file_name.startswith("var/lib/sage/installed/") or
                    file_name.endswith(".pyc") or file_name.endswith(".pyo")):
                file_list.append(dir_path)
    return file_list

def save_file_list(pkg, file_list, file_name):
    with open(file_name, "w") as f:
        for i in file_list:
            f.write("%s\n" % i)

def load_file_list(pkg, file_name):
    with open(file_name) as f:
        return [i.strip() for i in f.readlines()]

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

if __name__ == "__main__":
    main()
