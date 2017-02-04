import sys
import os
import shutil
import errno

sage_root = sys.argv[1]
sage_local = os.path.join(sage_root, "local")
pkg = sys.argv[2]
prefix = os.getenv("PREFIX")

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

with open(os.path.join(sage_root, "%s.txt" % pkg)) as file_list:
    files = file_list.readlines()
    for f in files:
        f = f.strip()
        if (f == ""):
            continue
        dst = os.path.join(prefix, f)
        f = os.path.join(sage_local, f)
        mkdir_p(os.path.dirname(dst))
        if os.path.islink(f):
            src = os.path.join(prefix, os.path.relpath(os.path.realpath(f), sage_local))
            os.symlink(src, dst)
        else:
            shutil.copy(f, dst)
