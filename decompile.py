import os
from utils import fs
from format.qvm import QVM
import ast
import qsc


def decompile_qvm():
    src_folder = "input"
    dst_folder = "output"
    count = 0

    try:
        for srcpath in fs.walkdir(src_folder, '*.qvm'):
            qvmfile = QVM()
            qvmfile.load(srcpath)
            qvmtree = ast.fromfile(qvmfile)
            qvmtext = qsc.fromtree(qvmtree)

            dstfile = srcpath.replace(src_folder, dst_folder, 1).replace('.qvm', '.qsc')
            os.makedirs(os.path.dirname(dstfile), exist_ok=True)

            with open(dstfile, 'w') as o:
                o.write(qvmtext)

            count += 1

        print('Decompiled: {0}'.format(count))
    except Exception as e:
        print('Error: {0}'.format(str(e)))


if __name__ == "__main__":
    decompile_qvm()
